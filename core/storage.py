import json
from django.conf import settings
from pathlib import Path
from typing import List, Dict, Any

def _ensure_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        if path.suffix == '.json':
            path.write_text('[]', encoding='utf-8')
        else:
            path.write_text('', encoding='utf-8')

def read_json(path: Path) -> List[Dict[str, Any]]:
    _ensure_file(path)
    try:
        return json.loads(path.read_text(encoding='utf-8') or '[]')
    except json.JSONDecodeError:
        return []

def write_json(path: Path, data: List[Dict[str, Any]]):
    _ensure_file(path)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')

def log(action: str):
    _ensure_file(settings.LOG_FILE)
    with open(settings.LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(action.strip() + '\n')

def next_id(items: List[Dict[str, Any]]) -> int:
    return (max([i.get('id', 0) for i in items]) + 1) if items else 1
