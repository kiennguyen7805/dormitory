"""Guard the runtime persistence boundary: repositories call stored functions only."""

import ast
from pathlib import Path
import re

import dormitory_infrastructure


PERSISTENCE_ROOT = Path(dormitory_infrastructure.__file__).parent / "persistence"
DIRECT_DML = re.compile(r"\b(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM)\b", re.IGNORECASE)
SELECT = re.compile(r"\bSELECT\b", re.IGNORECASE)
STORED_CALL = re.compile(r"\bpublic\.fn_[a-z_]+\s*\(", re.IGNORECASE)


def test_repositories_only_call_postgres_functions() -> None:
    # Scan Python runtime code, not migration/SQL definitions: those must access tables.
    sources = sorted((PERSISTENCE_ROOT / "repositories").glob("*.py"))
    assert sources
    for source in sources:
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            sql = node.value
            assert not DIRECT_DML.search(sql), f"Direct table write in {source.name}:{node.lineno}"
            if SELECT.search(sql):
                assert STORED_CALL.search(sql), (
                    f"SELECT must call a stored function in {source.name}:{node.lineno}"
                )
