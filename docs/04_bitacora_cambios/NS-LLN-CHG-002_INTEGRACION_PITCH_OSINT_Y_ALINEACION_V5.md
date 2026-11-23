# Bitácora de Integración Pitch Comercial, Auditorías OSINT/Marca y Alineación Nomack Studio v5.0.0 (`NS-LLN-CHG-002`)

| Campo de Control ISO 9001 (Cláusula 7.5) | Valor Canónico |
| :--- | :--- |
| **Código de Documento** | `NS-LLN-CHG-002` |
| **Versión SemVer** | `1.0.0` |
| **Fecha de Emisión / Revisión** | `2026-11-23` |
| **Estado** | `Vigente` |
| **Autor / Aprobador** | `Leonel Salcedo (Dirección y Consultoría Tecnológica / HITL Lead)` |
| **Estación de Ejecución** | `Laptop Nitro` (`HOST-02-MOBILE`) |
| **Marcos ISO Aplicables** | `ISO 9001:2015 (Cl. 7.1.6, 7.5, 8.5.6)` · `ISO/IEC 27001:2022` · `ISO/IEC 25010:2023` · `ISO/IEC 42001:2023` |

---

## 1. Resumen de la Intervención

Tras ejecutar la sincronización *fast-forward* sin pérdida (`62982d9` → `4bd51e7`) en la estación portátil **`HOST-02-MOBILE` (Laptop Nitro)**, se integraron de forma no destructiva los **22 archivos locales** producidos para el Pitch Comercial/Inversión, auditorías de marca y OSINT, y la Cuenta de Cobro `CC-2026-LLN-002` dentro de la taxonomía canónica ISO 9001/27001/25010 de **`projects/la-lupa-news/`**, alineando la gobernanza local a **Nomack Studio `v5.0.0 (CRSI-Ready)`**.

- **Integridad de Datos:** `22/22` activos locales contabilizados (`13` reubicados con verificación SHA-256 idéntica, `5` capturas preservadas en `assets/captures/`, `4` copias redundantes deduplicadas contra SSOT SHA-256 en `assets/branding/logos/`).
- **Auditoría ISO 27001 / Guarda de Estilo:** `0` fugas de secretos, `0` patrones prohibidos en entregables al cliente, `0` enlaces Markdown rotos, `5/5` scripts Python compilados sin error.

---

## 2. Matriz Forense de Integración y Deduplicación (Zero Data Loss)

| Origen Local (`HOST-02-MOBILE`) | Destino Canónico ISO (`projects/la-lupa-news/`) | Acción / Justificación ISO |
| :--- | :--- | :--- |
| `docs/02_investigacion/01_estudio_mercado_y_narrativa.md` | `docs/01_gobernanza/negocio/NS-LLN-GOV-004_ESTUDIO_MERCADO_Y_NARRATIVA_PITCH.md` | Integrado con tabla de control ISO 9001 Cl. 7.5 (conserva portada 9 niveles). |
| `docs/02_investigacion/02_auditoria_scraping_y_marca.md` | `docs/03_auditorias_y_drift/NS-LLN-AUD-002_AUDITORIA_SCRAPING_MARCA_Y_CAPTURAS.md` | Integrado como auditoría técnica de marca/capturas con enlaces canónicos `assets/branding/`. |
| `docs/02_investigacion/03_auditoria_osint_y_redes.md` | `docs/03_auditorias_y_drift/NS-LLN-AUD-003_AUDITORIA_OSINT_Y_ECOSISTEMA_SOCIAL.md` | Integrado como auditoría OSINT, RDAP/DNS, SEO y red social con filtro de homónimos. |
| `docs/04_plan_presentacion/plan_presentacion_hitl_somos_la_lupa_news.md` | `docs/02_especificaciones/NS-LLN-SPEC-002_PLAN_MAESTRO_PITCH_INTERACTIVO_HITL.md` | Integrado como especificación funcional/UI (`NS-LLN-SPEC-002`) del Pitch interactivo. |
| `docs/03_facturacion/cuenta_de_cobro_pitch_la_lupa_news.md` | `finance/cuentas_de_cobro/CUENTA_DE_COBRO_CC-2026-LLN-002_PITCH_LALUPANEWS.md` | Reubicado en cartera oficial en secuencia directa tras `CC-2026-LLN-001`. |
| `docs/03_facturacion/Cuenta_de_Cobro_Pitch_La_Lupa_News.docx` | `finance/cuentas_de_cobro/CUENTA_DE_COBRO_CC-2026-LLN-002_PITCH_LALUPANEWS.docx` | Entregable Word oficial reubicado sin alteración binaria. |
| `docs/05_entregable_pitch/Presentacion_Pitch_Comercial_Somos_La_Lupa_News.html` | `deliverables/pitch_comercial/Presentacion_Pitch_Comercial_Somos_La_Lupa_News.html` | Entregable interactivo autocontenido (`1.66 MB`, identidad real `#052962` + `#B9AF07`). |
| `docs/05_entregable_pitch/Presentacion_Pitch_Comercial_Somos_La_Lupa_News.pdf` | `deliverables/pitch_comercial/Presentacion_Pitch_Comercial_Somos_La_Lupa_News.pdf` | Copia vectorial widescreen (`5.76 MB`, `1440×900`) preservada íntegra. |
| `bin/build_docx_cuenta_de_cobro_la_lupa.py` | `scripts/build_docx_cuenta_de_cobro_la_lupa.py` | Consolidado en `scripts/` con `Path(__file__).resolve()` hacia `finance/cuentas_de_cobro/`. |
| `bin/build_pitch_html_la_lupa.py` | `scripts/build_pitch_html_la_lupa.py` | Consolidado en `scripts/` apuntando a SSOT `assets/branding/logos/` y `deliverables/pitch_comercial/`. |
| `bin/build_pitch_pdf_la_lupa.py` | `scripts/build_pitch_pdf_la_lupa.py` | Consolidado en `scripts/` apuntando a `deliverables/pitch_comercial/`. |
| `assets/brand/brand_tokens.json` | `assets/branding/brand_tokens.json` | Consolidado con rutas SSOT hacia `assets/branding/logos/`. |
| `assets/brand/favicon.png` | `assets/branding/logos/favicon.png` | Activo único `300×300 px` consolidado en `assets/branding/logos/`. |
| `assets/brand/imago_oficial.png` | *(Deduplicado → SSOT `assets/branding/logos/Imago favi2.png`)* | Duplicado exacto verificado (SHA-256 `FEE7224457A3...`). |
| `assets/brand/imago_variante.png` | *(Deduplicado → SSOT `assets/branding/logos/Imago 1.png`)* | Duplicado exacto verificado (SHA-256 `D1A02807F9DC...`). |
| `assets/brand/logo_alternativo_1.png` | *(Deduplicado → SSOT `assets/branding/logos/Logo 1.png`)* | Duplicado exacto verificado (SHA-256 `44210FE02349...`). |
| `assets/brand/logo_principal_fondo_azul.png` | *(Deduplicado → SSOT `assets/branding/logos/Logo 2.png`)* | Duplicado exacto verificado (SHA-256 `3CE90672DE6F...`). |
| `assets/captures/01..05_*.png` (5 capturas) | `assets/captures/01..05_*.png` | Preservadas en su ubicación canónica junto a `assets/branding/` y `assets/web-media/`. |

---

## 3. Alineación a Nomack Studio `v5.0.0 (CRSI-Ready)` y Hardening Cruzado

1. **Actualización de Gobernanza del Proyecto:** `AGENTS.md`, `README.md`, `.gitignore`, `pipeline/PROJECT_BUS.json`, `pipeline/handoffs/INIT_to_ALL_001_memory_brief.json` y `scripts/sync_workstation.ps1` actualizados a **`Nomack Studio v5.0.0`** desde la estación líder `HOST-02-MOBILE`.
2. **Clasificación de Memoria Local FTS5:** Se añadieron categorías `brand_assets` y `deliverables` en `scripts/update_project_memory.py` y se reconstruyó `knowledge/project_memory.sqlite` con auditoría anti-secretos *fail-closed*.
3. **Hardening ISO 27001 A.8.12 en Indexador Global (`../../bin/indexer.py`):** Se incorporaron `.secrets`, `backups`, `05_Servidor_Backups` y `backups_cpanel` a `EXCLUDED_DIRS` manteniendo íntegra la arquitectura `v5.0.0` (tablas SIM/CRSI) de `HOST-02-MOBILE`, seguido de reindexación y validación del contrato Handoff.
