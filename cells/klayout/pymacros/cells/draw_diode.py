# Copyright 2022 GlobalFoundries PDK Authors
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

########################################################################################################################
## Diode Pcells Generators for Klayout of GF180MCU
########################################################################################################################

import gdsfactory as gf
from .layers_def import layer
from gdsfactory.typings import Float2
from .via_generator import via_generator, via_stack

import numpy as np
import os


def draw_diode_nd2ps(
    layout,
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    deepnwell: bool = 0,
    pcmpgr: bool = 0,
    lbl: bool = 0,
    p_lbl: str = "",
    n_lbl: str = "",
) -> gf.Component:

    """
    Usage:-
     used to draw N+/LVPWELL diode (Outside DNWELL) by specifying parameters
    Arguments:-
     layout     : Object of layout
     la         : Float of diff length (anode)
     wa         : Float of diff width (anode)
     cw         : Float of cathode width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
     deepnwell  : Boolean of using Deep NWELL device
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    """

    c = gf.Component("diode_nd2ps_dev")

    comp_spacing: float = 0.48
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    dg_enc_cmp = 0.24
    dn_enc_lvpwell = 2.5
    lvpwell_enc_ncmp = 0.6 if (deepnwell == 1) else 0.16
    lvpwell_enc_pcmp = 0.16
    pcmpgr_enc_dn = 2.5
    dg_enc_dn = 0.5
    pcmp_gr_wid = 0.36

    # n generation
    ncmp = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["comp"]))
    nplus = c.add_ref(
        gf.components.rectangle(
            size=(ncmp.dxsize + (2 * np_enc_comp), ncmp.dysize + (2 * np_enc_comp),),
            layer=layer["nplus"],
        )
    )
    nplus.dxmin = ncmp.dxmin - np_enc_comp
    nplus.dymin = ncmp.dymin - np_enc_comp

    ncmp_con = c.add_ref(
        via_stack(
            x_range=(ncmp.dxmin, ncmp.dxmax),
            y_range=(ncmp.dymin, ncmp.dymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp_con

    # p generation
    pcmp = c.add_ref(gf.components.rectangle(size=(cw, la), layer=layer["comp"]))
    pcmp.dxmax = ncmp.dxmin - comp_spacing
    pplus = c.add_ref(
        gf.components.rectangle(
            size=(pcmp.dxsize + (2 * pp_enc_comp), pcmp.dysize + (2 * pp_enc_comp),),
            layer=layer["pplus"],
        )
    )
    pplus.dxmin = pcmp.dxmin - pp_enc_comp
    pplus.dymin = pcmp.dymin - pp_enc_comp

    pcmp_con = c.add_ref(
        via_stack(
            x_range=(pcmp.dxmin, pcmp.dxmax),
            y_range=(pcmp.dymin, pcmp.dymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # pcomp_con

    # diode_mk
    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(nplus.dxmax - pplus.dxmin, nplus.dysize), layer=layer["diode_mk"]
        )
    )
    diode_mk.dxmin = pplus.dxmin
    diode_mk.dymin = pplus.dymin

    # labels generation
    if lbl == 1:

        # n_label generation
        c.add_label(
            n_lbl,
            position=(
                ncmp_con.dxmin + (ncmp_con.dxsize / 2),
                ncmp_con.dymin + (ncmp_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_lbl,
            position=(
                pcmp_con.dxmin + (pcmp_con.dxsize / 2),
                pcmp_con.dymin + (pcmp_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    if deepnwell == 1:
        lvpwell = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.dxmax - pcmp.dxmin + (lvpwell_enc_ncmp + lvpwell_enc_pcmp),
                    ncmp.dysize + (2 * lvpwell_enc_ncmp),
                ),
                layer=layer["lvpwell"],
            )
        )

        lvpwell.dxmin = pcmp.dxmin - lvpwell_enc_pcmp
        lvpwell.dymin = ncmp.dymin - lvpwell_enc_ncmp

        dn_rect = c.add_ref(
            gf.components.rectangle(
                size=(
                    lvpwell.dxsize + (2 * dn_enc_lvpwell),
                    lvpwell.dysize + (2 * dn_enc_lvpwell),
                ),
                layer=layer["dnwell"],
            )
        )

        dn_rect.dxmin = lvpwell.dxmin - dn_enc_lvpwell
        dn_rect.dymin = lvpwell.dymin - dn_enc_lvpwell

        if volt == "5/6V":
            dg = c.add_ref(
                gf.components.rectangle(
                    size=(
                        dn_rect.dxsize + (2 * dg_enc_dn),
                        dn_rect.dysize + (2 * dg_enc_dn),
                    ),
                    layer=layer["dualgate"],
                )
            )
            dg.dcenter = dn_rect.dcenter

        if pcmpgr == 1:

            c_temp_gr = gf.Component("temp_store guard ring")
            rect_pcmpgr_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (dn_rect.dxmax - dn_rect.dxmin) + 2 * pcmpgr_enc_dn,
                        (dn_rect.dymax - dn_rect.dymin) + 2 * pcmpgr_enc_dn,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_in.dmove(
                (dn_rect.dxmin - pcmpgr_enc_dn, dn_rect.dymin - pcmpgr_enc_dn)
            )
            rect_pcmpgr_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) + 2 * pcmp_gr_wid,
                        (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) + 2 * pcmp_gr_wid,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_out.dmove(
                (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
            )
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["comp"],
                )
            )  # guardring Bulk draw

            psdm_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) - 2 * pp_enc_comp,
                        (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) - 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_in.dmove(
                (rect_pcmpgr_in.dxmin + pp_enc_comp, rect_pcmpgr_in.dymin + pp_enc_comp,)
            )
            psdm_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_out.dxmax - rect_pcmpgr_out.dxmin) + 2 * pp_enc_comp,
                        (rect_pcmpgr_out.dymax - rect_pcmpgr_out.dymin) + 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_out.dmove(
                (
                    rect_pcmpgr_out.dxmin - pp_enc_comp,
                    rect_pcmpgr_out.dymin - pp_enc_comp,
                )
            )
            c.add_ref(
                gf.boolean(
                    A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"]
                )
            )  # psdm draw

            # generating contacts

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.dxmin + con_size,
                        rect_pcmpgr_in.dxmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_out.dymin, rect_pcmpgr_in.dymin),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # bottom contact

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.dxmin + con_size,
                        rect_pcmpgr_in.dxmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_in.dymax, rect_pcmpgr_out.dymax),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # upper contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_out.dxmin, rect_pcmpgr_in.dxmin),
                    y_range=(
                        rect_pcmpgr_in.dymin + con_size,
                        rect_pcmpgr_in.dymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # right contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_in.dxmax, rect_pcmpgr_out.dxmax),
                    y_range=(
                        rect_pcmpgr_in.dymin + con_size,
                        rect_pcmpgr_in.dymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # left contact

            comp_m1_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(rect_pcmpgr_in.dxsize, rect_pcmpgr_in.dysize),
                    layer=layer["metal1"],
                )
            )

            comp_m1_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (comp_m1_in.dxsize) + 2 * pcmp_gr_wid,
                        (comp_m1_in.dysize) + 2 * pcmp_gr_wid,
                    ),
                    layer=layer["metal1"],
                )
            )
            comp_m1_out.dmove(
                (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
            )
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["metal1"],
                )
            )  # guardring metal1

    else:

        if volt == "5/6V":
            dg = c.add_ref(
                gf.components.rectangle(
                    size=(
                        ncmp.dxmax - pcmp.dxmin + (2 * dg_enc_cmp),
                        ncmp.dysize + (2 * dg_enc_cmp),
                    ),
                    layer=layer["dualgate"],
                )
            )
            dg.dxmin = pcmp.dxmin - dg_enc_cmp
            dg.dymin = pcmp.dymin - dg_enc_cmp

        lvpwell = c.add_ref(
            gf.components.rectangle(
                size=(diode_mk.dxsize, diode_mk.dysize,), layer=layer["lvpwell"],
            )
        )

        lvpwell.dcenter = diode_mk.dcenter

    # creating layout and cell in klayout

    c.write_gds("diode_nd2ps_temp.gds")
    layout.read("diode_nd2ps_temp.gds")
    os.remove("diode_nd2ps_temp.gds")

    return layout.cell(c.name)


def draw_diode_pd2nw(
    layout,
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    deepnwell: bool = 0,
    pcmpgr: bool = 0,
    lbl: bool = 0,
    p_lbl: str = "",
    n_lbl: str = "",
) -> gf.Component:
    """
    Usage:-
     used to draw 3.3V P+/Nwell diode (Outside DNWELL) by specifying parameters
    Arguments:-
     layout     : Object of layout
     la         : Float of diffusion length (anode)
     wa         : Float of diffusion width (anode)
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
     deepnwell  : Boolean of using Deep NWELL device
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    """

    c = gf.Component("diode_pd2nw_dev")

    comp_spacing: float = 0.48
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    dg_enc_cmp = 0.24
    dn_enc_nwell = 0.5
    nwell_ncmp_enc = 0.28
    nwell_pcmp_enc = 0.43 if volt == "3.3V" else 0.6
    pcmpgr_enc_dn = 2.5
    dg_enc_dn = 0.5
    pcmp_gr_wid = 0.36

    # p generation
    pcmp = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["comp"]))
    pplus = c.add_ref(
        gf.components.rectangle(
            size=(pcmp.dxsize + (2 * pp_enc_comp), pcmp.dysize + (2 * pp_enc_comp),),
            layer=layer["pplus"],
        )
    )
    pplus.dxmin = pcmp.dxmin - pp_enc_comp
    pplus.dymin = pcmp.dymin - pp_enc_comp
    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(pcmp.dxsize, pcmp.dysize), layer=layer["diode_mk"]
        )
    )
    diode_mk.dxmin = pcmp.dxmin
    diode_mk.dymin = pcmp.dymin

    pcmp_con = c.add_ref(
        via_stack(
            x_range=(pcmp.dxmin, pcmp.dxmax),
            y_range=(pcmp.dymin, pcmp.dymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # pcomp_contact

    # n generation
    ncmp = c.add_ref(gf.components.rectangle(size=(cw, la), layer=layer["comp"]))
    ncmp.dxmax = pcmp.dxmin - comp_spacing
    nplus = c.add_ref(
        gf.components.rectangle(
            size=(ncmp.dxsize + (2 * np_enc_comp), ncmp.dysize + (2 * np_enc_comp),),
            layer=layer["nplus"],
        )
    )
    nplus.dxmin = ncmp.dxmin - np_enc_comp
    nplus.dymin = ncmp.dymin - np_enc_comp

    ncmp_con = c.add_ref(
        via_stack(
            x_range=(ncmp.dxmin, ncmp.dxmax),
            y_range=(ncmp.dymin, ncmp.dymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp contact

    # labels generation
    if lbl == 1:

        # n_label generation
        c.add_label(
            n_lbl,
            position=(
                ncmp_con.dxmin + (ncmp_con.dxsize / 2),
                ncmp_con.dymin + (ncmp_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_lbl,
            position=(
                pcmp_con.dxmin + (pcmp_con.dxsize / 2),
                pcmp_con.dymin + (pcmp_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    # nwell generation
    nwell = c.add_ref(
        gf.components.rectangle(
            size=(
                pcmp.dxmax - ncmp.dxmin + (nwell_ncmp_enc + nwell_pcmp_enc),
                pcmp.dysize + (2 * nwell_pcmp_enc),
            ),
            layer=layer["nwell"],
        )
    )

    nwell.dxmin = ncmp.dxmin - nwell_ncmp_enc
    nwell.dymin = pcmp.dymin - nwell_pcmp_enc

    if deepnwell == 1:

        dn_rect = c.add_ref(
            gf.components.rectangle(
                size=(
                    nwell.dxsize + (2 * dn_enc_nwell),
                    nwell.dysize + (2 * dn_enc_nwell),
                ),
                layer=layer["dnwell"],
            )
        )

        dn_rect.dxmin = nwell.dxmin - dn_enc_nwell
        dn_rect.dymin = nwell.dymin - dn_enc_nwell

        if volt == "5/6V":
            dg = c.add_ref(
                gf.components.rectangle(
                    size=(
                        dn_rect.dxsize + (2 * dg_enc_dn),
                        dn_rect.dysize + (2 * dg_enc_dn),
                    ),
                    layer=layer["dualgate"],
                )
            )
            dg.dcenter = dn_rect.dcenter

        if pcmpgr == 1:

            c_temp_gr = gf.Component("temp_store guard ring")
            rect_pcmpgr_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (dn_rect.dxmax - dn_rect.dxmin) + 2 * pcmpgr_enc_dn,
                        (dn_rect.dymax - dn_rect.dymin) + 2 * pcmpgr_enc_dn,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_in.dmove(
                (dn_rect.dxmin - pcmpgr_enc_dn, dn_rect.dymin - pcmpgr_enc_dn)
            )
            rect_pcmpgr_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) + 2 * pcmp_gr_wid,
                        (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) + 2 * pcmp_gr_wid,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_out.dmove(
                (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
            )
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["comp"],
                )
            )  # Bulk guardring

            psdm_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) - 2 * pp_enc_comp,
                        (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) - 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_in.dmove(
                (rect_pcmpgr_in.dxmin + pp_enc_comp, rect_pcmpgr_in.dymin + pp_enc_comp,)
            )
            psdm_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_out.dxmax - rect_pcmpgr_out.dxmin) + 2 * pp_enc_comp,
                        (rect_pcmpgr_out.dymax - rect_pcmpgr_out.dymin) + 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_out.dmove(
                (
                    rect_pcmpgr_out.dxmin - pp_enc_comp,
                    rect_pcmpgr_out.dymin - pp_enc_comp,
                )
            )
            c.add_ref(
                gf.boolean(
                    A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"]
                )
            )  # psdm guardring

            # generating contacts

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.dxmin + con_size,
                        rect_pcmpgr_in.dxmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_out.dymin, rect_pcmpgr_in.dymin),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # bottom contact

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.dxmin + con_size,
                        rect_pcmpgr_in.dxmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_in.dymax, rect_pcmpgr_out.dymax),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # upper contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_out.dxmin, rect_pcmpgr_in.dxmin),
                    y_range=(
                        rect_pcmpgr_in.dymin + con_size,
                        rect_pcmpgr_in.dymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # right contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_in.dxmax, rect_pcmpgr_out.dxmax),
                    y_range=(
                        rect_pcmpgr_in.dymin + con_size,
                        rect_pcmpgr_in.dymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # left contact

            comp_m1_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(rect_pcmpgr_in.dxsize, rect_pcmpgr_in.dysize),
                    layer=layer["metal1"],
                )
            )

            comp_m1_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (comp_m1_in.dxsize) + 2 * pcmp_gr_wid,
                        (comp_m1_in.dysize) + 2 * pcmp_gr_wid,
                    ),
                    layer=layer["metal1"],
                )
            )
            comp_m1_out.dmove(
                (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
            )
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["metal1"],
                )
            )  # guardring metal1

    else:

        if volt == "5/6V":
            dg = c.add_ref(
                gf.components.rectangle(
                    size=(
                        pcmp.dxmax - ncmp.dxmin + (2 * dg_enc_cmp),
                        ncmp.dysize + (2 * dg_enc_cmp),
                    ),
                    layer=layer["dualgate"],
                )
            )
            dg.dxmin = ncmp.dxmin - dg_enc_cmp
            dg.dymin = ncmp.dymin - dg_enc_cmp

    # creating layout and cell in klayout

    c.write_gds("diode_pd2nw_temp.gds")
    layout.read("diode_pd2nw_temp.gds")
    os.remove("diode_pd2nw_temp.gds")

    return layout.cell(c.name)


def draw_diode_nw2ps(
    layout,
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    lbl: bool = 0,
    p_lbl: str = "",
    n_lbl: str = "",
) -> gf.Component:
    """
    Usage:-
     used to draw 3.3V Nwell/Psub diode by specifying parameters
    Arguments:-
     layout     : Object of layout
     la         : Float of diff length (anode)
     wa         : Float of diff width (anode)
     cw         : Float of Cathode width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
    """

    c = gf.Component("diode_nw2ps_dev")

    comp_spacing: float = 0.48
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    dg_enc_cmp = 0.24

    nwell_ncmp_enc = 0.16

    nwell = c.add_ref(gf.components.rectangle(size=(wa, la,), layer=layer["nwell"],))

    # n generation
    ncmp = c.add_ref(
        gf.components.rectangle(
            size=(
                nwell.dxsize - (2 * nwell_ncmp_enc),
                nwell.dysize - (2 * nwell_ncmp_enc),
            ),
            layer=layer["comp"],
        )
    )
    ncmp.dcenter = nwell.dcenter

    nplus = c.add_ref(
        gf.components.rectangle(
            size=(ncmp.dxsize + (2 * np_enc_comp), ncmp.dysize + (2 * np_enc_comp),),
            layer=layer["nplus"],
        )
    )
    nplus.dxmin = ncmp.dxmin - np_enc_comp
    nplus.dymin = ncmp.dymin - np_enc_comp

    n_con = c.add_ref(
        via_stack(
            x_range=(ncmp.dxmin, ncmp.dxmax),
            y_range=(ncmp.dymin, ncmp.dymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp contact

    # p generation
    pcmp = c.add_ref(
        gf.components.rectangle(size=(cw, ncmp.dysize), layer=layer["comp"])
    )
    pcmp.dcenter = ncmp.dcenter
    pcmp.dxmax = ncmp.dxmin - comp_spacing
    pplus = c.add_ref(
        gf.components.rectangle(
            size=(pcmp.dxsize + (2 * pp_enc_comp), pcmp.dysize + (2 * pp_enc_comp),),
            layer=layer["pplus"],
        )
    )
    pplus.dxmin = pcmp.dxmin - pp_enc_comp
    pplus.dymin = pcmp.dymin - pp_enc_comp

    p_con = c.add_ref(
        via_stack(
            x_range=(pcmp.dxmin, pcmp.dxmax),
            y_range=(pcmp.dymin, pcmp.dymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # pcmop contact

    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(nwell.dxmax - pplus.dxmin, nwell.dysize), layer=layer["well_diode_mk"]
        )
    )
    diode_mk.dxmin = pplus.dxmin
    diode_mk.dymin = nwell.dymin

    # labels generation
    if lbl == 1:

        # n_label generation
        c.add_label(
            n_lbl,
            position=(
                n_con.dxmin + (n_con.dxsize / 2),
                n_con.dymin + (n_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_lbl,
            position=(
                p_con.dxmin + (p_con.dxsize / 2),
                p_con.dymin + (p_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.dxmax - pcmp.dxmin + (2 * dg_enc_cmp),
                    ncmp.dysize + (2 * dg_enc_cmp),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.dxmin = pcmp.dxmin - dg_enc_cmp
        dg.dymin = pcmp.dymin - dg_enc_cmp

    # creating layout and cell in klayout

    c.write_gds("diode_nw2ps_temp.gds")
    layout.read("diode_nw2ps_temp.gds")
    os.remove("diode_nw2ps_temp.gds")

    return layout.cell(c.name)


def draw_diode_pw2dw(
    layout,
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    pcmpgr: bool = 0,
    lbl: bool = 0,
    p_lbl: str = "",
    n_lbl: str = "",
) -> gf.Component:
    """
    Usage:-
     used to draw LVPWELL/DNWELL diode by specifying parameters
    Arguments:-
     layout     : Object of layout
     la         : Float of diff length (anode)
     wa         : Float of diff width (anode)
     cw         : Float of cathode width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
    """

    c = gf.Component("diode_pw2dw_dev")

    comp_spacing: float = 0.92
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    dg_enc_dn = 0.5

    lvpwell_enc_pcmp = 0.16
    dn_enc_lvpwell = 2.5

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    pcmpgr_enc_dn = 2.5
    pcmp_gr_wid = 0.36
    grw = 0.36

    lvpwell = c.add_ref(
        gf.components.rectangle(size=(wa, la,), layer=layer["lvpwell"],)
    )

    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(lvpwell.dxsize, lvpwell.dysize), layer=layer["well_diode_mk"]
        )
    )
    diode_mk.dxmin = lvpwell.dxmin
    diode_mk.dymin = lvpwell.dymin

    if (wa < ((2 * grw) + comp_spacing + (2 * lvpwell_enc_pcmp))) or (
        la < ((2 * grw) + comp_spacing + (2 * lvpwell_enc_pcmp))
    ):

        # p generation
        pcmp = c.add_ref(
            gf.components.rectangle(
                size=(
                    lvpwell.dxsize - (2 * lvpwell_enc_pcmp),
                    lvpwell.dysize - (2 * lvpwell_enc_pcmp),
                ),
                layer=layer["comp"],
            )
        )
        pcmp.dcenter = lvpwell.dcenter

        pplus = c.add_ref(
            gf.components.rectangle(
                size=(
                    pcmp.dxsize + (2 * pp_enc_comp),
                    pcmp.dysize + (2 * pp_enc_comp),
                ),
                layer=layer["pplus"],
            )
        )
        pplus.dxmin = pcmp.dxmin - pp_enc_comp
        pplus.dymin = pcmp.dymin - pp_enc_comp

        p_con = c.add_ref(
            via_stack(
                x_range=(pcmp.dxmin, pcmp.dxmax),
                y_range=(pcmp.dymin, pcmp.dymax),
                base_layer=layer["comp"],
                metal_level=1,
            )
        )  # pcomp_contact

    else:

        c_temp = gf.Component("temp_store guard ring")

        pcmp_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    lvpwell.dxsize - (2 * lvpwell_enc_pcmp) - (2 * grw),
                    lvpwell.dysize - (2 * lvpwell_enc_pcmp) - (2 * grw),
                ),
                layer=layer["comp"],
            )
        )
        pcmp_in.dcenter = lvpwell.dcenter

        pcmp_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    lvpwell.dxsize - (2 * lvpwell_enc_pcmp),
                    lvpwell.dysize - (2 * lvpwell_enc_pcmp),
                ),
                layer=layer["comp"],
            )
        )
        pcmp_out.dmove((pcmp_in.dxmin - grw, pcmp_in.dymin - grw))
        pcmp = c.add_ref(
            gf.boolean(
                A=pcmp_out, B=pcmp_in, operation="A-B", layer=layer["comp"],
            )
        )

        pplus_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (pcmp_in.dxmax - pcmp_in.dxmin) - 2 * pp_enc_comp,
                    (pcmp_in.dymax - pcmp_in.dymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        pplus_in.dmove((pcmp_in.dxmin + pp_enc_comp, pcmp_in.dymin + pp_enc_comp,))
        pplus_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (pcmp_out.dxmax - pcmp_out.dxmin) + 2 * pp_enc_comp,
                    (pcmp_out.dymax - pcmp_out.dymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        pplus_out.dmove((pcmp_out.dxmin - pp_enc_comp, pcmp_out.dymin - pp_enc_comp,))
        pplus = c.add_ref(
            gf.boolean(
                A=pplus_out, B=pplus_in, operation="A-B", layer=layer["pplus"]
            )
        )  # pplus

        # generating contacts

        c.add_ref(
            via_generator(
                x_range=(pcmp_in.dxmin + con_size, pcmp_in.dxmax - con_size,),
                y_range=(pcmp_out.dymin, pcmp_in.dymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(pcmp_in.dxmin + con_size, pcmp_in.dxmax - con_size,),
                y_range=(pcmp_in.dymax, pcmp_out.dymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        p_con = c.add_ref(
            via_generator(
                x_range=(pcmp_out.dxmin, pcmp_in.dxmin),
                y_range=(pcmp_in.dymin + con_size, pcmp_in.dymax - con_size,),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        c.add_ref(
            via_generator(
                x_range=(pcmp_in.dxmax, pcmp_out.dxmax),
                y_range=(pcmp_in.dymin + con_size, pcmp_in.dymax - con_size,),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        c.add_ref(
            gf.boolean(
                A=pcmp_out, B=pcmp_in, operation="A-B", layer=layer["metal1"],
            )
        )  # guardring metal1

    # n generation
    ncmp = c.add_ref(
        gf.components.rectangle(
            size=(cw, lvpwell.dysize - (2 * lvpwell_enc_pcmp)), layer=layer["comp"]
        )
    )
    ncmp.dcenter = pcmp.dcenter
    ncmp.dxmax = pcmp.dxmin - comp_spacing

    nplus = c.add_ref(
        gf.components.rectangle(
            size=(ncmp.dxsize + (2 * np_enc_comp), ncmp.dysize + (2 * np_enc_comp),),
            layer=layer["nplus"],
        )
    )
    nplus.dxmin = ncmp.dxmin - np_enc_comp
    nplus.dymin = ncmp.dymin - np_enc_comp

    n_con = c.add_ref(
        via_stack(
            x_range=(ncmp.dxmin, ncmp.dxmax),
            y_range=(ncmp.dymin, ncmp.dymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp contact

    # labels generation
    if lbl == 1:

        # n_label generation
        c.add_label(
            n_lbl,
            position=(
                n_con.dxmin + (n_con.dxsize / 2),
                n_con.dymin + (n_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_lbl,
            position=(
                p_con.dxmin + (p_con.dxsize / 2),
                p_con.dymin + (p_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    dn_rect = c.add_ref(
        gf.components.rectangle(
            size=(
                lvpwell.dxmax - nplus.dxmin + (2 * dn_enc_lvpwell),
                lvpwell.dysize + (2 * dn_enc_lvpwell),
            ),
            layer=layer["dnwell"],
        )
    )

    dn_rect.dxmax = lvpwell.dxmax + dn_enc_lvpwell
    dn_rect.dymin = lvpwell.dymin - dn_enc_lvpwell

    if pcmpgr == 1:

        c_temp_gr = gf.Component("temp_store guard ring")
        rect_pcmpgr_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (dn_rect.dxmax - dn_rect.dxmin) + 2 * pcmpgr_enc_dn,
                    (dn_rect.dymax - dn_rect.dymin) + 2 * pcmpgr_enc_dn,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_in.dmove(
            (dn_rect.dxmin - pcmpgr_enc_dn, dn_rect.dymin - pcmpgr_enc_dn)
        )
        rect_pcmpgr_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) + 2 * pcmp_gr_wid,
                    (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) + 2 * pcmp_gr_wid,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_out.dmove(
            (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
        )
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["comp"],
            )
        )  # guardring Bulk

        psdm_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) - 2 * pp_enc_comp,
                    (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_in.dmove(
            (rect_pcmpgr_in.dxmin + pp_enc_comp, rect_pcmpgr_in.dymin + pp_enc_comp,)
        )
        psdm_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_out.dxmax - rect_pcmpgr_out.dxmin) + 2 * pp_enc_comp,
                    (rect_pcmpgr_out.dymax - rect_pcmpgr_out.dymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_out.dmove(
            (rect_pcmpgr_out.dxmin - pp_enc_comp, rect_pcmpgr_out.dymin - pp_enc_comp,)
        )
        c.add_ref(
            gf.boolean(
                A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"]
            )
        )  # guardring psdm

        # generating contacts

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.dxmin + con_size,
                    rect_pcmpgr_in.dxmax - con_size,
                ),
                y_range=(rect_pcmpgr_out.dymin, rect_pcmpgr_in.dymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.dxmin + con_size,
                    rect_pcmpgr_in.dxmax - con_size,
                ),
                y_range=(rect_pcmpgr_in.dymax, rect_pcmpgr_out.dymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_out.dxmin, rect_pcmpgr_in.dxmin),
                y_range=(
                    rect_pcmpgr_in.dymin + con_size,
                    rect_pcmpgr_in.dymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_in.dxmax, rect_pcmpgr_out.dxmax),
                y_range=(
                    rect_pcmpgr_in.dymin + con_size,
                    rect_pcmpgr_in.dymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        comp_m1_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(rect_pcmpgr_in.dxsize, rect_pcmpgr_in.dysize),
                layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (comp_m1_in.dxsize) + 2 * pcmp_gr_wid,
                    (comp_m1_in.dysize) + 2 * pcmp_gr_wid,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.dmove(
            (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
        )
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["metal1"],
            )
        )  # guardring metal1

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    dn_rect.dxsize + (2 * dg_enc_dn),
                    dn_rect.dysize + (2 * dg_enc_dn),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.dxmin = dn_rect.dxmin - dg_enc_dn
        dg.dymin = dn_rect.dymin - dg_enc_dn

    # creating layout and cell in klayout

    c.write_gds("diode_pw2dw_temp.gds")
    layout.read("diode_pw2dw_temp.gds")
    os.remove("diode_pw2dw_temp.gds")

    return layout.cell(c.name)


def draw_diode_dw2ps(
    layout,
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    pcmpgr: bool = 0,
    lbl: bool = 0,
    p_lbl: str = "",
    n_lbl: str = "",
) -> gf.Component:
    """
    Usage:-
     used to draw LVPWELL/DNWELL diode by specifying parameters
    Arguments:-
     layout     : Object of layout
     la         : Float of diff length (anode)
     wa         : Float of diff width (anode)
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
    """

    c = gf.Component("diode_dw2ps_dev")

    if volt == "5/6V":
        dn_enc_ncmp = 0.66
    else:
        dn_enc_ncmp = 0.62

    comp_spacing = 0.92
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    dg_enc_dn = 0.5

    pcmpgr_enc_dn = 2.5
    pcmp_gr_wid = 0.36

    dn_rect = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["dnwell"],))

    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(dn_rect.dxsize, dn_rect.dysize), layer=layer["well_diode_mk"]
        )
    )
    diode_mk.dxmin = dn_rect.dxmin
    diode_mk.dymin = dn_rect.dymin

    if (wa < ((2 * cw) + comp_spacing + (2 * dn_enc_ncmp))) or (
        la < ((2 * cw) + comp_spacing + (2 * dn_enc_ncmp))
    ):
        ncmp = c.add_ref(
            gf.components.rectangle(
                size=(cw, la - (2 * dn_enc_ncmp)), layer=layer["comp"]
            )
        )
        ncmp.dcenter = dn_rect.dcenter

        n_con = c.add_ref(
            via_stack(
                x_range=(ncmp.dxmin, ncmp.dxmax),
                y_range=(ncmp.dymin, ncmp.dymax),
                base_layer=layer["comp"],
                metal_level=1,
            )
        )  # ncomp_contact

        nplus = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.dxsize + (2 * np_enc_comp),
                    ncmp.dysize + (2 * np_enc_comp),
                ),
                layer=layer["nplus"],
            )
        )
        nplus.dxmin = ncmp.dxmin - np_enc_comp
        nplus.dymin = ncmp.dymin - np_enc_comp
    else:
        c_temp = gf.Component("temp_store guard ring")
        ncmp_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    wa - (2 * dn_enc_ncmp) - (2 * cw),
                    la - (2 * dn_enc_ncmp) - (2 * cw),
                ),
                layer=layer["comp"],
            )
        )
        ncmp_in.dcenter = dn_rect.dcenter
        ncmp_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(wa - (2 * dn_enc_ncmp), la - (2 * dn_enc_ncmp)),
                layer=layer["comp"],
            )
        )
        ncmp_out.dmove((ncmp_in.dxmin - cw, ncmp_in.dymin - cw))
        ncmp = c.add_ref(
            gf.boolean(
                A=ncmp_out, B=ncmp_in, operation="A-B", layer=layer["comp"],
            )
        )

        nplus_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (ncmp_in.dxmax - ncmp_in.dxmin) - 2 * pp_enc_comp,
                    (ncmp_in.dymax - ncmp_in.dymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        nplus_in.dmove((ncmp_in.dxmin + pp_enc_comp, ncmp_in.dymin + pp_enc_comp,))
        nplus_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (ncmp_out.dxmax - ncmp_out.dxmin) + 2 * pp_enc_comp,
                    (ncmp_out.dymax - ncmp_out.dymin) + 2 * pp_enc_comp,
                ),
                layer=layer["nplus"],
            )
        )
        nplus_out.dmove((ncmp_out.dxmin - pp_enc_comp, ncmp_out.dymin - pp_enc_comp,))
        nplus = c.add_ref(
            gf.boolean(
                A=nplus_out, B=nplus_in, operation="A-B", layer=layer["nplus"]
            )
        )  # nplus

        # generating contacts

        c.add_ref(
            via_generator(
                x_range=(ncmp_in.dxmin + con_size, ncmp_in.dxmax - con_size,),
                y_range=(ncmp_out.dymin, ncmp_in.dymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(ncmp_in.dxmin + con_size, ncmp_in.dxmax - con_size,),
                y_range=(ncmp_in.dymax, ncmp_out.dymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        n_con = c.add_ref(
            via_generator(
                x_range=(ncmp_out.dxmin, ncmp_in.dxmin),
                y_range=(ncmp_in.dymin + con_size, ncmp_in.dymax - con_size,),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        c.add_ref(
            via_generator(
                x_range=(ncmp_in.dxmax, ncmp_out.dxmax),
                y_range=(ncmp_in.dymin + con_size, ncmp_in.dymax - con_size,),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        comp_m1_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(ncmp_in.dxsize, ncmp_in.dysize), layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp.add_ref(
            gf.components.rectangle(
                size=((comp_m1_in.dxsize) + 2 * cw, (comp_m1_in.dxsize) + 2 * cw,),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.dmove((ncmp_in.dxmin - cw, ncmp_in.dymin - cw))
        c.add_ref(
            gf.boolean(
                A=ncmp_out, B=ncmp_in, operation="A-B", layer=layer["metal1"],
            )
        )  # guardring metal1

    # labels generation
    if lbl == 1:

        # n_label generation
        c.add_label(
            n_lbl,
            position=(
                n_con.dxmin + (n_con.dxsize / 2),
                n_con.dymin + (n_con.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    # generate dnwell

    if pcmpgr == 1:

        c_temp_gr = gf.Component("temp_store guard ring")
        rect_pcmpgr_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (dn_rect.dxmax - dn_rect.dxmin) + 2 * pcmpgr_enc_dn,
                    (dn_rect.dymax - dn_rect.dymin) + 2 * pcmpgr_enc_dn,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_in.dmove(
            (dn_rect.dxmin - pcmpgr_enc_dn, dn_rect.dymin - pcmpgr_enc_dn)
        )
        rect_pcmpgr_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) + 2 * pcmp_gr_wid,
                    (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) + 2 * pcmp_gr_wid,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_out.dmove(
            (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
        )
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["comp"],
            )
        )  # guardring Bulk

        psdm_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) - 2 * pp_enc_comp,
                    (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_in.dmove(
            (rect_pcmpgr_in.dxmin + pp_enc_comp, rect_pcmpgr_in.dymin + pp_enc_comp,)
        )
        psdm_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_out.dxmax - rect_pcmpgr_out.dxmin) + 2 * pp_enc_comp,
                    (rect_pcmpgr_out.dymax - rect_pcmpgr_out.dymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_out.dmove(
            (rect_pcmpgr_out.dxmin - pp_enc_comp, rect_pcmpgr_out.dymin - pp_enc_comp,)
        )
        c.add_ref(
            gf.boolean(
                A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"]
            )
        )  # psdm

        # generating contacts

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.dxmin + con_size,
                    rect_pcmpgr_in.dxmax - con_size,
                ),
                y_range=(rect_pcmpgr_out.dymin, rect_pcmpgr_in.dymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.dxmin + con_size,
                    rect_pcmpgr_in.dxmax - con_size,
                ),
                y_range=(rect_pcmpgr_in.dymax, rect_pcmpgr_out.dymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        p_con = c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_out.dxmin, rect_pcmpgr_in.dxmin),
                y_range=(
                    rect_pcmpgr_in.dymin + con_size,
                    rect_pcmpgr_in.dymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_in.dxmax, rect_pcmpgr_out.dxmax),
                y_range=(
                    rect_pcmpgr_in.dymin + con_size,
                    rect_pcmpgr_in.dymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        # labels generation
        if lbl == 1:

            # n_label generation
            c.add_label(
                p_lbl,
                position=(
                    p_con.dxmin + (p_con.dxsize / 2),
                    p_con.dymin + (p_con.dysize / 2),
                ),
                layer=layer["metal1_label"],
            )

        comp_m1_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(rect_pcmpgr_in.dxsize, rect_pcmpgr_in.dysize),
                layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) + 2 * pcmp_gr_wid,
                    (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) + 2 * pcmp_gr_wid,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.dmove(
            (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
        )
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["metal1"],
            )
        )  # guardring metal1

    # generate dualgate

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    dn_rect.dxsize + (2 * dg_enc_dn),
                    dn_rect.dysize + (2 * dg_enc_dn),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.dxmin = dn_rect.dxmin - dg_enc_dn
        dg.dymin = dn_rect.dymin - dg_enc_dn

    # creating layout and cell in klayout

    c.write_gds("diode_dw2ps_temp.gds")
    layout.read("diode_dw2ps_temp.gds")
    os.remove("diode_dw2ps_temp.gds")

    return layout.cell(c.name)


def draw_sc_diode(
    layout,
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    m: int = 1,
    pcmpgr: bool = 0,
    lbl: bool = 0,
    p_lbl: str = "",
    n_lbl: str = "",
) -> gf.Component:
    """
    Usage:-
     used to draw N+/LVPWELL diode (Outside DNWELL) by specifying parameters
    Arguments:-
     layout     : Object of layout
     la         : Float of diff length (anode)
     wa         : Float of diff width (anode)
     m          : Integer of number of fingers
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    """

    c = gf.Component("sc_diode_dev")

    sc_enc_comp = 0.16
    sc_comp_spacing = 0.28
    dn_enc_sc_an = 1.4
    np_enc_comp = 0.03
    m1_w = 0.23
    pcmpgr_enc_dn = 2.5
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07
    pcmp_gr_wid = 0.36

    # cathode draw

    @gf.cell
    def sc_cathode_strap(size: Float2 = (0.1, 0.1)) -> gf.Component:
        """Returns sc_diode cathode array element

        Args :
            size : size of cathode array element
        """

        c = gf.Component()

        ncmp = c.add_ref(gf.components.rectangle(size=size, layer=layer["comp"]))

        nplus = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.dxsize + (2 * np_enc_comp),
                    ncmp.dysize + (2 * np_enc_comp),
                ),
                layer=layer["nplus"],
            )
        )
        nplus.dxmin = ncmp.dxmin - np_enc_comp
        nplus.dymin = ncmp.dymin - np_enc_comp

        c.add_ref(
            via_stack(
                x_range=(ncmp.dxmin, ncmp.dxmax),
                y_range=(ncmp.dymin, ncmp.dymax),
                base_layer=layer["comp"],
                metal_level=1,
            )
        )  # ncomp contact

        return c

    @gf.cell
    def sc_anode_strap(size: Float2 = (0.1, 0.1)) -> gf.Component:
        """Returns sc_diode anode array element

        Args :
            size : size of anode array element
        """

        c = gf.Component()

        cmp = c.add_ref(gf.components.rectangle(size=size, layer=layer["comp"]))

        c.add_ref(
            via_stack(
                x_range=(cmp.dxmin, cmp.dxmax),
                y_range=(cmp.dymin, cmp.dymax),
                base_layer=layer["comp"],
                metal_level=1,
            )
        )  # comp contact

        return c

    sc_an = sc_anode_strap(size=(wa, la))
    sc_cath = sc_cathode_strap(size=(cw, la))

    sc_cathode = c.add_array(
        component=sc_cath,
        rows=1,
        columns=(m + 1),
        spacing=((cw + wa + (2 * sc_comp_spacing)), 0),
    )

    cath_m1_xmin = sc_cathode.dxmin
    cath_m1_ymin = sc_cathode.dymin
    cath_m1_xmax = sc_cathode.dxmax

    cath_m1_v = c.add_array(
        component=gf.components.rectangle(
            size=(
                cath_m1_xmax - cath_m1_xmin,
                cath_m1_ymin - sc_cathode.dymin + m1_w + 0.001,
            ),
            layer=layer["metal1"],
        ),
        rows=1,
        columns=(m + 1),
        spacing=((cw + wa + (2 * sc_comp_spacing)), 0),
    )

    cath_m1_v.dxmin = cath_m1_xmin
    cath_m1_v.dymax = cath_m1_ymin + 0.001

    cath_m1_h = c.add_ref(
        gf.components.rectangle(size=(cath_m1_v.dxsize, m1_w), layer=layer["metal1"])
    )
    cath_m1_h.dxmin = cath_m1_v.dxmin
    cath_m1_h.dymax = cath_m1_v.dymin

    # cathode label generation
    if lbl == 1:
        c.add_label(
            n_lbl,
            position=(
                cath_m1_h.dxmin + (cath_m1_h.dxsize / 2),
                cath_m1_h.dymin + (cath_m1_h.dysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    sc_anode = c.add_array(
        component=sc_an,
        rows=1,
        columns=m,
        spacing=(wa + cw + (2 * sc_comp_spacing), 0),
    )

    sc_anode.dxmin = sc_cathode.dxmin + (cw + sc_comp_spacing + np_enc_comp)

    an_m1_xmin = sc_anode.dxmin
    an_m1_ymin = sc_anode.dymin
    an_m1_xmax = sc_anode.dxmax
    an_m1_ymax = sc_anode.dymax

    if m > 1:

        an_m1_v = c.add_array(
            component=gf.components.rectangle(
                size=(
                    an_m1_xmax - an_m1_xmin,
                    cath_m1_ymin - sc_an.dymin + m1_w + 0.001,
                ),
                layer=layer["metal1"],
            ),
            rows=1,
            columns=m,
            spacing=((cw + wa + (2 * sc_comp_spacing)), 0),
        )

        an_m1_v.dxmin = an_m1_xmin
        an_m1_v.dymin = an_m1_ymax

        an_m1_h = c.add_ref(
            gf.components.rectangle(size=(an_m1_v.dxsize, m1_w), layer=layer["metal1"])
        )
        an_m1_h.dxmin = an_m1_v.dxmin
        an_m1_h.dymin = an_m1_v.dymax - 0.001

        # anode label generation
        if lbl == 1:
            c.add_label(
                p_lbl,
                position=(
                    an_m1_h.dxmin + (an_m1_h.dxsize / 2),
                    an_m1_h.dymin + (an_m1_h.dysize / 2),
                ),
                layer=layer["metal1_label"],
            )

    else:

        # anode label generation
        if lbl == 1:
            c.add_label(
                p_lbl,
                position=(
                    an_m1_xmin + ((an_m1_xmax - an_m1_xmin) / 2),
                    an_m1_ymin + ((an_m1_ymax - an_m1_ymin) / 2),
                ),
                layer=layer["metal1_label"],
            )

    # diode_mk
    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(
                sc_cathode.dxsize + (2 * sc_enc_comp),
                sc_cathode.dysize + (2 * sc_enc_comp),
            ),
            layer=layer["schottky_diode"],
        )
    )
    diode_mk.dxmin = sc_cathode.dxmin - sc_enc_comp
    diode_mk.dymin = sc_cathode.dymin - sc_enc_comp

    # dnwell
    dn_rect = c.add_ref(
        gf.components.rectangle(
            size=(
                sc_cathode.dxsize + (2 * dn_enc_sc_an),
                sc_anode.dysize + (2 * dn_enc_sc_an),
            ),
            layer=layer["dnwell"],
        )
    )
    dn_rect.dxmin = sc_cathode.dxmin - dn_enc_sc_an
    dn_rect.dymin = sc_anode.dymin - dn_enc_sc_an

    if pcmpgr == 1:

        c_temp_gr = gf.Component("temp_store guard ring")
        rect_pcmpgr_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (dn_rect.dxmax - dn_rect.dxmin) + 2 * pcmpgr_enc_dn,
                    (dn_rect.dymax - dn_rect.dymin) + 2 * pcmpgr_enc_dn,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_in.dmove(
            (dn_rect.dxmin - pcmpgr_enc_dn, dn_rect.dymin - pcmpgr_enc_dn)
        )
        rect_pcmpgr_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) + 2 * pcmp_gr_wid,
                    (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) + 2 * pcmp_gr_wid,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_out.dmove(
            (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
        )
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["comp"],
            )
        )  # guardring Bulk

        psdm_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.dxmax - rect_pcmpgr_in.dxmin) - 2 * pp_enc_comp,
                    (rect_pcmpgr_in.dymax - rect_pcmpgr_in.dymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_in.dmove(
            (rect_pcmpgr_in.dxmin + pp_enc_comp, rect_pcmpgr_in.dymin + pp_enc_comp,)
        )
        psdm_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_out.dxmax - rect_pcmpgr_out.dxmin) + 2 * pp_enc_comp,
                    (rect_pcmpgr_out.dymax - rect_pcmpgr_out.dymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_out.dmove(
            (rect_pcmpgr_out.dxmin - pp_enc_comp, rect_pcmpgr_out.dymin - pp_enc_comp,)
        )
        c.add_ref(
            gf.boolean(
                A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"]
            )
        )  # psdm

        # generating contacts

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.dxmin + con_size,
                    rect_pcmpgr_in.dxmax - con_size,
                ),
                y_range=(rect_pcmpgr_out.dymin, rect_pcmpgr_in.dymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.dxmin + con_size,
                    rect_pcmpgr_in.dxmax - con_size,
                ),
                y_range=(rect_pcmpgr_in.dymax, rect_pcmpgr_out.dymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_out.dxmin, rect_pcmpgr_in.dxmin),
                y_range=(
                    rect_pcmpgr_in.dymin + con_size,
                    rect_pcmpgr_in.dymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_in.dxmax, rect_pcmpgr_out.dxmax),
                y_range=(
                    rect_pcmpgr_in.dymin + con_size,
                    rect_pcmpgr_in.dymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        comp_m1_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(rect_pcmpgr_in.dxsize, rect_pcmpgr_in.dysize),
                layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (comp_m1_in.dxsize) + 2 * pcmp_gr_wid,
                    (comp_m1_in.dysize) + 2 * pcmp_gr_wid,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.dmove(
            (rect_pcmpgr_in.dxmin - pcmp_gr_wid, rect_pcmpgr_in.dymin - pcmp_gr_wid)
        )
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["metal1"],
            )
        )  # guardring metal1

    # creating layout and cell in klayout

    c.write_gds("sc_diode_temp.gds")
    layout.read("sc_diode_temp.gds")
    os.remove("sc_diode_temp.gds")

    return layout.cell(c.name)
