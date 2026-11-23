# somos-la-lupa-news (`projects/la-lupa-news/`)

> **Portal Digital, Arquitectura Web, Ciberseguridad y Estrategia Tecnológica — La Lupa News**  
> Repositorio desacoplado certificado bajo los estándares **ISO 9001:2015**, **ISO/IEC 27001:2022**, **ISO/IEC 25010:2023** e **ISO/IEC 42001:2023**, con memoria persistente integrada y sincronización multi-estación (**Desktop** ↔ **Laptop Nitro**) vía GitHub.

---

## 1. Gobernanza Institucional y Dirección del Proyecto

| Rol | Entidad / Responsable |
| :--- | :--- |
| **Cliente Corporativo** | **La Lupa News** (`somoslalupanews.com`) |
| **CEO del Cliente** | **Javier Fernández Franco** |
| **Dirección & Consultoría Tecnológica** | **Leonel Salcedo** |
| **Ruta Canónica Desacoplada** | `projects/la-lupa-news/` |
| **Repositorio Remoto (GitHub)** | `https://github.com/Nomackleo/somos-la-lupa-news.git` |
| **Estado del Repositorio** | Estandarizado ISO · Memoria Persistente Activa · Sync Multi-Host Activo |

---

## 2. Identidad Visual Documental & Paleta Oficial (Entregables al Cliente)

Todo documento formal, manual, cotización o dictamen dirigido a **La Lupa News** debe cumplir de forma estricta [`GEMINI.md`](GEMINI.md) y [`docs/01_gobernanza/NS-LLN-GOV-002_MANUAL_ESTETICA_Y_UI_DOCUMENTAL.md`](docs/01_gobernanza/NS-LLN-GOV-002_MANUAL_ESTETICA_Y_UI_DOCUMENTAL.md):

- **Morado Marca Personal (`#2d124d`)**: Títulos H1/H2, nodos principales y negritas institucionales.
- **Morado Profundo (`#220d3a`)**: Énfasis tipográfico y alto contraste.
- **Dorado Institucional (`#b8842a`)**: Filetes horizontales, numeraciones, viñetas y etiquetas de acento.
- **Cuerpo de Texto (`#222222`)**: Fuente Cambria 11pt, interlineado 1.15, texto justificado.

---

## 3. Arquitectura Canónica del Proyecto (ISO 9001 Cl. 7.5 & ISO 27001)

```text
projects/la-lupa-news/
├── .agents/                        # Reglas y skills locales específicas de La Lupa News
├── .secrets/                       # [GITIGNORED] Bóveda local de credenciales (ISO 27001 A.8.12)
├── assets/
│   ├── branding/                   # Logos, manual de marca y tipografías oficiales
│   └── web-media/                  # Recursos editoriales y piezas de prueba del portal
├── docs/                           # Taxonomía obligatoria ISO 9001 Cláusula 7.5
│   ├── README.md                   # NS-LLN-DOC-000 — Índice Maestro Documental ISO
│   ├── 01_gobernanza/              # NS-LLN-GOV-001..003 + documentación comercial/negocio
│   ├── 02_especificaciones/        # NS-LLN-SPEC-001 + diagramas Mermaid y comparativas técnicas
│   ├── 03_auditorias_y_drift/      # NS-LLN-AUD-001 (Auditoría 93 CVEs / FortiGuard / Hostinger)
│   └── 04_bitacora_cambios/        # NS-LLN-CHG-001 + NS-LLN-MEM-001 (Memoria Persistente)
├── finance/                        # Comprobantes PSE, cotizaciones y conciliación de cartera
├── knowledge/                      # Memoria persistente optimizada para modelos IA
│   ├── README.md                   # Protocolo Brief-First de carga de contexto
│   ├── project_memory.json         # Grafo estructurado de conocimiento del proyecto
│   ├── project_memory.sqlite       # Índice local FTS5 BM25 con validación anti-secretos
│   └── backups_cold_storage_manifest.json # Inventario auditado de respaldos fuera de Git
├── pipeline/                       # Patrón Blackboard para continuidad agéntica
│   ├── PROJECT_BUS.json            # Estado vivo de fases, compuertas HITL y sincronización
│   └── handoffs/                   # Contratos JSON validados por handoff-validator.py
├── scripts/
│   ├── generate_quotation_docx.py  # Generador DOCX con rutas portables multi-estación
│   ├── update_project_memory.py    # Indexador local determinista SQLite FTS5 ($0.00)
│   └── sync_workstation.ps1        # Asistente de sincronización Desktop <-> Laptop Nitro
├── templates/                      # Plantilla oficial ejecutiva con portada de 9 niveles
├── web/                            # Referencias y metadatos de plugins/temas WordPress
├── .gitignore                      # Blindaje ISO 27001 (excluye .secrets, dumps SQL y backups)
├── AGENTS.md                       # Gobernanza local desacoplada y onboarding de modelos IA
├── GEMINI.md                       # Reglas obligatorias de estilo y marca personal
└── README.md                       # Este documento
```

---

## 4. Guía de Sincronización Multi-Estación (Desktop `HOST-01-STUDIO` ↔ Laptop Nitro `HOST-02-MOBILE`)

### A. Primera clonación en **Laptop Nitro (`HOST-02-MOBILE`)**
Ubicado dentro de la carpeta `projects/` de la estación portátil:
```powershell
git clone https://github.com/Nomackleo/somos-la-lupa-news.git la-lupa-news
cd la-lupa-news
# Configurar identificador de estación (una sola vez en Laptop Nitro):
[System.Environment]::SetEnvironmentVariable('NOMACK_STUDIO_HOST_ID', 'HOST-02-MOBILE', 'User')
```

### B. Flujo diario antes y después de trabajar
```powershell
# Al iniciar sesión (Pre-Flight Sync):
.\scripts\sync_workstation.ps1 -Action pull

# Al finalizar avances (actualiza memoria local, valida seguridad y sincroniza con GitHub):
python scripts\update_project_memory.py
.\scripts\sync_workstation.ps1 -Action status
```

Para detalles de resolución de divergencias y compromisos Conventional Commits, consultar [`docs/01_gobernanza/NS-LLN-GOV-003_PROTOCOLO_SEGURIDAD_Y_SINCRONIZACION.md`](docs/01_gobernanza/NS-LLN-GOV-003_PROTOCOLO_SEGURIDAD_Y_SINCRONIZACION.md).

---

## 5. Confidencialidad y Derechos

Documentación, auditorías y código desarrollados para **La Lupa News** bajo la dirección de su CEO **Javier Fernández Franco**.  
Consultoría Tecnológica & Transformación Digital liderada exclusivamente por **Leonel Salcedo**. Todos los derechos reservados.
