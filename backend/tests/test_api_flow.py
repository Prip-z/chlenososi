import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
import os
from unittest.mock import AsyncMock
from app.core.s3 import s3_storage
import pytest

@pytest.fixture(autouse=True)
def mock_s3():
    s3_storage.upload_file = AsyncMock(return_value="http://localhost/fake-url.pmtiles")

os.environ["S3_ENDPOINT"] = "http://localhost:9000"
test_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(test_dir, "data", "test_map.pmtiles")

client = TestClient(app)

def test_full_map_creation_flow():
    # 1. Загрузка карты
    with open("test_map.pmtiles", "rb") as f:
        response = client.post("/api/v1/maps", data={"name": "Test Map"}, files={"file": f})
    assert response.status_code == 200
    map_id = response.json()["id"]

    # 2. Создание ноды
    node_res = client.post("/api/v1/nodes", json={"map_id": map_id, "lat": 55.0, "lon": 37.0, "is_walkable": True, "terrain_type": "road"})
    assert node_res.status_code == 200
    node_id = node_res.json()["id"]

    # 3. Финальная проверка (GeoJSON ручка)
    geo_res = client.post(f"/api/v1/maps/{map_id}/geojson", json={"min_lon": 0, "min_lat": 0, "max_lon": 180, "max_lat": 90})
    assert geo_res.status_code == 200
    assert "FeatureCollection" in geo_res.json()["type"]