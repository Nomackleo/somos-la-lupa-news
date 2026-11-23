#!/usr/bin/env python3
"""
Generador Oficial Word (.docx) para:
CUENTA DE COBRO No. CC-2026-LLN-002
Presentación Interactiva Ejecutiva (Pitch Comercial y para Inversores)
Portal Somos La Lupa News (somoslalupanews.com)

Autor Corporativo: Leonel Salcedo — Dirección y Consultoría Tecnológica (Marca Personal)
Paleta y Estética Oficial alineadas al Manual Documental de La Lupa News y al documento
maestro COTIZACION_ACTUALIZACION_SEGURIDAD_SOMOSLALUPANEWS:
- Morado Marca Personal (#2d124d) + Dorado Institucional (#b8842a) + Superficie Suave (#f5f7fa).
Cumplimiento Normativa Tributaria y Comercial de la República de Colombia.
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# =============================================================================
# PALETA OFICIAL MARCA PERSONAL LEONEL SALCEDO — LA LUPA NEWS
# (Verificada contra GEMINI.md + COTIZACION_ACTUALIZACION_SEGURIDAD_SOMOSLALUPANEWS)
# =============================================================================
MORADO_PRIMARY = RGBColor(0x2D, 0x12, 0x4D)    # #2d124d (Morado Principal)
MORADO_DEEP = RGBColor(0x22, 0x0D, 0x3A)       # #220d3a (Morado Profundo)
DORADO_ACCENT = RGBColor(0xB8, 0x84, 0x2A)     # #b8842a (Dorado Institucional)
NEGRO_CARGO = RGBColor(0x11, 0x11, 0x11)       # #111111 (Cargo portada)
GRIS_TEXTO = RGBColor(0x22, 0x22, 0x22)        # #222222 (Cuerpo de texto)
GRIS_SUBTITLE = RGBColor(0x66, 0x66, 0x66)     # #666666 (Subtítulo portada)
GRIS_META = RGBColor(0x77, 0x77, 0x77)         # #777777 (Headers, footers, metadatos)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

HEX_MORADO = "2D124D"
HEX_DORADO = "B8842A"
HEX_GRIS_LINEA = "CCCCCC"
HEX_SURFACE = "F5F7FA"       # Fondo suave oficial de celdas/callouts (ref. Google Doc)
HEX_GOLD_BG = "FDFBF7"       # Fondo destacado dorado suave para bloque de valor


def set_cell_background(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=80, bottom=80, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def add_paragraph_border(p, side="bottom", hex_color=HEX_DORADO, sz="8", space="4"):
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:{side} w:val="single" w:sz="{sz}" w:space="{space}" w:color="{hex_color}"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)


def set_paragraph_shading(p, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{hex_color}"/>')
    p._p.get_or_add_pPr().append(shd)


def add_table_borders(table, hex_color="D8DCE3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{HEX_MORADO}"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_DORADO}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)


def format_cell_text(
    cell,
    text,
    bold=False,
    italic=False,
    color=GRIS_TEXTO,
    size_pt=9.5,
    align=WD_ALIGN_PARAGRAPH.LEFT,
    font_name="Cambria",
):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.12
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return run


def add_section_heading(doc, number_str, title_str):
    """Título de sección: Número en Dorado (#b8842a), Título en Morado (#2d124d), filete inferior Dorado."""
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True

    r_num = h.add_run(f"{number_str}. ")
    r_num.font.name = "Calibri"
    r_num.font.size = Pt(13.5)
    r_num.font.bold = True
    r_num.font.color.rgb = DORADO_ACCENT

    r_txt = h.add_run(title_str)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(13.5)
    r_txt.font.bold = True
    r_txt.font.color.rgb = MORADO_PRIMARY

    add_paragraph_border(h, side="bottom", hex_color=HEX_DORADO, sz="8", space="3")
    return h


def add_subsection_heading(doc, title_str):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(title_str)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = MORADO_PRIMARY
    return h


def add_body_paragraph(doc, text, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.font.name = "Cambria"
    r.font.size = Pt(11)
    r.font.color.rgb = GRIS_TEXTO
    return p


def add_kv_table(doc, rows_data, bold_value_indices=None, col_widths=(2.35, 4.15)):
    """Tabla llave-valor alineada al estilo del documento maestro (#F5F7FA en columna izquierda, blanco en valor)."""
    bold_value_indices = set(bold_value_indices or [])
    table = doc.add_table(rows=len(rows_data), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    add_table_borders(table)

    for r_idx, (k, v) in enumerate(rows_data):
        row = table.rows[r_idx]
        row.cells[0].width = Inches(col_widths[0])
        row.cells[1].width = Inches(col_widths[1])

        set_cell_background(row.cells[0], HEX_SURFACE)
        set_cell_background(row.cells[1], "FFFFFF")
        set_cell_margins(row.cells[0], top=65, bottom=65, left=100, right=100)
        set_cell_margins(row.cells[1], top=65, bottom=65, left=100, right=100)

        format_cell_text(
            row.cells[0],
            k,
            bold=True,
            color=MORADO_PRIMARY,
            size_pt=9.5,
            font_name="Calibri",
        )
        format_cell_text(
            row.cells[1],
            v,
            bold=(r_idx in bold_value_indices),
            color=GRIS_TEXTO,
            size_pt=9.5,
            font_name="Cambria",
        )
    return table


def create_cuenta_de_cobro_docx():
    doc = Document()

    # Configuración de página Carta, márgenes 1 pulgada, Different First Page = True
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.different_first_page_header_footer = True

    # =========================================================================
    # ENCABEZADO Y PIE DE PÁGINA EN PÁGINAS INTERIORES (PÁG. 2 EN ADELANTE)
    # (Espejo exacto de COTIZACION_ACTUALIZACION_SEGURIDAD_SOMOSLALUPANEWS)
    # =========================================================================
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.paragraph_format.space_after = Pt(4)
    p_hdr.paragraph_format.line_spacing = 1.1
    r_hdr_text = p_hdr.add_run(
        "LA LUPA NEWS | Cuenta de Cobro No. CC-2026-LLN-002\n"
        "Confidencial — Uso Exclusivo de Dirección General"
    )
    r_hdr_text.font.name = "Calibri"
    r_hdr_text.font.size = Pt(8.5)
    r_hdr_text.font.color.rgb = GRIS_META
    add_paragraph_border(p_hdr, side="bottom", hex_color=HEX_DORADO, sz="6", space="3")

    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_ftr.paragraph_format.space_before = Pt(4)
    r_ftr_text = p_ftr.add_run(
        "Leonel Salcedo — Dirección y Consultoría Tecnológica | Confidencial — La Lupa News"
    )
    r_ftr_text.font.name = "Calibri"
    r_ftr_text.font.size = Pt(8.5)
    r_ftr_text.font.color.rgb = GRIS_META
    add_paragraph_border(p_ftr, side="top", hex_color=HEX_GRIS_LINEA, sz="4", space="3")

    # =========================================================================
    # PORTADA INSTITUCIONAL DE 9 NIVELES (CENTRADA VERTICAL Y HORIZONTALMENTE)
    # =========================================================================
    p_top_spacer = doc.add_paragraph()
    p_top_spacer.paragraph_format.space_before = Pt(68)

    # Nivel 1: Top Header — Calibri 8.5 pt Bold, Mayúsculas, Dorado #b8842a
    p_n1 = doc.add_paragraph()
    p_n1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n1.paragraph_format.space_after = Pt(10)
    r_n1 = p_n1.add_run("LA LUPA NEWS — ESTRATEGIA DIGITAL Y TECNOLOGÍA")
    r_n1.font.name = "Calibri"
    r_n1.font.size = Pt(8.5)
    r_n1.font.bold = True
    r_n1.font.color.rgb = DORADO_ACCENT

    # Nivel 2: Subtítulo Superior — Calibri 11 pt Bold, Morado #2d124d
    p_n2 = doc.add_paragraph()
    p_n2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n2.paragraph_format.space_after = Pt(14)
    r_n2 = p_n2.add_run("DOCUMENTO SOPORTE DE COBRO — CONSULTORÍA Y DESARROLLO INTERACTIVO")
    r_n2.font.name = "Calibri"
    r_n2.font.size = Pt(11)
    r_n2.font.bold = True
    r_n2.font.color.rgb = MORADO_PRIMARY

    # Nivel 3: Título Principal (H1) — Calibri 22 pt Bold, Morado #2d124d + línea dorada
    p_n3 = doc.add_paragraph()
    p_n3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n3.paragraph_format.space_after = Pt(16)
    p_n3.paragraph_format.line_spacing = 1.15
    r_n3 = p_n3.add_run("CUENTA DE COBRO\nNo. CC-2026-LLN-002")
    r_n3.font.name = "Calibri"
    r_n3.font.size = Pt(22)
    r_n3.font.bold = True
    r_n3.font.color.rgb = MORADO_PRIMARY
    add_paragraph_border(p_n3, side="bottom", hex_color=HEX_DORADO, sz="12", space="10")

    # Nivel 4: Espaciador Vertical Amplio
    p_n4 = doc.add_paragraph()
    p_n4.paragraph_format.space_before = Pt(34)
    p_n4.paragraph_format.space_after = Pt(10)

    # Nivel 5: Nombre del Proyecto / Subtítulo — Calibri 14 pt Italic, Gris #666666
    p_n5 = doc.add_paragraph()
    p_n5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n5.paragraph_format.space_after = Pt(40)
    p_n5.paragraph_format.line_spacing = 1.2
    r_n5 = p_n5.add_run(
        "Presentación Interactiva Ejecutiva (Pitch Comercial y para Inversores)\n"
        "Portal Digital somoslalupanews.com"
    )
    r_n5.font.name = "Calibri"
    r_n5.font.size = Pt(14)
    r_n5.font.italic = True
    r_n5.font.color.rgb = GRIS_SUBTITLE

    # Nivel 6: Etiqueta "PRESENTADO A" — Calibri 10 pt Bold, Dorado #b8842a
    p_n6 = doc.add_paragraph()
    p_n6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n6.paragraph_format.space_after = Pt(6)
    r_n6 = p_n6.add_run("PRESENTADO A:")
    r_n6.font.name = "Calibri"
    r_n6.font.size = Pt(10)
    r_n6.font.bold = True
    r_n6.font.color.rgb = DORADO_ACCENT

    # Nivel 7: Destinatario Principal (H2) — Calibri 18 pt Bold Morado + Cargo Calibri 12 pt #111111
    p_n7 = doc.add_paragraph()
    p_n7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n7.paragraph_format.space_after = Pt(4)
    r_n7 = p_n7.add_run("JAVIER FERNÁNDEZ FRANCO")
    r_n7.font.name = "Calibri"
    r_n7.font.size = Pt(18)
    r_n7.font.bold = True
    r_n7.font.color.rgb = MORADO_PRIMARY

    p_n7_cargo = doc.add_paragraph()
    p_n7_cargo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n7_cargo.paragraph_format.space_after = Pt(60)
    r_n7_c = p_n7_cargo.add_run("CEO & Representante Legal — La Lupa News")
    r_n7_c.font.name = "Calibri"
    r_n7_c.font.size = Pt(12)
    r_n7_c.font.color.rgb = NEGRO_CARGO

    # Nivel 8: Metadatos de Autoría y Fecha — Calibri 10 pt centrado con línea dorada superior
    p_n8 = doc.add_paragraph()
    p_n8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_n8.paragraph_format.line_spacing = 1.25
    add_paragraph_border(p_n8, side="top", hex_color=HEX_DORADO, sz="6", space="8")

    r_m1 = p_n8.add_run("Presentado por: ")
    r_m1.font.name = "Calibri"
    r_m1.font.size = Pt(10)
    r_m1.font.bold = True
    r_m1.font.color.rgb = DORADO_ACCENT

    r_m2 = p_n8.add_run("Leonel Salcedo | Dirección y Consultoría Tecnológica\n")
    r_m2.font.name = "Calibri"
    r_m2.font.size = Pt(10)
    r_m2.font.bold = True
    r_m2.font.color.rgb = MORADO_PRIMARY

    r_m3 = p_n8.add_run("Acreedor: Leonel Antonio Salcedo Acosta — C.C. 1.022.943.003 de Bogotá\n")
    r_m3.font.name = "Calibri"
    r_m3.font.size = Pt(9.5)
    r_m3.font.color.rgb = GRIS_META

    r_m4 = p_n8.add_run("Fecha de Emisión: 19 de Noviembre de 2026 | Estado: Versión Oficial Aprobada")
    r_m4.font.name = "Calibri"
    r_m4.font.size = Pt(9.5)
    r_m4.font.color.rgb = GRIS_META

    # Nivel 9: Salto de página hacia contenido interior
    doc.add_page_break()

    # =========================================================================
    # CALLOUT MARCO LEGAL COLOMBIANO (Estilo caja #F5F7FA del documento maestro)
    # =========================================================================
    p_marco = doc.add_paragraph()
    p_marco.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_marco.paragraph_format.left_indent = Inches(0.12)
    p_marco.paragraph_format.space_before = Pt(4)
    p_marco.paragraph_format.space_after = Pt(10)
    p_marco.paragraph_format.line_spacing = 1.15
    add_paragraph_border(p_marco, side="left", hex_color=HEX_DORADO, sz="24", space="8")
    set_paragraph_shading(p_marco, HEX_SURFACE)

    r_mc1 = p_marco.add_run("DOCUMENTO SOPORTE DE COBRO — PERSONA NATURAL NO OBLIGADA A FACTURAR\n")
    r_mc1.font.name = "Calibri"
    r_mc1.font.size = Pt(10)
    r_mc1.font.bold = True
    r_mc1.font.color.rgb = MORADO_PRIMARY

    r_mc2 = p_marco.add_run(
        "Expedido en Bogotá D.C., Colombia, el 19 de noviembre de 2026, bajo la gravedad de juramento y en "
        "estricto cumplimiento del Estatuto Tributario Nacional (Artículos 616-1, 616-2, 437 Parágrafo 3, "
        "383 y 388), el Decreto 1625 de 2016, la Resolución DIAN 000167 de 2021, la Ley 1393 de 2010 y la "
        "Ley 1955 de 2019."
    )
    r_mc2.font.name = "Cambria"
    r_mc2.font.size = Pt(9.5)
    r_mc2.font.color.rgb = GRIS_TEXTO

    # =========================================================================
    # 1. IDENTIFICACIÓN DE LAS PARTES
    # =========================================================================
    add_section_heading(doc, "1", "Identificación de las Partes")

    add_subsection_heading(doc, "1.1. Datos del Deudor (Cliente / Contratante)")
    deudor_rows = [
        ("Nombre Completo / Titular", "JAVIER FERNÁNDEZ FRANCO"),
        ("Cargo y Medio Digital", "CEO & Representante Legal — La Lupa News (somoslalupanews.com)"),
        ("Domicilio y Sede Editorial", "Calle 127 #16A-76, oficina 402, Bogotá D.C., Colombia"),
        ("Correo Directo del Titular", "elcantantedelgolnumero1@gmail.com"),
        ("Correos Institucionales", "lalupanewsco@gmail.com · somoslalupanews@gmail.com"),
    ]
    add_kv_table(doc, deudor_rows, bold_value_indices={0})

    add_subsection_heading(doc, "1.2. Datos del Acreedor (Consultor / Contratista Independiente)")
    acreedor_rows = [
        ("Nombre Completo", "LEONEL ANTONIO SALCEDO ACOSTA"),
        ("Cédula de Ciudadanía / NIT", "1.022.943.003 (1022943003) de Bogotá D.C."),
        ("Régimen Tributario", "Persona Natural — No Responsable del IVA (Art. 437 Par. 3 E.T.)"),
        ("Calidad Jurídica", "Contratista Independiente — Titular Exclusivo del Cobro"),
        ("Domicilio Fiscal", "Bogotá D.C., Colombia"),
        ("Teléfono Celular", "322 373 6685"),
        ("Correos de Notificación", "nomack3d@gmail.com / nomackleo@gmail.com"),
    ]
    add_kv_table(doc, acreedor_rows, bold_value_indices={0, 1})

    # =========================================================================
    # 2. DECLARACIÓN DE OBLIGACIÓN Y VALOR TOTAL A CANCELAR
    # =========================================================================
    add_section_heading(doc, "2", "Declaración de Obligación y Monto a Cancelar")

    p_debe = doc.add_paragraph()
    p_debe.paragraph_format.space_before = Pt(4)
    p_debe.paragraph_format.space_after = Pt(8)

    r_d1 = p_debe.add_run("JAVIER FERNÁNDEZ FRANCO (LA LUPA NEWS) ")
    r_d1.font.name = "Calibri"
    r_d1.font.size = Pt(11)
    r_d1.font.bold = True
    r_d1.font.color.rgb = MORADO_PRIMARY

    r_d2 = p_debe.add_run("DEBE A: ")
    r_d2.font.name = "Calibri"
    r_d2.font.size = Pt(11)
    r_d2.font.bold = True
    r_d2.font.color.rgb = DORADO_ACCENT

    r_d3 = p_debe.add_run("LEONEL ANTONIO SALCEDO ACOSTA (C.C. 1.022.943.003)")
    r_d3.font.name = "Calibri"
    r_d3.font.size = Pt(11)
    r_d3.font.bold = True
    r_d3.font.color.rgb = MORADO_PRIMARY

    # Caja destacada del monto
    p_monto = doc.add_paragraph()
    p_monto.paragraph_format.left_indent = Inches(0.12)
    p_monto.paragraph_format.space_before = Pt(4)
    p_monto.paragraph_format.space_after = Pt(10)
    p_monto.paragraph_format.line_spacing = 1.2
    add_paragraph_border(p_monto, side="left", hex_color=HEX_MORADO, sz="30", space="10")
    set_paragraph_shading(p_monto, HEX_GOLD_BG)

    r_m1 = p_monto.add_run("VALOR TOTAL EN NÚMEROS: ")
    r_m1.font.name = "Calibri"
    r_m1.font.size = Pt(11)
    r_m1.font.bold = True
    r_m1.font.color.rgb = DORADO_ACCENT

    r_m2 = p_monto.add_run("$50.000 COP\n")
    r_m2.font.name = "Calibri"
    r_m2.font.size = Pt(16)
    r_m2.font.bold = True
    r_m2.font.color.rgb = MORADO_PRIMARY

    r_m3 = p_monto.add_run("VALOR EN LETRAS: ")
    r_m3.font.name = "Calibri"
    r_m3.font.size = Pt(10)
    r_m3.font.bold = True
    r_m3.font.color.rgb = MORADO_DEEP

    r_m4 = p_monto.add_run("CINCUENTA MIL PESOS MONEDA CORRIENTE\n")
    r_m4.font.name = "Cambria"
    r_m4.font.size = Pt(10.5)
    r_m4.font.bold = True
    r_m4.font.color.rgb = GRIS_TEXTO

    r_m5 = p_monto.add_run("MODALIDAD: ")
    r_m5.font.name = "Calibri"
    r_m5.font.size = Pt(9.5)
    r_m5.font.bold = True
    r_m5.font.color.rgb = DORADO_ACCENT

    r_m6 = p_monto.add_run("Pago único total — Tarifa especial / preferencial acordada para el proyecto.")
    r_m6.font.name = "Cambria"
    r_m6.font.size = Pt(9.5)
    r_m6.font.italic = True
    r_m6.font.color.rgb = GRIS_SUBTITLE

    # =========================================================================
    # 3. CONCEPTO DEL COBRO Y ALCANCE DEL ENTREGABLE
    # (Tabla con encabezado Morado #2D124D y columna valor #F5F7FA como en el doc maestro)
    # =========================================================================
    add_section_heading(doc, "3", "Concepto del Cobro y Alcance del Entregable")

    add_body_paragraph(
        doc,
        "Honorarios profesionales pactados bajo tarifa especial preferencial por concepto de diseño, "
        "estructuración comercial y desarrollo integral de la Presentación Interactiva Ejecutiva "
        "(Pitch Comercial y para Inversores) del portal informativo Somos La Lupa News "
        "(somoslalupanews.com), conformada por los siguientes componentes:",
    )

    concepto_rows = [
        (
            "Estructuración Comercial y Narrativa Dual",
            "Construcción estratégica del argumento comercial orientado a la venta de pauta digital, "
            "patrocinios directos y atracción de capital de inversión, destacando la propuesta de valor "
            "del portal propio, sus espacios publicitarios y el potencial de reactivación estratégica.",
            "Incluido",
        ),
        (
            "Diseño Visual Ejecutivo y Experiencia Interactiva",
            "Maquetación moderna y de alto impacto alineada con la identidad visual oficial de Somos La "
            "Lupa News, con selector dual (anunciante/inversionista), mapa interactivo de espacios, "
            "simulador de impacto, modo presentación y visualización responsiva escritorio/móvil.",
            "Incluido",
        ),
        (
            "Archivo HTML Interactivo Autocontenido Final",
            "Compilación en un archivo HTML profesional autocontenido (standalone), portable y listo "
            "para abrirse directamente en cualquier navegador web moderno sin dependencias externas.",
            "$50.000 COP\n(Tarifa Preferencial)",
        ),
    ]

    t_conc = doc.add_table(rows=1 + len(concepto_rows), cols=3)
    t_conc.alignment = WD_TABLE_ALIGNMENT.CENTER
    add_table_borders(t_conc)
    widths_c = [Inches(1.65), Inches(3.55), Inches(1.30)]

    headers_c = ["Componente", "Alcance y Entregables Incluidos", "Valor (COP)"]
    for c_i, h_txt in enumerate(headers_c):
        cell = t_conc.rows[0].cells[c_i]
        cell.width = widths_c[c_i]
        set_cell_background(cell, HEX_MORADO)
        set_cell_margins(cell, top=75, bottom=75, left=85, right=85)
        format_cell_text(
            cell,
            h_txt,
            bold=True,
            color=BLANCO,
            size_pt=9.5,
            align=WD_ALIGN_PARAGRAPH.CENTER if c_i == 2 else WD_ALIGN_PARAGRAPH.LEFT,
            font_name="Calibri",
        )

    for r_i, (comp, desc, val) in enumerate(concepto_rows, start=1):
        row = t_conc.rows[r_i]
        for c_i, width in enumerate(widths_c):
            row.cells[c_i].width = width
            set_cell_margins(row.cells[c_i], top=70, bottom=70, left=85, right=85)
        set_cell_background(row.cells[0], "FFFFFF")
        set_cell_background(row.cells[1], "FFFFFF")
        set_cell_background(row.cells[2], HEX_SURFACE)

        format_cell_text(row.cells[0], comp, bold=True, color=MORADO_PRIMARY, size_pt=9.5, font_name="Calibri")
        format_cell_text(row.cells[1], desc, bold=False, color=GRIS_TEXTO, size_pt=9.2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, font_name="Cambria")
        format_cell_text(
            row.cells[2],
            val,
            bold=(r_i == len(concepto_rows)),
            color=MORADO_PRIMARY if r_i == len(concepto_rows) else GRIS_META,
            size_pt=9.5,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            font_name="Calibri",
        )

    # =========================================================================
    # 4. CONDICIÓN COMERCIAL DE SOCIALIZACIÓN Y ENTREGA DEL ARCHIVO FINAL
    # =========================================================================
    add_section_heading(doc, "4", "Condición Comercial de Socialización y Entrega")

    p_cond = doc.add_paragraph()
    p_cond.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cond.paragraph_format.left_indent = Inches(0.12)
    p_cond.paragraph_format.space_before = Pt(4)
    p_cond.paragraph_format.space_after = Pt(10)
    p_cond.paragraph_format.line_spacing = 1.15
    add_paragraph_border(p_cond, side="left", hex_color=HEX_DORADO, sz="24", space="8")
    set_paragraph_shading(p_cond, HEX_SURFACE)

    r_c1 = p_cond.add_run("PROTOCOLO DE DEMOSTRACIÓN PREVIA Y LIBERACIÓN DEL ARCHIVO FINAL\n")
    r_c1.font.name = "Calibri"
    r_c1.font.size = Pt(10)
    r_c1.font.bold = True
    r_c1.font.color.rgb = MORADO_PRIMARY

    r_c2 = p_cond.add_run(
        "Con el propósito de brindar plena claridad, transparencia y satisfacción ejecutiva para ambas "
        "partes, la presentación interactiva se socializa en demostración previa ante la Dirección General "
        "de La Lupa News para validar su propuesta visual, narrativa comercial y experiencia de navegación. "
        "Una vez confirmado el pago total por valor de "
    )
    r_c2.font.name = "Cambria"
    r_c2.font.size = Pt(10.5)
    r_c2.font.color.rgb = GRIS_TEXTO

    r_c3 = p_cond.add_run("$50.000 COP (Cincuenta Mil Pesos Moneda Corriente)")
    r_c3.font.name = "Cambria"
    r_c3.font.size = Pt(10.5)
    r_c3.font.bold = True
    r_c3.font.color.rgb = MORADO_PRIMARY

    r_c4 = p_cond.add_run(
        " y recibido el respectivo comprobante de transferencia en los correos autorizados "
        "(nomack3d@gmail.com / nomackleo@gmail.com), se realizará de manera "
    )
    r_c4.font.name = "Cambria"
    r_c4.font.size = Pt(10.5)
    r_c4.font.color.rgb = GRIS_TEXTO

    r_c5 = p_cond.add_run("inmediata el envío y liberación oficial del archivo HTML interactivo autocontenido final")
    r_c5.font.name = "Cambria"
    r_c5.font.size = Pt(10.5)
    r_c5.font.bold = True
    r_c5.font.color.rgb = MORADO_PRIMARY

    r_c6 = p_cond.add_run(
        ", listo para su uso comercial directo con marcas anunciantes e inversionistas."
    )
    r_c6.font.name = "Cambria"
    r_c6.font.size = Pt(10.5)
    r_c6.font.color.rgb = GRIS_TEXTO

    # =========================================================================
    # 5. DECLARACIONES JURAMENTADAS DE CARÁCTER TRIBUTARIO Y LEGAL
    # =========================================================================
    add_section_heading(doc, "5", "Declaraciones Juramentadas de Carácter Tributario y Legal")

    juramentos = [
        (
            "5.1. Declaración de No Responsable del IVA (E.T. Art. 437 Parágrafo 3)",
            "Bajo la gravedad de juramento declaro que pertenezco al régimen de No Responsables del "
            "Impuesto sobre las Ventas (IVA) conforme al Parágrafo 3 del Artículo 437 del Estatuto "
            "Tributario Nacional (modificado por las Leyes 1943 de 2018, 2010 de 2019 y 2277 de 2022). "
            "Manifiesto que ni en el año gravable anterior ni en el año en curso he obtenido ingresos "
            "brutos totales provenientes de mi actividad económica superiores a tres mil quinientas (3.500) "
            "UVT, no poseo más de un establecimiento de comercio, oficina o sede donde ejerza mi actividad, "
            "no desarrollo actividades bajo franquicia, concesión, regalía o autorización de explotación, "
            "y no ostento la calidad de usuario aduanero.",
        ),
        (
            "5.2. No Obligado a Expedir Factura Electrónica (E.T. Art. 616-2 y D. 1625/2016)",
            "Manifiesto que, en virtud de mi condición de persona natural no responsable del IVA y de "
            "conformidad con el Artículo 616-2 del Estatuto Tributario Nacional y el Artículo 1.6.1.4.3 "
            "del Decreto 1625 de 2016, no estoy obligado a expedir factura electrónica de venta ni "
            "documento equivalente. En consecuencia, la presente cuenta de cobro reúne los requisitos "
            "legales para que el adquirente, en caso de ser sujeto obligado, elabore el Documento Soporte "
            "Electrónico en Adquisiciones Efectuadas a Sujetos No Obligados a Expedir Factura de Venta "
            "(Resolución DIAN 000167 de 2021 y Artículo 1.6.1.4.12 del Decreto 1625 de 2016).",
        ),
        (
            "5.3. Declaración Juramentada de Retención en la Fuente (E.T. Arts. 383 y 388)",
            "Bajo la gravedad del juramento declaro que durante el año gravable 2026 NO he contratado ni "
            "vinculado a dos (2) o más trabajadores o contratistas asociados a mi actividad económica por "
            "un término igual o superior a noventa (90) días continuos o discontinuos, solicitando en "
            "consecuencia la aplicación de la tabla del Artículo 383 del Estatuto Tributario (modificado "
            "por el Art. 8 de la Ley 2277 de 2022) en concordancia con el Artículo 388 ibídem. Se deja "
            "constancia técnica de que, por tratarse de un monto total de $50.000 COP, el presente cobro "
            "no supera la base mínima legal sujeta a retención en la fuente a título de renta, por lo cual "
            "el valor neto a cancelar corresponde íntegramente a $50.000 COP.",
        ),
        (
            "5.4. Constancia sobre Sistema de Seguridad Social Integral (Ley 1393/2010 y Ley 1955/2019)",
            "En armonía con el Artículo 26 de la Ley 1393 de 2010, la Ley 100 de 1993 y el Artículo 244 "
            "de la Ley 1955 de 2019, se precisa que los honorarios pactados ($50.000 COP) corresponden a "
            "un servicio profesional puntual de cuantía inferior a un (1) Salario Mínimo Mensual Legal "
            "Vigente (SMMLV), por lo que no generan obligación autónoma de liquidación de planilla PILA "
            "específica por esta cuantía, manteniendo el contratista su debida sujeción general a las "
            "normas del Sistema de Seguridad Social Integral.",
        ),
    ]

    for sub_title, jur_text in juramentos:
        p_j = doc.add_paragraph()
        p_j.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_j.paragraph_format.space_before = Pt(3)
        p_j.paragraph_format.space_after = Pt(5)
        p_j.paragraph_format.line_spacing = 1.12

        rj_t = p_j.add_run(sub_title + "\n")
        rj_t.font.name = "Calibri"
        rj_t.font.size = Pt(10)
        rj_t.font.bold = True
        rj_t.font.color.rgb = MORADO_PRIMARY

        rj_b = p_j.add_run(jur_text)
        rj_b.font.name = "Cambria"
        rj_b.font.size = Pt(9.5)
        rj_b.font.color.rgb = GRIS_TEXTO

    # =========================================================================
    # 6. MEDIOS DE PAGO HABILITADOS Y NOTIFICACIÓN DE COMPROBANTE
    # =========================================================================
    add_section_heading(doc, "6", "Medios de Pago Habilitados y Notificación")

    add_body_paragraph(
        doc,
        "Las transferencias deberán efectuarse exclusivamente a nombre del titular oficial. El pago "
        "total por valor de $50.000 COP puede realizarse mediante cualquiera de las siguientes dos (2) "
        "opciones oficiales:",
        space_after=4,
    )

    add_subsection_heading(doc, "Opción 1 — Transferencia Bancaria (Banco Davivienda)")
    davivienda_rows = [
        ("Entidad Financiera", "BANCO DAVIVIENDA"),
        ("Tipo de Cuenta", "Cuenta de Ahorros"),
        ("Número de Cuenta", "488427354540 (4884-2735-4540)"),
        ("Titular de la Cuenta", "Leonel Antonio Salcedo Acosta"),
        ("Identificación del Titular", "C.C. 1.022.943.003 (1022943003) de Bogotá D.C."),
    ]
    add_kv_table(doc, davivienda_rows, bold_value_indices={0, 2})

    add_subsection_heading(doc, "Opción 2 — Transferencia Inmediata Bre-B")
    breb_rows = [
        ("Canal de Pago Inmediato", "Transferencia Inmediata Bre-B"),
        ("Llave Bre-B", "1022943003"),
        ("Titular Beneficiario", "Leonel Antonio Salcedo Acosta"),
    ]
    add_kv_table(doc, breb_rows, bold_value_indices={0, 1})

    p_notif = doc.add_paragraph()
    p_notif.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_notif.paragraph_format.space_before = Pt(8)
    p_notif.paragraph_format.space_after = Pt(6)
    p_notif.paragraph_format.line_spacing = 1.15

    r_nf1 = p_notif.add_run("Envío de Comprobante de Pago: ")
    r_nf1.font.name = "Calibri"
    r_nf1.font.size = Pt(10.5)
    r_nf1.font.bold = True
    r_nf1.font.color.rgb = MORADO_PRIMARY

    r_nf2 = p_notif.add_run("Favor remitir el comprobante de transferencia a ")
    r_nf2.font.name = "Cambria"
    r_nf2.font.size = Pt(10.5)
    r_nf2.font.color.rgb = GRIS_TEXTO

    r_nf3 = p_notif.add_run("nomack3d@gmail.com / nomackleo@gmail.com")
    r_nf3.font.name = "Calibri"
    r_nf3.font.size = Pt(10.5)
    r_nf3.font.bold = True
    r_nf3.font.color.rgb = DORADO_ACCENT

    r_nf4 = p_notif.add_run(
        " con referencia \"Pago CC-2026-LLN-002 — Pitch Somos La Lupa News\" para proceder de manera "
        "inmediata con el envío del archivo HTML interactivo final."
    )
    r_nf4.font.name = "Cambria"
    r_nf4.font.size = Pt(10.5)
    r_nf4.font.color.rgb = GRIS_TEXTO

    # =========================================================================
    # 7. SUSCRIPCIÓN, FIRMAS Y CONSTANCIA DE ACEPTACIÓN
    # =========================================================================
    add_section_heading(doc, "7", "Suscripción, Firmas y Constancia de Aceptación")

    add_body_paragraph(
        doc,
        "Para constancia de lo manifestado, se expide y suscribe la presente Cuenta de Cobro en la "
        "ciudad de Bogotá D.C., Colombia, a los diecinueve (19) días del mes de Noviembre de 2026.",
        space_after=14,
    )

    table_firmas = doc.add_table(rows=1, cols=2)
    table_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER

    firmas_data = [
        (
            "________________________________________",
            "LEONEL ANTONIO SALCEDO ACOSTA",
            [
                "C.C. 1.022.943.003 de Bogotá D.C.",
                "Dirección y Consultoría Tecnológica",
                "Acreedor — Contratista Independiente",
                "Cel: 322 373 6685 · nomack3d@gmail.com / nomackleo@gmail.com",
            ],
        ),
        (
            "________________________________________",
            "JAVIER FERNÁNDEZ FRANCO",
            [
                "CEO & Representante Legal",
                "La Lupa News (somoslalupanews.com)",
                "Aceptación y Recibido — Orden de Pago",
                "Fecha de Recibido: _____ / _____ / 2026",
            ],
        ),
    ]

    for c_idx, (line_str, name_str, details) in enumerate(firmas_data):
        cell = table_firmas.rows[0].cells[c_idx]
        cell.width = Inches(3.25)
        set_cell_background(cell, "FFFFFF")
        set_cell_margins(cell, top=100, bottom=80, left=60, right=60)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15

        r_l = p.add_run(line_str + "\n")
        r_l.font.name = "Cambria"
        r_l.font.size = Pt(9.5)
        r_l.font.color.rgb = DORADO_ACCENT

        r_n = p.add_run(name_str + "\n")
        r_n.font.name = "Calibri"
        r_n.font.size = Pt(10)
        r_n.font.bold = True
        r_n.font.color.rgb = MORADO_PRIMARY

        for d_line in details:
            r_d = p.add_run(d_line + "\n")
            r_d.font.name = "Cambria"
            r_d.font.size = Pt(8.5)
            r_d.font.color.rgb = GRIS_META

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Anexos disponibles a solicitud
    p_anexos = doc.add_paragraph()
    p_anexos.paragraph_format.left_indent = Inches(0.12)
    p_anexos.paragraph_format.line_spacing = 1.15
    add_paragraph_border(p_anexos, side="left", hex_color=HEX_DORADO, sz="16", space="8")
    set_paragraph_shading(p_anexos, HEX_SURFACE)

    r_at = p_anexos.add_run("DOCUMENTACIÓN SOPORTE DISPONIBLE A SOLICITUD:\n")
    r_at.font.name = "Calibri"
    r_at.font.size = Pt(9.5)
    r_at.font.bold = True
    r_at.font.color.rgb = MORADO_PRIMARY

    r_ab = p_anexos.add_run(
        "1. Copia del Registro Único Tributario (RUT) actualizado de Leonel Antonio Salcedo Acosta.\n"
        "2. Copia de la Cédula de Ciudadanía del Acreedor (C.C. 1.022.943.003).\n"
        "3. Certificación bancaria vigente emitida por el Banco Davivienda (Cuenta de Ahorros 488427354540)."
    )
    r_ab.font.name = "Cambria"
    r_ab.font.size = Pt(8.5)
    r_ab.font.color.rgb = GRIS_TEXTO

    # Guardar en finance/cuentas_de_cobro/ (Taxonomía Canónica ISO — Nomack Studio v5.0.0)
    from pathlib import Path

    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / "finance" / "cuentas_de_cobro"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "CUENTA_DE_COBRO_CC-2026-LLN-002_PITCH_LALUPANEWS.docx"
    doc.save(str(output_path))
    print(f"[OK] Documento Word generado exitosamente en: {output_path}")


if __name__ == "__main__":
    create_cuenta_de_cobro_docx()
