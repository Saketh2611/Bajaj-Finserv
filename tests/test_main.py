import sys
from pathlib import Path

# Add project root to Python path so 'main' is importable
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_extract_endpoint_exists():
    response = client.post("/extract-bill-data", json={"document": "dummy"})
    assert response.status_code in [200, 500]

def test_invalid_input():
    response = client.post("/extract-bill-data", json={})
    assert response.status_code == 422
