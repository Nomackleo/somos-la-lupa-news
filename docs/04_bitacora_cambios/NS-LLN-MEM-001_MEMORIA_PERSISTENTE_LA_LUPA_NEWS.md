# Memoria Persistente del Proyecto — La Lupa News (`NS-LLN-MEM-001`)

| Campo de Control ISO 9001 (Cláusula 7.5) | Valor Canónico |
| :--- | :--- |
| **Código de Documento** | `NS-LLN-MEM-001` |
| **Versión SemVer** | `1.0.0` |
| **Fecha de Emisión / Revisión** | `2026-11-23` |
| **Estado** | `Vigente` |
| **Autor / Aprobador** | `Leonel Salcedo (Dirección y Consultoría Tecnológica / HITL Lead)` |
| **Marcos ISO Aplicables** | `ISO 9001:2015 (Cl. 7.1.6 & 7.5)` · `ISO/IEC 27001:2022` · `ISO/IEC 25010:2023` · `ISO/IEC 42001:2023` |

> **Sincronización Agéntica:** Memoria autocontenida en [`knowledge/project_memory.json`](../../knowledge/project_memory.json) + [`knowledge/project_memory.sqlite`](../../knowledge/project_memory.sqlite) y sincronizada globalmente con `mcp/codebase-memory-mcp` (`project:la-lupa-news`).

---

## 1. Propósito de la Memoria Persistente

Este registro consolida de forma verificable el contexto institucional, el estado forense de infraestructura y ciberseguridad, la conciliación financiera exacta, las decisiones de arquitectura (**ADR**) y los guardrails obligatorios del proyecto **La Lupa News** (`projects/la-lupa-news/`). Permite que cualquier modelo de IA en **Desktop (`HOST-01-STUDIO`)** o **Laptop Nitro (`HOST-02-MOBILE`)** arranque con conocimiento preciso, cero alucinaciones y consumo mínimo de tokens.

---

## 2. Identidad de Cuenta y Reglas de Oro (No Negociables)

- **Cliente:** **La Lupa News** · **CEO:** **Javier Fernández Franco**.
- **Categoría de Cuenta:** **Marca Personal Exclusiva de Leonel Salcedo** (Categoría B).
- **Autor Oficial en Entregables al Cliente:** `Leonel Salcedo — Dirección y Consultoría Tecnológica`.
- **Paleta Oficial al Cliente:** Morado `#2d124d` (primario y negritas), Morado Profundo `#220d3a` (contraste), Dorado `#b8842a` (separadores y numeraciones), Cuerpo `#222222` (Cambria 11pt justificado), Metadatos `#777777`, Portada de 9 niveles.
- **Anti-Patrones Prohibidos hacia el Cliente:** ❌ Jamás usar `#1a3a5c`, ❌ Jamás mencionar a Daniel Moncada ni sociedades ajenas, ❌ Jamás usar el alias `"Nomack"` en documentos entregados a Javier Fernández Franco.

---

## 3. Línea Base de Infraestructura y Ciberseguridad (Oct–Nov 2026)

| Dimensión | Estado Verificado | Referencia Canónica |
| :--- | :--- | :--- |
| **Dominio Activo** | `somoslalupanews.com` registrado en **GoDaddy** el `2026-10-21` (\$11.99 USD / ~\$50.000 COP). | `docs/01_gobernanza/negocio/INFORME_TECNICO_DOMINIO_LALUPANEWS.md` |
| **Dominio Histórico** | `lalupanews.com` capturado por DropCatch (`2026-09-13`) y subastado (`2026-09-17`, \$64 USD); actualmente parqueado en `pltraffic7.com` (`ns4/ns5.dnsauthority.com`). Existen 10 URLs residuales en BD. | `docs/03_auditorias_y_drift/NS-LLN-AUD-001_AUDITORIA_SEGURIDAD_Y_VULNERABILIDADES.md` |
| **Servidor & Stack** | **Hostinger LiteSpeed** (`82.29.158.129`), `PHP 8.3.36`, **WordPress `6.9.9`**, **JNews `12.0.4`**, MySQL `u459389234_e8taL` (~726 MB), 40 plugins instalados. | `NS-LLN-SPEC-001` & `NS-LLN-AUD-001` |
| **Postura CVE** | **93 vulnerabilidades documentadas (Nivel CRÍTICO):** 28 en WP Core `6.9.9` (SQLi, LFI→RCE, XSS→RCE, REST Batch), 64 en 8 plugins activos (Forminator `1.51.1` [38], Complianz `7.1.6` [13], Elementor `3.35.8` [6], CMB2 [3], MC4WP [2], Elementor Pro [1], GTM4WP [1]), 1 en tema JNews. | `NS-LLN-AUD-001` |
| **Exposición Perimetral** | Bloqueo **FortiGuard NRD**; REST `/wp-json/wp/v2/users` abierto (91.3 KB); `X-Powered-By` / `Server` expuestos; `allow_url_fopen=On`; sin HSTS/XFO/CSP; registro `ftp` expone IP origen; DMARC `p=none`, SPF `~all`. | `NS-LLN-AUD-001` |
| **Regla Operativa Activa** | **Solo diagnóstico no invasivo hasta Gate 1 (aprobación comercial HITL).** Ninguna modificación en producción autorizada aún. | `NS-LLN-GOV-001` |

---

## 4. Conciliación Financiera y Portafolio Comercial Vigente

### 4.1. Balance Contable Histórico (Corte `2026-10-21`)
- **Honorarios Ciclo 1 (2024–2025):** Causado `\$2.500.000` | Abonado `\$0` | Pendiente `\$2.500.000` (Vencido).
- **Honorarios Ciclo 2 (2025):** Causado `\$2.500.000` | Abonado `\$2.000.000` (`2026-10-09`) | Pendiente `\$500.000`.
- **Fondo Dominio GoDaddy (`2026-10-21`):** Giro recibido `\$200.000` | Registro `\$50.000` | Saldo a favor cliente `-\$150.000`.
- **Balance Neto Consolidado Exigible:** **`\$2.850.000 COP`** (`\$3.000.000` honorarios netos menos `\$150.000` remanente dominio).
- **Fuente:** [`finance/cuentas_de_cobro/INFORME_AUDITORIA_FINANCIERA_LALUPANEWS.md`](../../finance/cuentas_de_cobro/INFORME_AUDITORIA_FINANCIERA_LALUPANEWS.md).

### 4.2. Cotización de Remediación Activa (`PROP-2026-LLN-SEC03`)
- **Nivel 1A (Desbloqueo & DNS):** `\$380.000 COP` (2–3 días hábiles).
- **Nivel 1B (Investor-Ready & BMV — Recomendado Rondas):** `\$580.000 COP` (3–4 días hábiles; 100% acreditable si sube a Nivel 2 en 45 días).
- **Nivel 2 (Remediación Integral 93 CVEs + Staging):** `\$3.600.000 COP` (7–10 días hábiles).
- **Nivel 3 (Integral + Póliza DevSecOps 90 días):** `\$5.400.000 COP`.
- **Nivel 4 (Backend Editorial Propio — Cero WordPress):** `\$9.800.000 COP` (4–6 semanas).
- **Fuente:** [`finance/cotizaciones/COTIZACION_ACTUALIZACION_SEGURIDAD_SOMOSLALUPANEWS.md`](../../finance/cotizaciones/COTIZACION_ACTUALIZACION_SEGURIDAD_SOMOSLALUPANEWS.md).

---

## 5. Registro de Decisiones de Arquitectura (ADR)

| ID ADR | Fecha | Decisión | Justificación Técnica / ISO |
| :--- | :---: | :--- | :--- |
| **ADR-LLN-001** | `2026-10-21` | Adquisición de `somoslalupanews.com` vía GoDaddy | Mitigación de pérdida de `lalupanews.com` (capturado por DropCatch) sin sobrecostos de rescate. |
| **ADR-LLN-002** | `2026-10-22` | Estandarización de guía visual cliente en Morado `#2d124d` + Dorado `#b8842a` | Segregación estricta de Marca Personal respecto a cuentas societarias (`#1a3a5c`). |
| **ADR-LLN-003** | `2026-10-28` | Auditoría forense no invasiva + cotización escalonada en 4 niveles (`PROP-2026-LLN-SEC03`) | Trazabilidad objetiva de 93 CVEs antes de intervenir producción y viabilidad comercial *Investor-Ready*. |
| **ADR-LLN-004** | `2026-11-23` | Migración desacoplada a `projects/la-lupa-news/` bajo taxonomía ISO 9001 Cl. 7.5 (`docs/01..04`) | Cumplimiento de `rules/architecture-directory-governance-standards.md`, eliminación de duplicados y purga de guía heredada conflictiva (`NOMACK_STUDIO_STYLE_GUIDE.md`). |
| **ADR-LLN-005** | `2026-11-23` | Bóveda `.secrets/` local + manifiesto de respaldos en frío (`6.98 GB` en `D:\Work\lalupanews\05_Servidor_Backups\`) | Cumplimiento **ISO/IEC 27001:2022 A.8.12**: cero contraseñas, dumps `.sql` o archivos `.tar` en GitHub ni en SQLite. |
| **ADR-LLN-006** | `2026-11-23` | Memoria persistente dual: local autocontenida (`knowledge/project_memory.json` + `project_memory.sqlite` FTS5) + global (`codebase_memory.sqlite`) | Continuidad inmediata entre **Desktop (`HOST-01-STUDIO`)** y **Laptop Nitro (`HOST-02-MOBILE`)** con `$0.00` de costo de indexación. |

---

## 6. Guardrails Activos y Backlog Prioritario

1. **Nunca exponer `.secrets/` ni backups crudos:** Verificar siempre que `.secrets/`, `*.sql`, `*.tar*`, `*.zip`, `*.rar` estén ignorados por Git antes de cualquier commit.
2. **Rutas portables multi-estación:** Todo script en `scripts/` debe usar `Path(__file__).resolve()` (prohibido hardcodear `D:\Work\lalupanews\`).
3. **Actualización obligatoria de memoria:** Al cerrar cada hito, ejecutar `python scripts\update_project_memory.py` y actualizar `pipeline/PROJECT_BUS.json` + este archivo `NS-LLN-MEM-001`.
4. **Próximos hitos pendientes (post Gate 1):**
   - Recibir confirmación de Javier Fernández Franco sobre plan `PROP-2026-LLN-SEC03` y conciliación de cartera.
   - Ejecutar Fase 1 (desbloqueo FortiGuard + saneamiento DNS GoDaddy/Hostinger + 10 URLs residuales).
   - Clonar `Nomackleo/somos-la-lupa-news` en **Laptop Nitro (`HOST-02-MOBILE`)** bajo `projects/la-lupa-news/`.
