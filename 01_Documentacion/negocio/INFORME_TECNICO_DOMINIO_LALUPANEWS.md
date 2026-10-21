# <span style="color:#2D124D">INFORME TÉCNICO DE INFRAESTRUCTURA Y GOBERNANZA DIGITAL</span>
## Diagnóstico Forense y Estrategia de Rescate del Dominio `lalupanews.com`

---

**PARA:** Javier Fernández Franco — Director General & CEO, La Lupa News  
**DE:** Leonel Antonio Salcedo Acosta — Consultor Líder en Tecnología y Desarrollo, Nomack Studio  
**FECHA:** 21 de Octubre de 2026  
**ESTADO:** <span style="color:#ba1650">**CRÍTICO / ACCIÓN INMEDIATA REQUERIDA**</span>  
**SISTEMA VISUAL:** Manual de Documentación Nomack Studio (Paleta Morado Oscuro `#2D124D` · Rigor Forense ISO 25010)  

---

### 1.0 Resumen Ejecutivo

Estimado Javier,

Durante la auditoría técnica previa a la reactivación operativa del portal de noticias **La Lupa News**, se detectó que el sitio web no se encuentra en línea no por fallas en el servidor de Hostinger, sino debido a la **pérdida de la titularidad del dominio principal `lalupanews.com`**. 

El dominio no fue renovado a tiempo ante la entidad registradora internacional, agotó su período reglamentario de gracia y fue **capturado de manera automática por un servicio especializado de subastas internacionales (DropCatch)**, siendo transferido a un tercero el pasado mes de septiembre de 2026.

Actualmente, el código fuente, la base de datos de WordPress y todos los artículos desarrollados se encuentran **completamente seguros e intactos en el hosting**, pero la dirección web ya no pertenece a La Lupa News y está siendo explotada por terceros mediante una página de parqueo publicitario.

---

### 2.0 Auditoría y Verificación en Vivo (Soporte Oficial)

Para que puedas verificar directamente desde la base de datos pública de registros globales de ICANN la situación jurídica y técnica del dominio, puedes consultar el enlace oficial de la registradora actual:

🔗 **Enlace de Auditoría WHOIS en Vivo:**  
[https://www.namebright.com/whois/lalupanews.com](https://www.namebright.com/whois/lalupanews.com)

Al ingresar a dicho enlace, observarás los siguientes datos forenses irrefutables:
* **Registrador Acreditado:** `DropCatch.com 701 LLC` / `NameBright.com` (IANA ID: 2181).
* **Fecha de Registro / Captura:** 13 de Septiembre de 2026.
* **Fecha de Expiración Actual:** 13 de Septiembre de 2027 (renovado por el nuevo tenedor).
* **Estado de Protección:** `clientTransferProhibited` (bloqueado para transferencia sin autorización del nuevo propietario).
* **Servidores de Nombres (DNS):** `A.2NS.NET` y `B.2NS.NET` (no pertenecen a Hostinger).
* **Redirección de Tráfico (CNAME):** `pltraffic7.com` (red de tráfico comercial de anuncios).

---

### 3.0 Cronología de los Hechos: ¿Cómo se perdió el dominio?

```
[Vencimiento del Dominio] ──> [Período de Gracia Expirado] ──> [Liberación al Registro Central]
                                                                        │
                                                                        ▼
[Parqueo y Tráfico] <── [Venta en Subasta DropCatch: $64 USD] <── [Captura por Sniping Bot]
 (18 Sept 2026)                (17 Sept 2026)                       (13 Sept 2026)
```

1. **Vencimiento Inicial:** Al no efectuarse el pago oportuno de la anualidad del dominio, la entidad registradora inicial procedió a suspender los DNS y otorgar los 30 días reglamentarios de gracia.
2. **Caída al Registro (Drop):** Al vencerse el plazo sin pago de rescate, el dominio fue liberado a la raíz de Verisign.
3. **Captura por Sniping (13 de Septiembre de 2026):** Bots de alta velocidad de la compañía estadounidense **DropCatch** capturaron el dominio en milisegundos para monetizar su historial de visitas y marca.
4. **Subasta Pública (17 de Septiembre de 2026):** El dominio fue puesto en subasta competitiva en la plataforma de DropCatch y adjudicado al postor ganador por un monto de **$64 USD** (aprox. **$260.000 COP**).
5. **Alojamiento Actual (18 de Septiembre a la fecha):** El comprador final depositó el dominio en su cuenta de **NameBright.com** y configuró un servidor de parking publicitario (`pltraffic7.com`) para captar a los lectores habituales de La Lupa News y cobrar por clics.

---

### 4.0 Matriz de Riesgo y Consecuencias Comerciales

| Nivel de Riesgo | Factor de Impacto | Descripción Técnica y Comercial |
| :---: | :--- | :--- |
| <span style="color:#ba1650">**CRÍTICO**</span> | **Extorsión / Incremento de Precio** | Mientras más tiempo transcurra, el tenedor actual asumirá mayor valor de marca y podría solicitar miles de dólares por la recompra. |
| <span style="color:#ba1650">**CRÍTICO**</span> | **Pérdida de Reputación y Tráfico** | Cualquier usuario o anunciante que escriba `lalupanews.com` hoy en día ve páginas de spam y publicidad externa no autorizada. |
| <span style="color:#056c5c">**CONTROLADO**</span> | **Integridad del Portal Web** | La instalación de WordPress, temas licenciados (JNews), plugins y base de datos en Hostinger están intactos y respaldados. |

---

### 5.0 Plan de Acción: Protocolo de Rescate y Presupuesto Requerido

Para recuperar el activo digital y reanudar la operación del periódico digital, Nomack Studio liderará la siguiente estrategia técnica:

#### Vía A: Negociación Directa y Recompra ante NameBright (Recomendada)
* Abriremos una solicitud formal de intermediación (*Domain Brokerage Inquiry*) ante NameBright para presentar una oferta de adquisición al tenedor actual.
* **Costo histórico del postor:** $64 USD.
* **Margen de salida habitual del mercado:** Entre **$150 USD y $350 USD** (aprox. **$600.000 a $1.450.000 COP**), más el costo de transferencia y renovación inmediata por 2 años.
* **Fondo de Maniobra Solicitado para el Rescate:** **$1.500.000 COP ($350 USD)**.

#### Vía B: Plan de Contingencia Preventivo (Inmediato)
* Para proteger la operación y no detener el relanzamiento mientras se concreta la negociación con NameBright, registraremos de inmediato a nombre de la empresa una alternativa de alta autoridad:
  * `lalupanews.co` (Dominio territorial colombiano oficial).
  * `somoslalupanews.com`
* **Costo de contingencia:** Menos de **$60.000 COP anuales** en Hostinger.

---

### 6.0 Requerimiento Financiero para Ejecución

Para iniciar formalmente el proceso de intermediación y compra del dominio ante NameBright y salvaguardar la identidad digital de La Lupa News, solicitamos autorizar y girar los siguientes recursos:

| Concepto Técnico | Monto (USD) | Monto Estimado (COP) |
| :--- | :---: | :---: |
| **Fondo de Negociación y Recompra de Dominio (NameBright / Tenedor)** | $350.000 USD | $1.450.000 COP |
| **Registro Preventivo de Contingencia en Hostinger (`.co`)** | $12.00 USD | $50.000 COP |
| **TOTAL FONDO DE RECUPERACIÓN DIGITAL** | **$362.00 USD** | **$1.500.000 COP** |

*(Cualquier excedente no utilizado en la negociación con el tenedor será acreditado directamente a favor de La Lupa News).*

Quedo atento a tu aprobación y confirmación de la transferencia para aperturar la oferta formal en NameBright de inmediato.

Atentamente,

**Leonel Antonio Salcedo Acosta**  
Líder Técnico & Arquitectura Digital — Nomack Studio  
C.C. 1.022.943.003 de Bogotá  
Móvil / WhatsApp: 322 373 6685  
Email: nomackleo@gmail.com
