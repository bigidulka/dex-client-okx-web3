import json
from pathlib import Path


def test_endpoint_inventory_exists():
    data = json.loads(Path('endpoint_inventory.json').read_text())
    assert data['client']
    assert isinstance(data.get('endpoints'), list)
