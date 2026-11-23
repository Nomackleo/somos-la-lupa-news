# Base de Conocimiento y Memoria Persistente Local — La Lupa News

> **Propósito:** Permitir que cualquier modelo de IA (en **Desktop `HOST-01-STUDIO`** o **Laptop Nitro `HOST-02-MOBILE`**) recupere el 100% del contexto crítico del proyecto **La Lupa News** en segundos, sin alucinaciones y con economía óptima de tokens (*Brief-First*).

## 1. Secuencia Óptima de Lectura (*Brief-First*)

1. [`../pipeline/PROJECT_BUS.json`](../pipeline/PROJECT_BUS.json) — Estado actual de fase, compuertas HITL y sincronización multi-host.
2. [`project_memory.json`](project_memory.json) — Mapa estructurado JSON (gobernanza, dominios, servidor, 93 CVEs, finanzas exactas, ADRs, backlog).
3. [`../docs/04_bitacora_cambios/NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md`](../docs/04_bitacora_cambios/NS-LLN-MEM-001_MEMORIA_PERSISTENTE_LA_LUPA_NEWS.md) — Narrativa canónica de memoria persistente (ISO 9001 Cl. 7.1.6).
4. [`project_memory.sqlite`](project_memory.sqlite) — Base SQLite FTS5 (`project_files`, `project_fts`, `project_facts`) consultable por cualquier agente o script Python.
5. [`backups_cold_storage_manifest.json`](backups_cold_storage_manifest.json) — Inventario auditado de respaldos fuera de Git (`6.98 GB` en almacenamiento frío).

## 2. Actualización y Consulta Determinista (`$0.00` Tokens)

```powershell
# Reindexar memoria persistente local (valida ausencia de secretos y recalcula SHA-256):
python scripts\update_project_memory.py

# Consultar la base FTS5 local por palabra clave:
python scripts\update_project_memory.py --query "FortiGuard OR Forminator"
```

## 3. Invariante de Seguridad ISO/IEC 27001:2022

- Esta carpeta **NUNCA** almacena contraseñas, tokens, claves API ni volcados SQL de usuarios.
- El indexador `scripts/update_project_memory.py` excluye estrictamente `.secrets/`, `backups/`, `*.sql`, `*.env` y aplica escaneo de patrones de secretos en modo *fail-closed*.
