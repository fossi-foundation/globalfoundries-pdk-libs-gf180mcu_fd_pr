# Copyright 2025 Leo Moser
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

import klayout.db as db


class Layers:

    def by_name(name):
        return Layers.__dict__[name]

    COMP = db.LayerInfo(22, 0)
    Pplus = db.LayerInfo(31, 0)
    Nplus = db.LayerInfo(32, 0)
    DNWELL = db.LayerInfo(12, 0)
    Nwell = db.LayerInfo(21, 0)
    LVPWELL = db.LayerInfo(204, 0)
    Dualgate = db.LayerInfo(55, 0)
    Poly2 = db.LayerInfo(30, 0)
    Nplus = db.LayerInfo(32, 0)
    Pplus = db.LayerInfo(31, 0)
    SAB = db.LayerInfo(49, 0)
    ESD = db.LayerInfo(24, 0)

    Metal1 = db.LayerInfo(34, 0)
    Metal2 = db.LayerInfo(36, 0)
    Metal3 = db.LayerInfo(42, 0)
    Metal4 = db.LayerInfo(46, 0)
    Metal5 = db.LayerInfo(81, 0)
    MetalTop = db.LayerInfo(53, 0)

    Contact = db.LayerInfo(33, 0)
    Via1 = db.LayerInfo(35, 0)
    Via2 = db.LayerInfo(38, 0)
    Via3 = db.LayerInfo(40, 0)
    Via4 = db.LayerInfo(41, 0)
    Via5 = db.LayerInfo(82, 0)

    PR_bndry = db.LayerInfo(0, 0)

    GUARD_RING_MK = db.LayerInfo(167, 5)

    Pad = db.LayerInfo(37, 0)
