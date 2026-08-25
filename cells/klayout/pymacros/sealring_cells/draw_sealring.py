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
from .layers import Layers

sealring_edge_width = 16

# contact to contact spacing
c2c_spacing = 0.7

# via to via spacing
v2v_spacing = 0.7

# When doing flip-chip packaging, the guard ring needs to be protected
# If not, pad opening is required

# AD layer is missing -> what is it?

solid_layers_table = {
    "bonding": [
        # Pad (Passivation) opening
        {"layer": Layers.Pad, "start": 4, "end": 13},
        {"layer": Layers.COMP, "start": 0, "end": 16},
        {"layer": Layers.Pplus, "start": 0, "end": 16},
        {"layer": Layers.GUARD_RING_MK, "start": 0, "end": 16},
        {"layer": Layers.Metal1, "start": 1, "end": 16},
        {"layer": Layers.Metal2, "start": 0, "end": 16},
        {"layer": Layers.Metal3, "start": 1, "end": 16},
        {"layer": Layers.Metal4, "start": 0, "end": 16},
        {"layer": Layers.Metal5, "start": 1, "end": 16},
        {"layer": Layers.MetalTop, "start": 0, "end": 16},
    ],
    "flip-chip": [
        {"layer": Layers.COMP, "start": 0, "end": 16},
        {"layer": Layers.Pplus, "start": 0, "end": 16},
        {"layer": Layers.GUARD_RING_MK, "start": 0, "end": 16},
        {"layer": Layers.Metal1, "start": 1, "end": 13},
        {"layer": Layers.Metal2, "start": 0, "end": 13},
        {"layer": Layers.Metal3, "start": 1, "end": 13},
        {"layer": Layers.Metal4, "start": 0, "end": 13},
        {"layer": Layers.Metal5, "start": 1, "end": 13},
        {"layer": Layers.MetalTop, "start": 0, "end": 13},
    ],
}

corner_polygons = {
    "bonding": {
        # Pad (Passivation) opening
        Layers.Pad: [
            db.DPoint(3, 16),
            db.DPoint(12, 16),
            db.DPoint(16, 12),
            db.DPoint(16, 3),
            # Extend based on thickness
            db.DPoint(16 - 4, 3),
            db.DPoint(3, 16 - 4),
        ],
        Layers.COMP: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Pplus: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.GUARD_RING_MK: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Metal1: [
            db.DPoint(0, 16),
            db.DPoint(15, 16),
            db.DPoint(16, 15),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Metal2: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Metal3: [
            db.DPoint(0, 16),
            db.DPoint(15, 16),
            db.DPoint(16, 15),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Metal4: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Metal5: [
            db.DPoint(0, 16),
            db.DPoint(15, 16),
            db.DPoint(16, 15),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.MetalTop: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
    },
    "flip-chip": {
        Layers.COMP: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Pplus: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.GUARD_RING_MK: [
            db.DPoint(0, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 0),
            # Extend based on thickness
            db.DPoint(16 - 7, 0),
            db.DPoint(0, 16 - 7),
        ],
        Layers.Metal1: [
            db.DPoint(3, 16),
            db.DPoint(15, 16),
            db.DPoint(16, 15),
            db.DPoint(16, 3),
            # Extend based on thickness
            db.DPoint(16 - 7, 3),
            db.DPoint(3, 16 - 7),
        ],
        Layers.Metal2: [
            db.DPoint(3, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 3),
            # Extend based on thickness
            db.DPoint(16 - 7, 3),
            db.DPoint(3, 16 - 7),
        ],
        Layers.Metal3: [
            db.DPoint(3, 16),
            db.DPoint(15, 16),
            db.DPoint(16, 15),
            db.DPoint(16, 3),
            # Extend based on thickness
            db.DPoint(16 - 7, 3),
            db.DPoint(3, 16 - 7),
        ],
        Layers.Metal4: [
            db.DPoint(3, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 3),
            # Extend based on thickness
            db.DPoint(16 - 7, 3),
            db.DPoint(3, 16 - 7),
        ],
        Layers.Metal5: [
            db.DPoint(3, 16),
            db.DPoint(15, 16),
            db.DPoint(16, 15),
            db.DPoint(16, 3),
            # Extend based on thickness
            db.DPoint(16 - 7, 3),
            db.DPoint(3, 16 - 7),
        ],
        Layers.MetalTop: [
            db.DPoint(3, 16),
            db.DPoint(16, 16),
            db.DPoint(16, 3),
            # Extend based on thickness
            db.DPoint(16 - 7, 3),
            db.DPoint(3, 16 - 7),
        ],
    },
}

contact_vias_table = [
    {
        "layer": Layers.Contact,
        "start": 3.7,
        "size": 0.22,
        "distance": 1.6,
        "distance2": c2c_spacing,
        "stagger": 0.22 - 0.1,
    },
    {
        "layer": Layers.Via1,
        "start": 4.44,
        "size": 0.26,
        "distance": 1.8,
        "distance2": v2v_spacing,
        "stagger": 0.26 - 0.1,
    },
    {
        "layer": Layers.Via2,
        "start": 3.0,
        "size": 0.26,
        "distance": 1.8,
        "distance2": v2v_spacing,
        "stagger": 0.26 - 0.1,
    },
    {
        "layer": Layers.Via3,
        "start": 4.08,
        "size": 0.26,
        "distance": 1.8,
        "distance2": v2v_spacing,
        "stagger": 0.26 - 0.1,
    },
    {
        "layer": Layers.Via4,
        "start": 3.36,
        "size": 0.26,
        "distance": 1.8,
        "distance2": v2v_spacing,
        "stagger": 0.26 - 0.1,
    },
    {
        "layer": Layers.Via5,
        "start": 3.72,
        "size": 0.26,
        "distance": 1.8,
        "distance2": v2v_spacing,
        "stagger": 0.26 - 0.1,
    },
]

vias_edge_width = {"bonding": 16, "flip-chip": 13}


def draw_sealring(layout, w, h, metal_level, sealring_type="bonding"):

    # Create sealring cell
    sealring_cell = layout.cell(layout.add_cell("sealring"))

    # Draw the vertical sealring edges
    sealring_vertical = draw_sealring_edge(
        layout, h - 2 * sealring_edge_width, metal_level, sealring_type
    )

    sealring_cell.insert(
        db.DCellInstArray(
            sealring_vertical.cell_index(),
            db.DTrans(
                db.DTrans.M90, db.DPoint(sealring_edge_width, sealring_edge_width)
            ),
        )
    )

    sealring_cell.insert(
        db.DCellInstArray(
            sealring_vertical.cell_index(),
            db.DTrans(db.DPoint(w - sealring_edge_width, sealring_edge_width)),
        )
    )

    # Draw the horizontal sealring edges
    sealring_horizontal = draw_sealring_edge(
        layout, w - 2 * sealring_edge_width, metal_level, sealring_type
    )

    sealring_cell.insert(
        db.DCellInstArray(
            sealring_horizontal.cell_index(),
            db.DTrans(
                db.DTrans.R90,
                db.DPoint(w - sealring_edge_width, h - sealring_edge_width),
            ),
        )
    )

    sealring_cell.insert(
        db.DCellInstArray(
            sealring_horizontal.cell_index(),
            db.DTrans(
                db.DTrans.R270, db.DPoint(sealring_edge_width, sealring_edge_width)
            ),
        )
    )

    # Draw the sealring corner
    sealring_corner = draw_sealring_corner(layout, metal_level, sealring_type)

    # Bottom-left
    sealring_cell.insert(
        db.DCellInstArray(
            sealring_corner.cell_index(),
            db.DTrans(db.DPoint(0, 0)),
        )
    )

    # Top-left
    sealring_cell.insert(
        db.DCellInstArray(
            sealring_corner.cell_index(),
            db.DTrans(db.DTrans.R270, db.DPoint(0, h)),
        )
    )

    # Top-right
    sealring_cell.insert(
        db.DCellInstArray(
            sealring_corner.cell_index(),
            db.DTrans(db.DTrans.R180, db.DPoint(w, h)),
        )
    )

    # Bottom-right
    sealring_cell.insert(
        db.DCellInstArray(
            sealring_corner.cell_index(),
            db.DTrans(db.DTrans.R90, db.DPoint(w, 0)),
        )
    )

    # Flatten the cell and merge GUARD_RING_MK polygons
    sealring_cell.flatten(0)
    region = db.Region(
        sealring_cell.begin_shapes_rec(layout.layer(Layers.GUARD_RING_MK))
    )
    region.merge()
    sealring_cell.clear(Layers.GUARD_RING_MK)
    sealring_cell.shapes(Layers.GUARD_RING_MK).insert(region)

    return sealring_cell


def draw_sealring_edge(layout, h, metal_level, sealring_type="bonding"):
    """
    Draw a sealring edge as shown in:
    https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_12_2.html
    """

    if metal_level == "Metal3":
        max_metal = Layers.Metal3
        max_via = Layers.Via2
    elif metal_level == "Metal4":
        max_metal = Layers.Metal4
        max_via = Layers.Via3
    elif metal_level == "Metal5":
        max_metal = Layers.Metal5
        max_via = Layers.Via4
    elif metal_level == "MetalTop":
        max_metal = Layers.MetalTop
        max_via = Layers.Via5

    cell_index = layout.add_cell("sealring_edge")
    sealring_edge_cell = layout.cell(cell_index)

    # Draw the solid layers
    for cur_dict in solid_layers_table[sealring_type]:
        layer, start, end = cur_dict.values()
        sealring_edge_cell.shapes(layer).insert(db.DBox.new(start, 0, end, h))

        if layer == max_metal:
            break

    # Draw the contacts and vias
    for cur_dict in contact_vias_table:

        layer, start, size, distance, distance2, stagger = cur_dict.values()
        contact_vias_cell = layout.cell(layout.add_cell("cont_via"))
        contact_vias_cell.shapes(layer).insert(db.DBox.new(0, 0, size, size))

        for i in range(
            int((vias_edge_width[sealring_type] - start - size) / (size + distance)) + 1
        ):
            sealring_edge_cell.insert(
                db.DCellInstArray(
                    contact_vias_cell.cell_index(),
                    db.DPoint(start + i * distance, i * stagger),
                    db.DVector(0, 0),
                    db.DVector(0, distance2 + size),
                    0,
                    (h - i * stagger) / (distance2 + size),
                )
            )

        if layer == max_via:
            break

    return sealring_edge_cell


def draw_sealring_corner(layout, metal_level, sealring_type="bonding"):

    if metal_level == "Metal3":
        max_metal = Layers.Metal3
    elif metal_level == "Metal4":
        max_metal = Layers.Metal4
    elif metal_level == "Metal5":
        max_metal = Layers.Metal5
    elif metal_level == "MetalTop":
        max_metal = Layers.MetalTop

    cell_index = layout.add_cell("sealring_corner")
    sealring_corner_cell = layout.cell(cell_index)

    # Draw the polygon for each layer
    for layer, points in corner_polygons[sealring_type].items():
        sealring_corner_cell.shapes(layer).insert(db.DPolygon(points))

        if layer == max_metal:
            break

    return sealring_corner_cell
