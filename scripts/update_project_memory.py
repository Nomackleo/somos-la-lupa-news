#!/usr/bin/env python3
"""
La Lupa News — Local Persistent Memory Indexer (ISO 9001 Cl. 7.1.6 / ISO 27001 A.8.12)
======================================================================================
Builds and queries `knowledge/project_memory.sqlite` (FTS5 BM25) strictly scoped to
`projects/la-lupa-news/`, enabling instant Brief-First recall on any workstation
(Desktop HOST-01-STUDIO or Laptop Nitro HOST-02-MOBILE) at $0.00 token cost.

Security invariants (ISO/IEC 27001:2022):
- Strictly excludes `.secrets/`, `.git/`, `backups/`, `05_Servidor_Backups/`,
  vendor theme documentation, and binary/dump extensions.
- Fail-closed regex secret scanner aborts indexing if any API key, token, or
  private key header is detected in an indexable file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "knowledge" / "project_memory.sqlite"
MEMORY_JSON_PATH = PROJECT_ROOT / "knowledge" / "project_memory.json"

EXCLUDED_DIRS: Set[str] = {
    ".git",
    ".secrets",
    "backups",
    "05_Servidor_Backups",
    "backups_cpanel",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "scratch",
    "artifacts",
    ".gemini",
    ".vscode",
    ".idea",
}

EXCLUDED_PREFIXES: Tuple[str, ...] = (
    "web/themes/Documentation/",
)

INDEXABLE_EXTENSIONS: Set[str] = {
    ".md",
    ".json",
    ".py",
    ".ps1",
    ".sh",
    ".mermaid",
    ".yml",
    ".yaml",
    ".txt",
}

MAX_FILE_BYTES = 512 * 1024  # 512 KB cap to prevent bloat

SECRET_PATTERNS: Tuple[Tuple[str, re.Pattern[str]], ...] = (
    ("GOOGLE_API_KEY", re.compile(r"AIzaSy[0-9A-Za-z\-_]{33}")),
    ("GOOGLE_OAUTH_TOKEN", re.compile(r"ya29\.[0-9A-Za-z\-_]+")),
    ("GITHUB_PAT", re.compile(r"ghp_[0-9A-Za-z]{36}")),
    ("OPENAI_OR_GENERIC_SK", re.compile(r"\bsk-[0-9A-Za-z]{32,}\b")),
    ("PRIVATE_KEY_BLOCK", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)

MD_TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _classify_category(rel_posix: str) -> str:
    if rel_posix.startswith("docs/01_gobernanza/"):
        return "governance"
    if rel_posix.startswith("docs/02_especificaciones/"):
        return "specification"
    if rel_posix.startswith("docs/03_auditorias_y_drift/"):
        return "audit_security"
    if rel_posix.startswith("docs/04_bitacora_cambios/"):
        return "changelog_memory"
    if rel_posix.startswith("knowledge/"):
        return "knowledge_base"
    if rel_posix.startswith("pipeline/"):
        return "blackboard_pipeline"
    if rel_posix.startswith("finance/"):
        return "finance_commercial"
    if rel_posix.startswith("scripts/"):
        return "automation_scripts"
    if rel_posix.startswith(".agents/"):
        return "agent_rules_skills"
    if rel_posix.startswith("templates/"):
        return "templates"
    return "root_governance"


def _scan_secrets(rel_posix: str, text: str) -> None:
    if rel_posix == "scripts/update_project_memory.py":
        return  # Contains regex definitions themselves, not real secrets
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise RuntimeError(
                f"[ISO 27001 FAIL-CLOSED] Potential secret ({label}) detected in {rel_posix}. "
                "Remove secret or move file into .secrets/ before indexing."
            )


def _extract_title(rel_posix: str, text: str) -> str:
    m = MD_TITLE_RE.search(text)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()[:180]
    return Path(rel_posix).name


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode = DELETE;
        PRAGMA synchronous = FULL;

        DROP TABLE IF EXISTS project_fts;
        DROP TABLE IF EXISTS project_files;
        DROP TABLE IF EXISTS project_facts;
        DROP TABLE IF EXISTS index_meta;

        CREATE TABLE index_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE project_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rel_path TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            indexed_at_utc TEXT NOT NULL
        );

        CREATE VIRTUAL TABLE project_fts USING fts5(
            rel_path,
            category,
            title,
            summary,
            content,
            content='project_files',
            content_rowid='id',
            tokenize='porter unicode61 remove_diacritics 2'
        );

        CREATE TABLE project_facts (
            fact_key TEXT PRIMARY KEY,
            section TEXT NOT NULL,
            fact_json TEXT NOT NULL,
            updated_at_utc TEXT NOT NULL
        );
        """
    )


def _collect_files() -> List[Path]:
    collected: List[Path] = []
    for path in sorted(PROJECT_ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(PROJECT_ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        rel_posix = rel.as_posix()
        if any(rel_posix.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        if path.suffix.lower() not in INDEXABLE_EXTENSIONS:
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            continue
        collected.append(path)
    return collected


def build_index() -> Dict[str, object]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    files = _collect_files()
    now = _utc_now()

    rows: List[Tuple[str, str, str, str, int, str, str, str]] = []
    for abs_path in files:
        rel_posix = abs_path.relative_to(PROJECT_ROOT).as_posix()
        raw = abs_path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        _scan_secrets(rel_posix, text)
        digest = hashlib.sha256(raw).hexdigest()
        title = _extract_title(rel_posix, text)
        category = _classify_category(rel_posix)
        clean_lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("<!--")]
        summary = " ".join(clean_lines[:5])[:400]
        rows.append((rel_posix, category, title, digest, len(raw), summary, text, now))

    conn = sqlite3.connect(str(DB_PATH))
    try:
        _init_schema(conn)
        conn.executemany(
            """
            INSERT INTO project_files
                (rel_path, category, title, sha256, size_bytes, summary, content, indexed_at_utc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.execute("INSERT INTO project_fts(project_fts) VALUES('rebuild');")

        facts_count = 0
        if MEMORY_JSON_PATH.is_file():
            mem_data = json.loads(MEMORY_JSON_PATH.read_text(encoding="utf-8"))
            for section, value in mem_data.items():
                conn.execute(
                    "INSERT INTO project_facts (fact_key, section, fact_json, updated_at_utc) VALUES (?, ?, ?, ?)",
                    (f"memory.{section}", section, json.dumps(value, ensure_ascii=False), now),
                )
                facts_count += 1

        meta_items = [
            ("project_slug", "la-lupa-news"),
            ("schema_version", "1.0.0"),
            ("indexed_at_utc", now),
            ("indexed_files", str(len(rows))),
            ("indexed_facts", str(facts_count)),
        ]
        conn.executemany("INSERT INTO index_meta (key, value) VALUES (?, ?)", meta_items)
        conn.execute("INSERT INTO project_fts(project_fts) VALUES('integrity-check');")
        conn.commit()
        conn.execute("VACUUM;")
    finally:
        conn.close()

    return {
        "status": "OK",
        "db_path": str(DB_PATH),
        "indexed_files": len(rows),
        "indexed_facts": facts_count,
        "db_size_kb": round(DB_PATH.stat().st_size / 1024, 2),
        "indexed_at_utc": now,
    }


def query_index(query_text: str, limit: int = 8) -> List[Dict[str, object]]:
    if not DB_PATH.is_file():
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run without --query first.")
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        cur = conn.execute(
            """
            SELECT
                f.rel_path,
                f.category,
                f.title,
                bm25(project_fts, 4.0, 2.0, 6.0, 3.0, 1.0) AS rank_score,
                snippet(project_fts, 4, '[', ']', ' ... ', 24) AS match_snippet
            FROM project_fts
            JOIN project_files f ON f.id = project_fts.rowid
            WHERE project_fts MATCH ?
            ORDER BY rank_score
            LIMIT ?
            """,
            (query_text, limit),
        )
        return [
            {
                "rel_path": row[0],
                "category": row[1],
                "title": row[2],
                "bm25": round(float(row[3]), 4),
                "snippet": row[4],
            }
            for row in cur.fetchall()
        ]
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="La Lupa News local persistent memory SQLite FTS5 manager.")
    parser.add_argument("--query", "-q", type=str, default=None, help="Run an FTS5 BM25 query against local memory.")
    parser.add_argument("--limit", "-l", type=int, default=8, help="Max results for --query.")
    args = parser.parse_args()

    if args.query:
        results = query_index(args.query, limit=args.limit)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    report = build_index()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
