# Especificación de Arquitectura del Portal y Esquema del Proyecto — La Lupa News (`NS-LLN-SPEC-001`)

| Campo de Control ISO 9001 (Cláusula 7.5) | Valor Canónico |
| :--- | :--- |
| **Código de Documento** | `NS-LLN-SPEC-001` |
| **Versión SemVer** | `1.0.0` |
| **Fecha de Emisión / Revisión** | `2026-11-23` |
| **Estado** | `Vigente` |
| **Autor / Aprobador** | `Leonel Salcedo (Dirección y Consultoría Tecnológica / HITL Lead)` |
| **Marcos ISO Aplicables** | `ISO/IEC 25010:2023` · `ISO 9001:2015 (Cl. 7.5)` · `ISO/IEC 27001:2022` |

---

## 1. Arquitectura de Producción Actual (Línea Base Auditada)

| Capa | Componente / Proveedor | Estado Auditado (`NS-LLN-AUD-001`) |
| :--- | :--- | :--- |
| **Dominio Oficial Activo** | `somoslalupanews.com` (GoDaddy, registrado `2026-10-21`) | Bloqueo temporal FortiGuard (*Newly Registered Domain*) pendiente de recategorización. |
| **Dominio Histórico** | `lalupanews.com` (DropCatch / NameBright / ParkLogic) | Capturado `2026-09-13` por terceros; 10 URLs residuales pendientes de saneamiento en BD. |
| **Alojamiento Web** | Hostinger — LiteSpeed (`82.29.158.129`, PHP `8.3.36`) | Fuga de cabeceras (`X-Powered-By`, `Server`), `allow_url_fopen=On`, falta HSTS/CSP/XFO. |
| **CMS & Tema** | WordPress Core `6.9.9` + Tema `JNews 12.0.4` | **28 CVEs en Core** + **1 CVE en tema**; actualización objetivo: Core `7.1.3+`. |
| **Plugins Críticos** | 40 plugins instalados (8 críticos vulnerables) | **64 CVEs en plugins** (Forminator `1.51.1` [38], Complianz `7.1.6` [13], Elementor `3.35.8` [6], CMB2 `2.11.0` [3], MC4WP `4.12.0` [2], Elementor Pro `3.35.1` [1], GTM4WP `1.22.3` [1]). |
| **Base de Datos** | MySQL `u459389234_e8taL` (~726 MB) | Respaldo previo obligatorio antes de cualquier intervención en Staging/Producción. |
| **Superficie API & Correo** | `/wp-json/wp/v2/users` abierto (91.3 KB); DMARC `p=none`, SPF `~all` | Exposición de usuarios y riesgo de spoofing; remediación definida en Fases 2 y 4. |

---

## 2. Arquitectura Objetivo de Evolución (Roadmap Escalonado `PROP-2026-LLN-SEC03`)

1. **Nivel 1 — Táctico *Investor-Ready* (\$380.000 / \$580.000 COP):** Desbloqueo FortiGuard, saneamiento DNS GoDaddy/Hostinger, cierre REST `/users` y parcheo de choque de brechas RCE.
2. **Nivel 2 — Remediación Integral Llave en Mano (\$3.600.000 COP):** Entorno Staging espejo, mitigación integral de las 93 vulnerabilidades, hardening PHP/HTTP Security Headers y certificación de parcheo.
3. **Nivel 3 — Continuidad DevSecOps (\$5.400.000 COP / 90 días):** Nivel 2 + monitoreo 24/7, mantenimiento mensual y respaldos externos verificados.
4. **Nivel 4 — Soberanía Tecnológica (\$9.800.000 COP):** Reemplazo definitivo de WordPress por backend editorial propietario ultraliviano con migración completa de histórico y cero licencias de terceros.

---

## 3. Esquema de Arquitectura del Repositorio Desacoplado

Los diagramas técnicos detallados y comparativas históricas de temas/costos se conservan bajo [`arquitectura/`](arquitectura/):
- `news-portal-architecture.mermaid`
- `wordpress-news-architecture.mermaid`
- `wordpress-news-final-architecture.mermaid`
- `news-portal-theme-comparison.md` / `wordpress-news-themes-comparison.md`
- `lalupanews-requerimientos.html` / `lalupanews-costs.html`
