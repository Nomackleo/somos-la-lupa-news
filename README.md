# somos-la-lupa-news

> **Portal Digital, Arquitectura Web y Estrategia Tecnológica — La Lupa News**  
> Repositorio oficial de gobernanza técnica, arquitectura documental y entregables estratégicos.

---

## 1. Gobernanza Institucional y Dirección del Proyecto

| Rol | Entidad / Responsable |
| :--- | :--- |
| **Cliente Corporativo** | **La Lupa News** |
| **CEO del Cliente** | **Javier Fernández Franco** |
| **Dirección & Consultoría Tecnológica** | **Leonel Salcedo** |
| **Estado del Repositorio** | En Producción / Sincronización Multi-Estación Activa |

---

## 2. Identidad Visual Documental & Paleta Oficial

Todo documento formal, manual o reporte técnico emitido en este repositorio debe respetar de forma estricta la paleta de identidad corporativa establecida:

- **Morado Marca Personal (`#2d124d`)**: Títulos H1/H2, nodos principales y negritas institucionales.
- **Morado Profundo (`#220d3a`)**: Énfasis tipográfico y alto contraste.
- **Dorado Institucional (`#b8842a`)**: Filetes horizontales, numeraciones, viñetas y etiquetas de acento.
- **Cuerpo de Texto (`#222222`)**: Fuente Cambria 11pt, interlineado 1.15, texto justificado.

---

## 3. Estructura del Repositorio

```text
somos-la-lupa-news/
├── .gitignore
├── GEMINI.md                    # Reglas obligatorias de estilo y contexto para agentes de IA
├── README.md                    # Documentación general del repositorio y gobernanza
├── docs/
│   └── 01_gobernanza/
│       └── manual_estetica_y_ui_documental_la_lupa_news.md   # Manual canónico de maquetación y estilo
└── templates/
    └── template_documento_ejecutivo_la_lupa_news.md         # Plantilla oficial con portada de 9 niveles
```

---

## 4. Guía de Sincronización Multi-Estación (Desktop / Laptop)

Para garantizar consistencia entre estaciones de trabajo (Desktop y Laptop):

### A. Al comenzar una jornada en una estación:
```bash
git fetch origin
git pull --rebase origin main
```

### B. Al finalizar o commitear avances:
```bash
git status
git add .
git commit -m "feat(docs): actualizar entregables y gobernanza técnica"
git push origin main
```

---

## 5. Confidencialidad y Derechos

Documentación y código desarrollados para **La Lupa News** bajo la dirección de su CEO **Javier Fernández Franco**.  
Consultoría Tecnológica & Transformación Digital liderada por **Leonel Salcedo**. Todos los derechos reservados.
