# Plan Maestro y Gobernanza ISO — Proyecto La Lupa News (`NS-LLN-GOV-001`)

| Campo de Control ISO 9001 (Cláusula 7.5) | Valor Canónico |
| :--- | :--- |
| **Código de Documento** | `NS-LLN-GOV-001` |
| **Versión SemVer** | `1.0.0` |
| **Fecha de Emisión / Revisión** | `2026-11-23` |
| **Estado** | `Vigente` |
| **Autor / Aprobador** | `Leonel Salcedo (Dirección y Consultoría Tecnológica / HITL Lead)` |
| **Marcos ISO Aplicables** | `ISO 9001:2015 (Cl. 7.1.6 & 7.5)` · `ISO/IEC 27001:2022` · `ISO/IEC 25010:2023` · `ISO/IEC 42001:2023` |

---

## 1. Propósito y Alcance del Sistema de Gestión del Proyecto

Este documento establece la arquitectura de gobernanza, nomenclatura documental, controles de seguridad de la información y gestión del conocimiento organizacional para el proyecto desacoplado **`projects/la-lupa-news/`** (repositorio `somos-la-lupa-news`), garantizando que cada entregable técnico, financiero, editorial o de infraestructura sea auditable y certificable bajo estándares internacionales.

### 1.1. Clasificación de Cuenta y Segregación Legal
- **Tipo de Cuenta:** Categoría B — Cliente Exclusivo de Marca Personal (**Leonel Salcedo**).
- **Cliente Corporativo:** **La Lupa News** (`somoslalupanews.com`).
- **Destinatario Ejecutivo:** **Javier Fernández Franco** (CEO — La Lupa News).
- **Regla de Segregación:** Aislamiento total respecto a cuentas societarias externas. Todo entregable emitido hacia el cliente cumple estrictamente [`NS-LLN-GOV-002_MANUAL_ESTETICA_Y_UI_DOCUMENTAL.md`](NS-LLN-GOV-002_MANUAL_ESTETICA_Y_UI_DOCUMENTAL.md) y [`../../GEMINI.md`](../../GEMINI.md).

---

## 2. Matriz de Cumplimiento de Normas ISO Aplicables

| Norma Internacional | Cláusula / Control | Implementación Verificable en `projects/la-lupa-news/` |
| :--- | :--- | :--- |
| **ISO 9001:2015** | Cláusula 7.1.6 (Conocimiento Organizacional) | Memoria persistente estructurada en `knowledge/project_memory.json`, `knowledge/project_memory.sqlite` y `docs/04_bitacora_cambios/NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md`. |
| **ISO 9001:2015** | Cláusula 7.5 (Información Documentada) | Taxonomía obligatoria de 4 carpetas en `docs/` con codificación única `NS-LLN-<TIPO>-<NNN>`, tabla de metadatos SemVer y bitácora cronológica `NS-LLN-CHG-*`. |
| **ISO/IEC 27001:2022** | A.5.8, A.8.12, A.8.19, A.8.20 | Aislamiento de credenciales en `.secrets/` (excluida de Git y de indexadores), bloqueo de dumps `.sql`/backups en `.gitignore`, escáner determinista anti-secretos en `scripts/update_project_memory.py` y remediación planificada de 93 CVEs (`NS-LLN-AUD-001`). |
| **ISO/IEC 25010:2023** | Modularidad, Mantenibilidad, Portabilidad | Proyecto 100% desacoplado bajo `projects/la-lupa-news/` con repositorio Git independiente, rutas relativas portables (`Path(__file__).resolve()`) y eliminación de duplicados. |
| **ISO/IEC 42001:2023** | Gobernanza de Sistemas de IA y Supervisión HITL | Compuertas HITL explícitas en `pipeline/PROJECT_BUS.json`, contratos validados con `bin/handoff-validator.py` y carga controlada de contexto (*Brief-First*). |
| **Ley 1581 de 2012 (CO)** | Protección de Datos Personales (PII) | Prohibición de exponer bases de datos de usuarios, contraseñas o volcados productivos en repositorios o índices de memoria de modelos IA. |

---

## 3. Convención de Nomenclatura de Activos y Documentos

| Tipo de Artefacto | Patrón Obligatorio | Ejemplo Canónico |
| :--- | :--- | :--- |
| **Directorio de Proyecto** | `kebab-case` bajo `projects/` | `projects/la-lupa-news/` |
| **Documentos de Gobernanza** | `NS-LLN-GOV-<NNN>_<NOMBRE_MAYUSCULAS>.md` | `NS-LLN-GOV-001_PLAN_MAESTRO_Y_GOBERNANZA_ISO.md` |
| **Especificaciones Técnicas** | `NS-LLN-SPEC-<NNN>_<NOMBRE_MAYUSCULAS>.md` | `NS-LLN-SPEC-001_ARQUITECTURA_PORTAL_Y_ESQUEMA.md` |
| **Auditorías y Deriva** | `NS-LLN-AUD-<NNN>_<NOMBRE_MAYUSCULAS>.md` | `NS-LLN-AUD-001_AUDITORIA_SEGURIDAD_Y_VULNERABILIDADES.md` |
| **Bitácoras de Cambio** | `NS-LLN-CHG-<NNN>_<NOMBRE_MAYUSCULAS>.md` | `NS-LLN-CHG-001_BITACORA_MIGRACION_Y_ESTANDARIZACION_ISO.md` |
| **Memoria Persistente** | `NS-LLN-MEM-<NNN>_<NOMBRE_MAYUSCULAS>.md` | `NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md` |
| **Commits Git** | Conventional Commits v1.0.0 + `Host-Origin` + `Ref-Project` | `feat(governance): ...` |

---

## 4. Matriz RACI y Compuertas HITL (Human-in-the-Loop)

| Compuerta / Decisión | Responsable (R) | Aprobador HITL (A) | Evidencia Requerida |
| :--- | :--- | :--- | :--- |
| **Gate 0 — Gobernanza y Migración ISO** | Agente Arquitecto / ISO | Leonel Salcedo | Taxonomía `docs/`, memoria SQLite validada, Watchdog `PASS`. |
| **Gate 1 — Aprobación Comercial Cliente** | Leonel Salcedo | Javier Fernández Franco | Aceptación de plan Nivel 1–4 (`PROP-2026-LLN-SEC03`) y conciliación de cartera. |
| **Gate 2 — Intervención en Producción / DNS** | Equipo Técnico / DevSecOps | Leonel Salcedo | Backup verificado SHA-256 previo, entorno Staging aprobado, cero cambios sin autorización. |
| **Gate 3 — Certificación de Parcheo y Cierre** | Auditoría Independiente (Goldfish) | Leonel Salcedo | Reporte `NS-LLN-AUD-002` con `0` CVEs críticas, FortiGuard desbloqueado y actualización de memoria. |
