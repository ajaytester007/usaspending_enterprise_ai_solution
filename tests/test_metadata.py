import json
from pathlib import Path

def test_metadata_catalog_exists():
    path = Path('config/metadata_catalog.json')
    assert path.exists()
    data = json.loads(path.read_text())
    assert 'layers' in data
    assert 'entities' in data
