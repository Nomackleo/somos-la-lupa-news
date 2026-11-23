# Índice Maestro Documental ISO — La Lupa News (`NS-LLN-DOC-000`)

| Campo de Control ISO 9001 (Cláusula 7.5) | Valor Canónico |
| :--- | :--- |
| **Código de Documento** | `NS-LLN-DOC-000` |
| **Versión SemVer** | `1.0.0` |
| **Fecha de Emisión / Revisión** | `2026-11-23` |
| **Estado** | `Vigente` |
| **Autor / Aprobador** | `Leonel Salcedo (Dirección y Consultoría Tecnológica / HITL Lead)` |
| **Marcos ISO Aplicables** | `ISO 9001:2015 (Cl. 7.5)` · `ISO/IEC 27001:2022` · `ISO/IEC 25010:2023` · `ISO/IEC 42001:2023` |

---

## 1. Taxonomía Canónica de Información Documentada

| Carpeta ISO | Código | Documento | Propósito |
| :--- | :--- | :--- | :--- |
| `01_gobernanza/` | `NS-LLN-GOV-001` | [`NS-LLN-GOV-001_PLAN_MAESTRO_Y_GOBERNANZA_ISO.md`](01_gobernanza/NS-LLN-GOV-001_PLAN_MAESTRO_Y_GOBERNANZA_ISO.md) | Carta de gobernanza ISO 9001/27001/25010/42001, matriz RACI/HITL y segregación de cuenta. |
| `01_gobernanza/` | `NS-LLN-GOV-002` | [`NS-LLN-GOV-002_MANUAL_ESTETICA_Y_UI_DOCUMENTAL.md`](01_gobernanza/NS-LLN-GOV-002_MANUAL_ESTETICA_Y_UI_DOCUMENTAL.md) | Manual oficial de estética y maquetación documental para entregables al cliente (`#2d124d` + `#b8842a`). |
| `01_gobernanza/` | `NS-LLN-GOV-003` | [`NS-LLN-GOV-003_PROTOCOLO_SEGURIDAD_Y_SINCRONIZACION.md`](01_gobernanza/NS-LLN-GOV-003_PROTOCOLO_SEGURIDAD_Y_SINCRONIZACION.md) | Controles ISO/IEC 27001:2022, bóveda `.secrets/` y sincronización GitHub Desktop ↔ Laptop Nitro. |
| `01_gobernanza/negocio/` | — | `INFORME_TECNICO_DOMINIO_LALUPANEWS.*`, propuestas y plan de trabajo | Soportes históricos de negocio, dominio `somoslalupanews.com` y propuesta IA. |
| `02_especificaciones/` | `NS-LLN-SPEC-001` | [`NS-LLN-SPEC-001_ARQUITECTURA_PORTAL_Y_ESQUEMA.md`](02_especificaciones/NS-LLN-SPEC-001_ARQUITECTURA_PORTAL_Y_ESQUEMA.md) | Especificación de arquitectura del portal, topología DNS/Hostinger y nomenclaturas del proyecto. |
| `02_especificaciones/arquitectura/` | — | Diagramas `.mermaid`, comparativas de temas y requerimientos HTML | Artefactos de arquitectura web y comparativas WordPress/JNews. |
| `03_auditorias_y_drift/` | `NS-LLN-AUD-001` | [`NS-LLN-AUD-001_AUDITORIA_SEGURIDAD_Y_VULNERABILIDADES.md`](03_auditorias_y_drift/NS-LLN-AUD-001_AUDITORIA_SEGURIDAD_Y_VULNERABILIDADES.md) | Dictamen pericial de ciberseguridad: 93 CVEs, bloqueo FortiGuard NRD y plan de remediación en 4 fases. |
| `04_bitacora_cambios/` | `NS-LLN-CHG-001` | [`NS-LLN-CHG-001_BITACORA_MIGRACION_Y_ESTANDARIZACION_ISO.md`](04_bitacora_cambios/NS-LLN-CHG-001_BITACORA_MIGRACION_Y_ESTANDARIZACION_ISO.md) | Bitácora forense de migración desacoplada a `projects/la-lupa-news/` y estandarización ISO. |
| `04_bitacora_cambios/` | `NS-LLN-MEM-001` | [`NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md`](04_bitacora_cambios/NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md) | Memoria persistente oficial del proyecto (ADRs, estado técnico, cartera y guardrails para modelos IA). |

---

## 2. Repositorios Complementarios de Conocimiento y Finanzas

- **Memoria Persistente Estructurada:** [`../knowledge/project_memory.json`](../knowledge/project_memory.json) y base FTS5 [`../knowledge/project_memory.sqlite`](../knowledge/project_memory.sqlite).
- **Bus de Estado Agéntico (Blackboard):** [`../pipeline/PROJECT_BUS.json`](../pipeline/PROJECT_BUS.json).
- **Finanzas y Conciliación:** [`../finance/`](../finance/) (`cotizaciones/`, `cuentas_de_cobro/`, `comprobantes_pago/`).
- **Plantillas Ejecutivas:** [`../templates/template_documento_ejecutivo_la_lupa_news.md`](../templates/template_documento_ejecutivo_la_lupa_news.md).
