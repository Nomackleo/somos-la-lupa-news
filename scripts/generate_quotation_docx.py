import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_quotation_docx(output_path):
    doc = docx.Document()
    
    # Page setup - Margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.different_first_page_header_footer = True
        
    C_PURPLE = RGBColor(45, 18, 77)
    C_GOLD = RGBColor(184, 132, 42)
    C_DEEP_PURPLE = RGBColor(34, 13, 58)
    C_BODY = RGBColor(34, 34, 34)
    C_GRAY = RGBColor(119, 119, 119)
    C_WHITE = RGBColor(255, 255, 255)
    
    HEX_PURPLE = "2D124D"
    HEX_GOLD = "B8842A"
    HEX_LIGHT_GRAY = "F5F7FA"
    HEX_BORDER = "CCCCCC"
    HEX_GOLD_BORDER = "B8842A"
    
    # Configure default normal style
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Cambria'
    normal_font.size = Pt(10.5)
    normal_font.color.rgb = C_BODY
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(5)
    
    # XML helper functions
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color=HEX_BORDER, sz="4", val="single"):
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(tblBorders)

    # ==========================================
    # 1. PORTADA INSTITUCIONAL (9 NIVELES)
    # ==========================================
    cover_p1 = doc.add_paragraph()
    cover_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p1.paragraph_format.space_before = Pt(28)
    cover_p1.paragraph_format.space_after = Pt(6)
    run_ch1 = cover_p1.add_run("LA LUPA NEWS — ESTRATEGIA DIGITAL Y TECNOLOGÍA")
    run_ch1.font.name = 'Calibri'
    run_ch1.font.size = Pt(8.5)
    run_ch1.font.bold = True
    run_ch1.font.color.rgb = C_GOLD

    cover_p2 = doc.add_paragraph()
    cover_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p2.paragraph_format.space_before = Pt(4)
    cover_p2.paragraph_format.space_after = Pt(14)
    run_ch2 = cover_p2.add_run("PROPUESTA COMERCIAL & PLAN ESCALONADO DE INTERVENCIÓN")
    run_ch2.font.name = 'Calibri'
    run_ch2.font.size = Pt(11)
    run_ch2.font.bold = True
    run_ch2.font.color.rgb = C_PURPLE

    cover_p3 = doc.add_paragraph()
    cover_p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p3.paragraph_format.space_before = Pt(8)
    cover_p3.paragraph_format.space_after = Pt(16)
    run_ch3 = cover_p3.add_run("COTIZACIÓN DE SERVICIOS: ACTUALIZACIÓN TÁCTICA, REMEDIACIÓN DE VULNERABILIDADES, BLINDAJE Y ARQUITECTURA PROPIA")
    run_ch3.font.name = 'Calibri'
    run_ch3.font.size = Pt(18)
    run_ch3.font.bold = True
    run_ch3.font.color.rgb = C_PURPLE

    cover_p4 = doc.add_paragraph()
    cover_p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p4.paragraph_format.space_before = Pt(10)
    cover_p4.paragraph_format.space_after = Pt(28)
    run_ch4 = cover_p4.add_run("Portal Digital somoslalupanews.com — Modelos Flexibles: Fase Semilla 'Investor-Ready', Continuidad y Soberanía Tecnológica")
    run_ch4.font.name = 'Calibri'
    run_ch4.font.size = Pt(12)
    run_ch4.font.italic = True
    run_ch4.font.color.rgb = RGBColor(102, 102, 102)

    cover_p5 = doc.add_paragraph()
    cover_p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p5.paragraph_format.space_before = Pt(16)
    cover_p5.paragraph_format.space_after = Pt(4)
    run_ch5 = cover_p5.add_run("PRESENTADO A:")
    run_ch5.font.name = 'Calibri'
    run_ch5.font.size = Pt(10)
    run_ch5.font.bold = True
    run_ch5.font.color.rgb = C_GOLD

    cover_p6 = doc.add_paragraph()
    cover_p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p6.paragraph_format.space_before = Pt(2)
    cover_p6.paragraph_format.space_after = Pt(2)
    run_ch6a = cover_p6.add_run("JAVIER FERNÁNDEZ FRANCO\n")
    run_ch6a.font.name = 'Calibri'
    run_ch6a.font.size = Pt(17)
    run_ch6a.font.bold = True
    run_ch6a.font.color.rgb = C_PURPLE
    run_ch6b = cover_p6.add_run("CEO — La Lupa News")
    run_ch6b.font.name = 'Calibri'
    run_ch6b.font.size = Pt(11.5)
    run_ch6b.font.color.rgb = RGBColor(17, 17, 17)

    cover_p7 = doc.add_paragraph()
    cover_p7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p7.paragraph_format.space_before = Pt(24)
    cover_p7.paragraph_format.space_after = Pt(4)
    run_div = cover_p7.add_run("____________________________________________________________")
    run_div.font.name = 'Calibri'
    run_div.font.size = Pt(9)
    run_div.font.color.rgb = C_GOLD

    cover_p8 = doc.add_paragraph()
    cover_p8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_p8.paragraph_format.space_before = Pt(6)
    cover_p8.paragraph_format.space_after = Pt(0)
    run_meta = cover_p8.add_run(
        "Presentado por: Leonel Salcedo | Dirección y Consultoría Tecnológica\n"
        "Fecha de Emisión: Octubre de 2026 | Estado: Versión Oficial Aprobada\n"
        "Referencia de Auditoría: Dictamen Técnico Forense somoslalupanews.com | Código: PROP-2026-LLN-SEC03"
    )
    run_meta.font.name = 'Calibri'
    run_meta.font.size = Pt(9)
    run_meta.font.color.rgb = C_GRAY

    # Salto de página
    doc.add_page_break()

    # ==========================================
    # 2. ENCABEZADOS Y PIES DE PÁGINA INTERIORES
    # ==========================================
    body_section = doc.sections[0]
    header = body_section.header
    header_p = header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_hdr = header_p.add_run("LA LUPA NEWS | Cotización de Ciberseguridad Web & Servidores\nConfidencial — Uso Exclusivo de Dirección General")
    run_hdr.font.name = 'Calibri'
    run_hdr.font.size = Pt(8.5)
    run_hdr.font.color.rgb = C_GRAY

    footer = body_section.footer
    footer_p = footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_ftr = footer_p.add_run("Leonel Salcedo — Dirección y Consultoría Tecnológica | Confidencial — La Lupa News")
    run_ftr.font.name = 'Calibri'
    run_ftr.font.size = Pt(8.5)
    run_ftr.font.color.rgb = C_GRAY

    def add_section_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        
        run_num = p.add_run(num_str + " ")
        run_num.font.name = 'Calibri'
        run_num.font.size = Pt(13)
        run_num.font.bold = True
        run_num.font.color.rgb = C_GOLD
        
        run_title = p.add_run(title_str)
        run_title.font.name = 'Calibri'
        run_title.font.size = Pt(13)
        run_title.font.bold = True
        run_title.font.color.rgb = C_PURPLE
        
        p_line = doc.add_paragraph()
        p_line.paragraph_format.space_before = Pt(0)
        p_line.paragraph_format.space_after = Pt(8)
        run_l = p_line.add_run("―" * 55)
        run_l.font.size = Pt(7.5)
        run_l.font.color.rgb = C_GOLD

    def add_callout(text, title="ALERTA"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_LIGHT_GRAY)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="20" w:space="0" w:color="{HEX_GOLD}"/>'
            f'<w:top w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after = Pt(3)
        rt = cp.add_run(title + "\n")
        rt.font.name = 'Calibri'
        rt.font.size = Pt(9.5)
        rt.font.bold = True
        rt.font.color.rgb = C_PURPLE
        
        rc = cp.add_run(text)
        rc.font.name = 'Cambria'
        rc.font.size = Pt(9.5)
        rc.font.color.rgb = C_BODY
        doc.add_paragraph()

    # ==========================================
    # SECCIÓN 1: PRESENTACIÓN Y FILOSOFÍA COMERCIAL
    # ==========================================
    add_section_heading("1.", "Presentación Ejecutiva y Enfoque de Acompañamiento Estratégico")

    p = doc.add_paragraph()
    p.add_run(
        "Estimado Javier,\n\n"
        "Comprendiendo a cabalidad el momento decisivo en el que se encuentra "
    )
    r_bold = p.add_run("La Lupa News")
    r_bold.font.bold = True
    r_bold.font.color.rgb = C_PURPLE
    p.add_run(
        ", enfocado en la consecución y cierre de rondas de inversión, patrocinadores estratégicos e inyección de capital "
        "para consolidar el proyecto, la plataforma digital "
    )
    r_link = p.add_run("somoslalupanews.com")
    r_link.font.bold = True
    r_link.font.color.rgb = C_PURPLE
    p.add_run(
        " representa el activo patrimonial y la carta de presentación más crítica ante evaluadores, inversionistas y mesas de dinero. "
        "En una reunión de negocios, si un inversionista intenta evaluar el medio desde su oficina corporativa o red bancaria y choca "
        "contra una pantalla roja de bloqueo de seguridad, o detecta fallos de navegación, la credibilidad del medio se compromete al instante.\n\n"
        "Bajo un principio de absoluta cercanía, entendimiento financiero y flexibilidad comercial con el cliente, hemos estructurado "
        "un portafolio en tres dimensiones estratégicas:\n"
        "1. "
    )
    r_t1 = p.add_run("Planes Tácticos 'Investor-Ready' (Inversión reducida < $600.000 COP): ")
    r_t1.font.bold = True
    r_t1.font.color.rgb = C_GOLD
    p.add_run(
        "Alternativas ágiles diseñadas para eliminar el bloqueo perimetral ante inversionistas, corregir la navegación y cerrar las brechas "
        "más riesgosas de desfiguración visual sin asfixiar el flujo de caja actual del periódico.\n"
        "2. "
    )
    r_t2 = p.add_run("Planes Estructurales de Continuidad (Fase de Escalamiento): ")
    r_t2.font.bold = True
    r_t2.font.color.rgb = C_PURPLE
    p.add_run(
        "La remediación pericial exhaustiva de las 93 vulnerabilidades y póliza de monitoreo 24/7 para operar con estándares corporativos.\n"
        "3. "
    )
    r_t3 = p.add_run("Soberanía Tecnológica (Backend Propio a Medida): ")
    r_t3.font.bold = True
    r_t3.font.color.rgb = C_GOLD
    p.add_run(
        "El desarrollo de un sistema de gestión editorial propio, eliminando para siempre WordPress, los costos de licencias a terceros "
        "y la fragilidad de actualizaciones externas."
    )

    add_callout(
        "Garantía de Escalabilidad (Crédito de Inversión): Si contratas hoy el Plan Táctico B ($580.000 COP) para asegurar tus reuniones con inversionistas, "
        "el 100% de ese valor se acreditará como abono a tu favor si decides ascender al Plan Estructural ($3.600.000 COP) dentro de los siguientes 45 días tras concretar el capital.",
        title="FILOSOFÍA GANAR-GANAR: FACILIDADES INMEDIATAS CON CRÉDITO A FUTURO"
    )

    # ==========================================
    # SECCIÓN 2: ESTRUCTURA TARIFARIA Y MATRIZ DE OPCIONES
    # ==========================================
    add_section_heading("2.", "Estructura Tarifaria Integral y Opciones Escalonadas")

    p = doc.add_paragraph()
    p.add_run(
        "A continuación se presenta la matriz comercial comparativa. La Dirección General puede elegir la alternativa que mejor "
        "se ajuste a su presupuesto inmediato, con la tranquilidad de contar con una ruta clara de escalamiento futuro:"
    )

    # Tabla de Tarifas
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    headers = ["Nivel / Plan Comercial", "Alcance y Componentes Incluidos", "Tiempo de Entrega", "Inversión (COP)"]
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], HEX_PURPLE)
        set_cell_margins(hdr_cells[i], top=130, bottom=130, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(8.5)
            run.font.bold = True
            run.font.color.rgb = C_WHITE

    plans = [
        ("NIVEL 1: TÁCTICO A\n'Desbloqueo & Pitch-Ready'\n(Mínimo para Exposición)",
         "• Respaldo de seguridad esencial previo (código + base de datos).\n"
         "• Trámite pericial ante Fortinet FortiGuard para levantar el bloqueo corporativo/bancario a somoslalupanews.com.\n"
         "• Corrección y alineación de registros DNS en GoDaddy y Hostinger.\n"
         "• Redirección limpia del dominio histórico lalupanews.com (desvío de ParkLogic).\n"
         "• Reparación de las 10 URLs residuales rotas en la portada.\n"
         "• Verificación de certificado de navegación segura (HTTPS/SSL).",
         "2 a 3 días hábiles",
         "$380.000 COP\n(Pago de contado)"),
        ("NIVEL 1: TÁCTICO B\n'Investor-Ready & BMV'\n(Recomendado para Rondas)",
         "• Todo lo incluido en el Plan Táctico A ($380.000 COP).\n"
         "• Parcheo de choque de brechas críticas de ejecución de código y subida de archivos en plugins de formularios (Forminator) y constructores.\n"
         "• Cierre perimetral de la fuga de identidades de redactores y administradores en la API.\n"
         "• Parcheo preventivo menor en el núcleo del sistema web.\n"
         "• Protección básica contra intentos masivos de adivinación de claves en el acceso administrativo.\n"
         "• Entrega de checklist de validación para demostraciones con inversionistas.",
         "3 a 4 días hábiles",
         "$580.000 COP\n(Pago de contado)\n(< $600.000 COP)"),
        ("NIVEL 2: CAPITALIZACIÓN\n'Plan de Choque & Remediación Integral'\n(Fase Post-Inversión)",
         "• Ejecución total de las 4 Fases Técnicas de ciberseguridad forense.\n"
         "• Mitigación exhaustiva de las 93 vulnerabilidades documentadas (Core 6.9.9 a 7.1.3 + los 8 plugins críticos).\n"
         "• Despliegue en entorno de pruebas espejo (Staging) para validación visual de portadas y noticias.\n"
         "• Endurecimiento completo de servidor y directivas de configuración seguras.\n"
         "• Implementación de cabeceras de protección informática avanzada.\n"
         "• Configuración de tareas programadas automáticas en el servidor.\n"
         "• Entrega de Informe Pericial Final y Certificación de Parcheo.",
         "7 a 10 días hábiles",
         "$3.600.000 COP\n(50% anticipo / 50% entrega)"),
        ("NIVEL 3: CONTINUIDAD\n'Plan Integral + Póliza DevSecOps Trimestral'\n(Operatividad y Monitoreo 24/7)",
         "• Todo lo incluido en el Plan de Remediación Integral ($3.600.000 COP).\n"
         "• Monitoreo activo de ciberseguridad 24/7 durante noventa (90) días calendario.\n"
         "• Mantenimiento y actualización preventiva mensual de componentes y extensiones.\n"
         "• Copias de seguridad automáticas externas semanales con verificación periódica.\n"
         "• Optimización continua de velocidad y aceleradores de carga.\n"
         "• Soporte técnico prioritario con tiempo de respuesta inferior a 4 horas.",
         "3 Meses (90 días)",
         "$5.400.000 COP\n(O $3.000.000 inicial + 2 cuotas de $1.200.000)"),
        ("NIVEL 4: SOBERANÍA TOTAL\n'Desarrollo de Backend Propio a Medida'\n(Independencia y Cero WordPress)",
         "• Arquitectura editorial propietaria diseñada a la medida exacta de La Lupa News.\n"
         "• Cero dependencia de WordPress: eliminación radical de las 93 vulnerabilidades y parches constantes.\n"
         "• Eliminación definitiva de costos de licencias a terceros (plugins de pago, constructores visuales).\n"
         "• Velocidad de carga ultrarrápida (3x a 5x superior), maximizando tráfico publicitario y SEO en Google.\n"
         "• Panel de redacción intuitivo, seguro, ultraliviano y blindado contra ataques masivos de internet.\n"
         "• Migración completa y transparente de todo el histórico de noticias e imágenes.",
         "4 a 6 semanas",
         "$9.800.000 COP\n(50% inicio / 25% entrega / 25% despliegue)")
    ]

    for p_title, p_desc, p_term, p_price in plans:
        row_cells = table.add_row().cells
        
        row_cells[0].text = p_title
        set_cell_margins(row_cells[0], top=100, bottom=100, left=90, right=90)
        p = row_cells[0].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(8.5)
            run.font.bold = True
            run.font.color.rgb = C_PURPLE
            
        row_cells[1].text = p_desc
        set_cell_margins(row_cells[1], top=100, bottom=100, left=90, right=90)
        p = row_cells[1].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Cambria'
            run.font.size = Pt(8)
            run.font.color.rgb = C_BODY

        row_cells[2].text = p_term
        set_cell_margins(row_cells[2], top=100, bottom=100, left=90, right=90)
        p = row_cells[2].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(8)
            run.font.color.rgb = C_BODY

        row_cells[3].text = p_price
        set_cell_margins(row_cells[3], top=100, bottom=100, left=90, right=90)
        set_cell_background(row_cells[3], HEX_LIGHT_GRAY)
        p = row_cells[3].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(8.5)
            run.font.bold = True
            run.font.color.rgb = C_GOLD

    doc.add_paragraph()

    # ==========================================
    # SECCIÓN 2.1: DESGLOSE EN LENGUAJE CERO TÉCNICO
    # ==========================================
    add_section_heading("2.1.", "Desglose Ejecutivo en Lenguaje Claro: ¿Qué significa cada componente para el negocio?")

    p = doc.add_paragraph()
    p.add_run(
        "Para que la Dirección General cuente con total claridad al momento de tomar decisiones y presentar el proyecto "
        "a sus evaluadores de inversión, a continuación se traduce cada término de la propuesta a su impacto real en el negocio, "
        "en un lenguaje completamente transparente y libre de tecnicismos:"
    )

    items_no_tech = [
        ("1. Respaldo de Base de Datos y Archivos (Caja Fuerte Digital):",
         "Consiste en crear una copia exacta e inmodificable de todo el patrimonio informativo del periódico (todas las noticias publicadas, "
         "investigaciones históricas, fotografías, perfiles de redactores y configuraciones) antes de tocar una sola línea de código. "
         "Garantiza que, pase lo que pase, el medio de comunicación jamás perderá su memoria periodística ni su archivo de publicaciones."),
        
        ("2. Desbloqueo ante FortiGuard y Redes Corporativas (Eliminación de la Lista Negra):",
         "Actualmente, cuando un banco, una gran empresa, un ministerio o un inversionista en su oficina intenta abrir somoslalupanews.com, "
         "su antivirus empresarial bloquea la pantalla con una alerta roja diciendo que el sitio es sospechoso porque el dominio tiene pocos días de creado. "
         "Este trámite pericial consiste en radicar las solicitudes oficiales para que las firmas de seguridad retiren a La Lupa News de esa lista de alerta, "
         "permitiendo que cualquier patrocinador o evaluador entre directamente y sin mensajes de peligro."),
        
        ("3. Dominio Limpio y Redirección del Enlace Antiguo (Consistencia de Marca):",
         "Hoy en día, las personas que buscan el nombre tradicional del medio son enviadas a una página de anuncios ajenos en internet. "
         "Tener un 'dominio limpio' significa que cualquier lector o cliente corporativo que escriba la dirección histórica sea llevado de forma "
         "automática e imperceptible al portal actual, reparando además los enlaces rotos internos para que la marca proyecte seriedad y profesionalismo."),
         
        ("4. Cierre de Fuga en la API y Protección de Accesos (Cerrar las Puertas Traseras):",
         "Actualmente, la plataforma tiene una 'ventana abierta' que le entrega a cualquier curioso o pirata informático la lista con los nombres exactos "
         "de los periodistas y administradores del medio. Cerrar esta fuga significa poner una cortina opaca: nadie desde afuera puede ver quién administra "
         "el sitio, impidiendo que delincuentes digitales intenten adivinar contraseñas o secuestrar las cuentas para publicar contenido falso."),
         
        ("5. Parcheo de Brechas Críticas en Formularios y Constructores (Evitar la Desfiguración del Portal):",
         "Los módulos que hoy utiliza la web para recibir mensajes o maquetar portadas tienen grietas graves que permitirían a un tercero tomarse "
         "el control del periódico, cambiar los titulares por propaganda o borrar la página en cuestión de segundos. Parchear estas brechas equivale "
         "a cambiar las cerraduras dañadas para evitar que el medio sufra un ataque vergonzoso en medio de una reunión con inversionistas."),
         
        ("6. Entorno Espejo de Pruebas o Staging (El Laboratorio de Ensayo):",
         "En lugar de hacer experimentos o actualizaciones directamente sobre la página que el público está leyendo, se crea una copia idéntica 'en privado'. "
         "Allí se corrigen los errores, se prueban las noticias y se verifica que los titulares se vean perfectos. Solo cuando todo está 100% probado "
         "se traslada a la página pública, asegurando que el sitio jamás se caiga ni muestre errores a la audiencia."),
         
        ("7. Blindaje del Servidor y Cabeceras de Seguridad (Protección Perimetral del Motor Web):",
         "Es el equivalente a colocar alarmas perimetrales y vidrios blindados en la sede física del medio. Evita que espías informáticos sepan qué "
         "programas usa el servidor para atacarlo y bloquea intentos de suplantar correos corporativos haciéndose pasar por periodistas de La Lupa News."),
         
        ("8. Desarrollo de Backend Propio a Medida (Independencia y Soberanía Tecnológica):",
         "Hoy el periódico depende de WordPress, un sistema genérico que requiere parches continuos, es el blanco favorito de piratas informáticos "
         "y obliga a comprar licencias a proveedores extranjeros. Construir un motor propio significa fabricar una plataforma a la medida exacta "
         "de La Lupa News: ultrarrápida, 100% inmune a ataques comunes, sin costos de licencias a terceros y que incrementa el valor patrimonial "
         "del proyecto de cara a venderlo a futuros inversionistas.")
    ]

    for it_title, it_desc in items_no_tech:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.space_before = Pt(4)
        p_it.paragraph_format.space_after = Pt(3)
        r_tit = p_it.add_run(it_title + "\n")
        r_tit.font.name = 'Calibri'
        r_tit.font.size = Pt(10)
        r_tit.font.bold = True
        r_tit.font.color.rgb = C_PURPLE
        
        r_dsc = p_it.add_run(it_desc)
        r_dsc.font.name = 'Cambria'
        r_dsc.font.size = Pt(9.5)

    # ==========================================
    # SECCIÓN 3: DELIMITACIÓN RESPONSABLE DEL ALCANCE
    # ==========================================
    add_section_heading("3.", "Hoja de Ruta y Delimitación Responsable de Alcance")

    p = doc.add_paragraph()
    p.add_run(
        "Es fundamental que la Dirección General cuente con una hoja de ruta transparente para guiar la evolución de su plataforma:\n\n"
        "• "
    )
    r_h1 = p.add_run("Alcance de los Planes Tácticos ($380.000 / $580.000 COP): ")
    r_h1.font.bold = True
    r_h1.font.color.rgb = C_GOLD
    p.add_run(
        "Constituyen una intervención de choque para levantar la bandera roja ante inversionistas, corregir enlaces rotos y contener "
        "las brechas más escandalosas. Permite presentar el proyecto con dignidad comercial sin asfixiar el presupuesto de arranque.\n\n"
        "• "
    )
    r_h2 = p.add_run("Alcance de los Planes Estructurales ($3.600.000 / $5.400.000 COP): ")
    r_h2.font.bold = True
    r_h2.font.color.rgb = C_PURPLE
    p.add_run(
        "Es la ingeniería de blindaje integral para cuando los fondos de inversión ingresen al medio: resuelve las 93 vulnerabilidades "
        "acumuladas y otorga soporte continuo 24/7 para operar con millones de visitas mensuales.\n\n"
        "• "
    )
    r_h3 = p.add_run("Alcance de la Soberanía Tecnológica ($9.800.000 COP): ")
    r_h3.font.bold = True
    r_h3.font.color.rgb = C_GOLD
    p.add_run(
        "La cúspide del escalamiento digital: una plataforma hecha a medida que convierte a La Lupa News en un activo de tecnología propio, "
        "eliminando para siempre los costos y la fragilidad de plataformas de terceros."
    )

    # ==========================================
    # SECCIÓN 4: CONDICIONES COMERCIALES Y PAGO
    # ==========================================
    add_section_heading("4.", "Condiciones Comerciales y Política de Pago")

    p = doc.add_paragraph()
    p.add_run(
        "Con el objetivo de garantizar una relación transparente y organizada, se definen los siguientes términos:"
    )

    condiciones = [
        ("1. Modalidad de Pago para Planes Tácticos (Nivel 1):", 
         " Al tratarse de paquetes especiales y accesibles de habilitación inmediata (< $600.000 COP), el valor seleccionado ($380.000 COP o $580.000 COP) se cancela 100% de contado de manera anticipada para dar inicio formal a las labores y respaldos."),
        ("2. Modalidad de Pago para Planes Estructurales (Nivel 2 y 3):", 
         " Anticipo indispensable del cincuenta por ciento (50%) al inicio para la preparación de Staging y respaldos, y el cincuenta por ciento (50%) restante contra entrega certificada."),
        ("3. Modalidad de Pago para Backend Propio (Nivel 4):", 
         " Cincuenta por ciento (50%) al inicio para arquitectura de software, veinticinco por ciento (25%) contra entrega del panel editorial funcional, y veinticinco por ciento (25%) contra despliegue y migración en producción."),
        ("4. Garantía de Escalabilidad (Crédito de Inversión):", 
         " Si La Lupa News contrata el Plan Táctico B ($580.000 COP) y en los siguientes 45 días decide ascender al Plan Estructural ($3.600.000 COP) tras el ingreso de capital, el 100% del valor pagado por el plan táctico se abonará como parte de pago del nuevo contrato."),
        ("5. Política Estricta de Inicio:", 
         " Ninguna intervención técnica en servidor ni manipulación de archivos se ejecutará sin la verificación efectiva de la transferencia de fondos correspondiente.")
    ]

    for c_title, c_desc in condiciones:
        pc = doc.add_paragraph()
        pc.paragraph_format.space_before = Pt(3)
        pc.paragraph_format.space_after = Pt(3)
        r_ct = pc.add_run(c_title)
        r_ct.font.bold = True
        r_ct.font.color.rgb = C_GOLD
        r_cd = pc.add_run(c_desc)

    # ==========================================
    # SECCIÓN 5: INFORMACIÓN BANCARIA
    # ==========================================
    add_section_heading("5.", "Información Bancaria para Dispersión de Fondos")

    p = doc.add_paragraph()
    p.add_run("Las transferencias deberán efectuarse exclusivamente a nombre del titular oficial:")

    b_table = doc.add_table(rows=5, cols=2)
    b_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(b_table)

    bank_info = [
        ("Titular de la Cuenta", "Leonel Antonio Salcedo Acosta"),
        ("Identificación Tributaria", "C.C. 1.022.943.003 de Bogotá"),
        ("Entidad Bancaria", "Banco Davivienda"),
        ("Tipo y Número de Cuenta", "Cuenta de Ahorros Nº 4884-2735-4540"),
        ("Banca Digital / Transfiya / Nequi", "Línea Celular: 322 373 6685 (Nequi / Daviplata / Bancolombia)")
    ]

    for idx, (label, val) in enumerate(bank_info):
        r = b_table.rows[idx]
        r.cells[0].text = label
        r.cells[1].text = val
        set_cell_background(r.cells[0], HEX_LIGHT_GRAY)
        set_cell_margins(r.cells[0], top=85, bottom=85, left=110, right=110)
        set_cell_margins(r.cells[1], top=85, bottom=85, left=110, right=110)
        
        p0 = r.cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p0.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(9)
            run.font.bold = True
            run.font.color.rgb = C_PURPLE
            
        p1 = r.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p1.runs:
            run.font.name = 'Cambria'
            run.font.size = Pt(9)
            run.font.bold = (idx in [0, 3, 4])
            run.font.color.rgb = C_BODY

    doc.add_paragraph()

    # ==========================================
    # SECCIÓN 6: ACEPTACIÓN Y FIRMAS
    # ==========================================
    add_section_heading("6.", "Aceptación Institucional y Formalización del Servicio")

    p = doc.add_paragraph()
    p.add_run(
        "La notificación formal del plan elegido o la confirmación de la transferencia del abono respectivo "
        "activará de inmediato la orden de servicio para el inicio del cronograma de trabajo."
    )

    doc.add_paragraph()

    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = sig_table._tbl.tblPr
    tblBorders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="none"/><w:bottom w:val="none"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(tblBorders)

    c_left = sig_table.cell(0, 0)
    c_right = sig_table.cell(0, 1)

    p_sig1 = c_left.paragraphs[0]
    p_sig1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_sig1.add_run("_________________________________________\n")
    r.font.color.rgb = C_PURPLE
    r1 = p_sig1.add_run("Leonel Salcedo\n")
    r1.font.bold = True
    r1.font.color.rgb = C_PURPLE
    r2 = p_sig1.add_run("Dirección y Consultoría Tecnológica\nC.C. 1.022.943.003 de Bogotá\nConsultor Líder en Infraestructura & DevSecOps")
    r2.font.size = Pt(9)
    r2.font.color.rgb = C_GRAY

    p_sig2 = c_right.paragraphs[0]
    p_sig2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_sig2.add_run("_________________________________________\n")
    r.font.color.rgb = C_GOLD
    r3 = p_sig2.add_run("Javier Fernández Franco\n")
    r3.font.bold = True
    r3.font.color.rgb = C_PURPLE
    r4 = p_sig2.add_run("CEO & Representante Legal\nLa Lupa News\nAceptado — Orden de Servicio")
    r4.font.size = Pt(9)
    r4.font.color.rgb = C_GRAY

    doc.save(output_path)
    print(f"Documento DOCX generado exitosamente en: {output_path}")

if __name__ == "__main__":
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / "finance" / "cotizaciones"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "COTIZACION_ACTUALIZACION_SEGURIDAD_SOMOSLALUPANEWS.docx"
    create_quotation_docx(str(out_file))
