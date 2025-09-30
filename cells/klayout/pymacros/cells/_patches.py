# Copyright 2025 GlobalFoundries PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ==============================================================================
# ---------------- Patches for compatibility with gdsfactory v9 ----------------
# ==============================================================================

def _patch_class_attr(cls, name, attr, force=False):
    """
    Add or replace an attribute (method or property) on a class.

    Args:
        cls: The class to patch.
        name: The name of the attribute to add.
        attr: The method or property object.
        force: If True, will override existing attributes.
    """
    if not hasattr(cls, name) or force:
        setattr(cls, name, attr)
    else:
        print(f"[patch_class_attr] Skipped: '{cls.__name__}.{name}' already exists.")


def patch_legacy_classes():
    import gdsfactory as gf
    from importlib.util import find_spec
    from typing import Optional

    #
    # Replacement for gdsfactory.Component.add_array() method
    #

    # noinspection PyPep8Naming
    def __gf__Component__add_array(
        self: gf.Component,
        component: gf.Component,
        columns: int = 2,
        rows: int = 2,
        spacing: tuple[float, float] = (100, 100),
        alias: Optional[str] = None
    ) -> gf.ComponentReference:
        column_pitch = spacing[0]
        row_pitch = spacing[1]
        ref = self.add_ref(
            component=component,
            name=alias,
            columns=columns,
            rows=rows,
            column_pitch=column_pitch,
            row_pitch=row_pitch
        )
        return ref


    # noinspection PyPep8Naming
    def __gf__component_layout___GeometryHelper__size(self):  # gf.component_layout._GeometryHelper
        return self.xsize, self.ysize


    _patch_class_attr(gf.Component, 'add_array', __gf__Component__add_array)
    _patch_class_attr(gf.Component, 'size', property(__gf__component_layout___GeometryHelper__size))
    _patch_class_attr(gf.ComponentReference, 'size', property(__gf__component_layout___GeometryHelper__size))
    
    # class gdsfactory.geometry.boolean (v7) now resides under gdsfactory.boolean (v9)
    if find_spec('gdsfactory.geometry') is None:
        class DummyNamespace:
            pass
        gf__geometry = DummyNamespace()
        gf__geometry.boolean = gf.boolean
        gf.geometry = gf__geometry


    # gf.Component("nfet_dev") for example would yield the error below, e.g. when changing PCell parameters
    #
    #ERROR: ValueError: Cellname nfet_dev already exists. Please make sure the cellname is unique or pass `allow_duplicate` when creating the library in PCellDeclaration.produce
    #  /usr/local/lib/python3.12/dist-packages/kfactory/layout.py:1209
    #  /usr/local/lib/python3.12/dist-packages/kfactory/kcell.py:594
    #  /usr/local/lib/python3.12/dist-packages/kfactory/kcell.py:2563

    import klayout.db as kdb
    import kfactory.layout
    original_method = kfactory.layout.KCLayout.create_cell

    # noinspection PyPep8Naming
    def __kfactory__layout__KCLayout_create_cell(
        self,
        name: str,
        *args: str,
        allow_duplicate: bool = True,
    ) -> kdb.Cell:
        return original_method(self, name, *args, allow_duplicate=allow_duplicate)

    kfactory.layout.KCLayout.create_cell = __kfactory__layout__KCLayout_create_cell