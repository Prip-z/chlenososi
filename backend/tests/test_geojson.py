import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.util.geojson import to_geojson


def test_geojson_conversion():
    nodes = [{'id': 1, 'lat': 55.0, 'lon': 37.0, 'is_walkable': True, 'terrain_type': 'road'}]
    edges = []
    result = to_geojson(nodes, edges)
    
    assert result['type'] == 'FeatureCollection'
    assert result['features'][0]['geometry']['type'] == 'Point'
    assert result['features'][0]['geometry']['coordinates'] == [37.0, 55.0]
    assert result['features'][0]['properties']['lat'] == 55.0
    assert result['features'][0]['properties']['lon'] == 37.0

test_geojson_conversion()