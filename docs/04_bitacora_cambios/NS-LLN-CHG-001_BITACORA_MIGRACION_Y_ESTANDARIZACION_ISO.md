# Bitácora de Migración Desacoplada y Estandarización ISO — La Lupa News (`NS-LLN-CHG-001`)

| Campo de Control ISO 9001 (Cláusula 7.5) | Valor Canónico |
| :--- | :--- |
| **Código de Documento** | `NS-LLN-CHG-001` |
| **Versión SemVer** | `1.0.0` |
| **Fecha de Emisión / Revisión** | `2026-11-23` |
| **Estado** | `Vigente` |
| **Autor / Aprobador** | `Leonel Salcedo (Dirección y Consultoría Tecnológica / HITL Lead)` |
| **Estación de Ejecución** | `NOMACK` (`HOST-01-STUDIO`) |
| **Marcos ISO Aplicables** | `ISO 9001:2015 (Cl. 7.1.6, 7.5, 8.5.6)` · `ISO/IEC 27001:2022` · `ISO/IEC 25010:2023` · `ISO/IEC 42001:2023` |

---

## 1. Resumen de la Intervención

Se ejecutó la migración no destructiva (copia íntegra con preservación de historial Git) del proyecto **La Lupa News** desde la ubicación heredada `D:\Work\lalupanews` hacia la ruta canónica desacoplada de Nomack Studio `v4.0.0`:

- **Ruta Canónica:** `projects/la-lupa-news/`
- **Respaldo de Origen (Zero Data Loss):** `D:\Work\lalupanews\` preservado íntegro sin alteraciones.
- **Repositorio Remoto Sincronizado:** `https://github.com/Nomackleo/somos-la-lupa-news.git` (rama `main`).

---

## 2. Matriz Forense de Reorganización de Activos

| Origen Heredado (`D:\Work\lalupanews\`) | Destino Canónico (`projects/la-lupa-news\`) | Acción / Justificación ISO |
| :--- | :--- | :--- |
| `docs/01_gobernanza/manual_estetica_y_ui_documental_la_lupa_news.md` | `docs/01_gobernanza/NS-LLN-GOV-002_MANUAL_ESTETICA_Y_UI_DOCUMENTAL.md` | `git mv` a codificación ISO 9001 Cl. 7.5 (`NS-LLN-GOV-002`). |
| `01_Documentacion/01_gobernanza/manual_estetica_y_ui_documental_la_lupa_news.md` | *(Eliminado en copia canónica)* | Duplicado exacto (SHA-256 `EFEE8127...`). |
| `01_Documentacion/templates/template_documento_ejecutivo_la_lupa_news.md` | *(Eliminado en copia canónica; SSOT en `templates/`)* | Duplicado exacto (SHA-256 `A1BAC0E2...`). |
| `01_Documentacion/NOMACK_STUDIO_STYLE_GUIDE.md` | *(Retirado / Superseded por `NS-LLN-GOV-002`)* | Contenía referencias obsoletas (`#ffd231`, `#07283d`, menciones societarias) en conflicto con `GEMINI.md`. |
| `01_Documentacion/negocio/*` | `docs/01_gobernanza/negocio/*` | `git mv` preservando historial. |
| `01_Documentacion/arquitectura/*` | `docs/02_especificaciones/arquitectura/*` | `git mv` preservando historial. |
| `01_Documentacion/auditoria/INFORME_TECNICO_AUDITORIA_SEGURIDAD_LA_LUPA_NEWS.md` | `docs/03_auditorias_y_drift/NS-LLN-AUD-001_AUDITORIA_SEGURIDAD_Y_VULNERABILIDADES.md` | Incorporado bajo taxonomía `03_auditorias_y_drift/` (antes untracked). |
| `02_Finanzas_Legal/comprobantes_pago/*` y `cuentas_de_cobro/*` | `finance/comprobantes_pago/*` y `finance/cuentas_de_cobro/*` | `git mv` preservando historial. |
| `02_Finanzas_Legal/cotizaciones/*` (excepto script) | `finance/cotizaciones/*` | Incorporado en control de versiones (antes untracked). |
| `02_Finanzas_Legal/cotizaciones/generate_docx.py` | `scripts/generate_quotation_docx.py` | Refactorizado con `Path(__file__).resolve()` para portabilidad Desktop ↔ Laptop Nitro. |
| `03_Branding_Media/*` | `assets/branding/*` | Incorporado (binarios pesados `.mp4`, `.psd`, `.rar`, `.zip` excluidos por `.gitignore`). |
| `04_Desarrollo_Web/demo_publicacion/*` | `assets/web-media/*` | Incorporado (`.mp4` excluido por `.gitignore`). |
| `04_Desarrollo_Web/plugins/*` y `themes/*` | `web/plugins/*` y `web/themes/*` | Paquetes `.zip` y documentación vendor excluidos de Git; activos ligeros y notas preservados. |
| `05_Servidor_Backups/accesos_restringidos/*` | `.secrets/*` *(LOCAL ONLY — GITIGNORED)* | Blindaje ISO 27001 A.8.12: aislado en `.secrets/`, excluido de Git y de ambos indexadores SQLite. |
| `05_Servidor_Backups/backups_cpanel/*` (`6.98 GB`) | Referenciado en `knowledge/backups_cold_storage_manifest.json` | Mantenido en almacenamiento en frío en `D:\Work\lalupanews\05_Servidor_Backups\backups_cpanel\` para evitar fugas PII/SQL y sobrecarga del repositorio Git. |

---

## 3. Artefactos Nuevos de Gobernanza ISO, Memoria Persistente y Sincronización

- `AGENTS.md` — Gobernanza local desacoplada y protocolo *Brief-First*.
- `docs/README.md` (`NS-LLN-DOC-000`) — Índice maestro ISO.
- `docs/01_gobernanza/NS-LLN-GOV-001_PLAN_MAESTRO_Y_GOBERNANZA_ISO.md` — Charter ISO 9001/27001/25010/42001.
- `docs/01_gobernanza/NS-LLN-GOV-003_PROTOCOLO_SEGURIDAD_Y_SINCRONIZACION.md` — Protocolo ISO 27001 + Multi-Host Desktop ↔ Laptop Nitro.
- `docs/02_especificaciones/NS-LLN-SPEC-001_ARQUITECTURA_PORTAL_Y_ESQUEMA.md` — Especificación de arquitectura y roadmap.
- `docs/04_bitacora_cambios/NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md` — Memoria persistente oficial.
- `knowledge/README.md`, `knowledge/project_memory.json`, `knowledge/backups_cold_storage_manifest.json`, `knowledge/project_memory.sqlite` — Base de conocimiento persistente autocontenida e indexada FTS5.
- `pipeline/PROJECT_BUS.json` y `pipeline/handoffs/INIT_to_ALL_001_memory_brief.json` — Bus Blackboard validado con `bin/handoff-validator.py`.
- `scripts/update_project_memory.py` y `scripts/sync_workstation.ps1` — Automatización determinista `$0.00` de memoria local y sincronización GitHub.
