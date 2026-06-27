def to_geojson(nodes: list, edges: list):
    features = []
    
    # Превращаем ноды в GeoJSON Points
    for node in nodes:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [node['lon'], node['lat']]
            },
            "properties": {
                "id": node['id'],
                "is_walkable": node['is_walkable'],
                "terrain_type": node['terrain_type']
            }
        })
        
    # Превращаем эджи в LineStrings (упрощенно)
    for edge in edges:
        # Внимание: здесь нужно найти координаты source и target
        # Это потребует доработки запроса или поиска по списку нод
        pass 

    return {
        "type": "FeatureCollection",
        "features": features
    }