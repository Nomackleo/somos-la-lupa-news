# La Lupa News (`somos-la-lupa-news`) — Gobernanza Local de Proyecto Desacoplado (Nomack Studio `v4.0.0`)

> **Proyecto:** `projects/la-lupa-news/` (Cuenta Exclusiva de Marca Personal — **Leonel Salcedo**)  
> **Cliente Corporativo:** **La Lupa News** · **CEO:** **Javier Fernández Franco**  
> **Repositorio GitHub:** `https://github.com/Nomackleo/somos-la-lupa-news.git`  
> **Hereda Gobernanza Raíz:** [`../../AGENTS.md`](../../AGENTS.md)  
> **Normas Aplicables:** `ISO 9001:2015 (Cl. 7.1.6 & 7.5)` · `ISO/IEC 27001:2022` · `ISO/IEC 25010:2023` · `ISO/IEC 42001:2023` · `NIST CSF 2.0`

---

## 1. Protocolo de Arranque Rápido para Modelos de IA (*Brief-First*)

Al iniciar cualquier sesión sobre este proyecto (tanto en **Desktop `HOST-01-STUDIO`** como en **Laptop Nitro `HOST-02-MOBILE`**), el modelo o agente **DEBE** cargar primero el contexto optimizado en este orden exacto antes de abrir archivos pesados:

1. **Pre-Flight Git Multi-Host:** Ejecutar `git fetch origin --prune` y comprobar `git rev-list --left-right --count HEAD...origin/main`.
2. **Estado Vivo (Blackboard):** Leer [`pipeline/PROJECT_BUS.json`](pipeline/PROJECT_BUS.json) y [`pipeline/handoffs/INIT_to_ALL_001_memory_brief.json`](pipeline/handoffs/INIT_to_ALL_001_memory_brief.json).
3. **Memoria Persistente Local:** Consultar [`knowledge/project_memory.json`](knowledge/project_memory.json), [`docs/04_bitacora_cambios/NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md`](docs/04_bitacora_cambios/NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md) o la base FTS5 local [`knowledge/project_memory.sqlite`](knowledge/project_memory.sqlite) (y `codebase-memory-mcp` bajo el scope `project:la-lupa-news`).
4. **Reglas de Estilo al Cliente:** Respetar de forma estricta [`GEMINI.md`](GEMINI.md) y [`.agents/rules/estilo-documental-la-lupa-news.md`](.agents/rules/estilo-documental-la-lupa-news.md).

---

## 2. Reglas Inviolables de Certificación ISO y Seguridad

1. **Aislamiento Estricto (Desacoplamiento):** Todos los documentos, scripts, activos, cotizaciones y memoria persistente de La Lupa News residen exclusivamente dentro de `projects/la-lupa-news/`. Prohibido escribir artefactos del proyecto en la raíz de Nomack Studio o en carpetas de otros clientes.
2. **Cero Secretos en Git ni en Memoria SQLite (ISO/IEC 27001:2022 A.8.12):**
   - Toda credencial, clave de WordPress, acceso de base de datos o hoja de accesos reside exclusivamente en `.secrets/` (100% excluida por `.gitignore`, `bin/indexer.py` y `scripts/update_project_memory.py`).
   - Los respaldos crudos de cPanel (`6.98 GB`, `.tar`, `.sql`, `wp-config.php`) permanecen fuera de Git y catalogados por metadatos en [`knowledge/backups_cold_storage_manifest.json`](knowledge/backups_cold_storage_manifest.json).
3. **Taxonomía Documental ISO 9001 Cláusula 7.5:** Todo documento técnico, especificación, auditoría o bitácora debe ubicarse bajo `docs/{01_gobernanza,02_especificaciones,03_auditorias_y_drift,04_bitacora_cambios}/` con codificación `NS-LLN-<TIPO>-<NNN>` y tabla de control documental.
4. **Segregación Estricta Multi-Cliente (Documentos hacia el Cliente):**
   - Autor exclusivo en entregables al cliente: **Leonel Salcedo — Dirección y Consultoría Tecnológica**.
   - Paleta oficial al cliente: **Morado `#2d124d`** + **Dorado `#b8842a`** + Portada de 9 niveles.
   - **Prohibición Absoluta en Entregables al Cliente:** Jamás usar `#1a3a5c`, jamás mencionar a Daniel Moncada ni a sociedades ajenas, y jamás usar el alias `"Nomack"` en documentos dirigidos a **Javier Fernández Franco**.
5. **Mantenimiento de Memoria Persistente:** Tras cualquier cambio relevante en el proyecto, ejecutar:
   ```powershell
   python scripts\update_project_memory.py
   python ..\..\bin\indexer.py
   ```
6. **Sincronización Multi-Estación (Desktop ↔ Laptop Nitro):** Usar [`scripts/sync_workstation.ps1`](scripts/sync_workstation.ps1) o el protocolo formal de [`docs/01_gobernanza/NS-LLN-GOV-003_PROTOCOLO_SEGURIDAD_Y_SINCRONIZACION.md`](docs/01_gobernanza/NS-LLN-GOV-003_PROTOCOLO_SEGURIDAD_Y_SINCRONIZACION.md). Prohibido `git push --force`, `git reset --hard` o `git add .` ciego.
