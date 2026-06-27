def to_geojson(nodes: list, edges: list):
    features = []

    node_coords = {node['id']: [node['lon'], node['lat']] for node in nodes}
    
    for node in nodes:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [node['lon'], node['lat']]
            },
            "properties": {
                "id": node['id'],
                "lon": node['lon'],
                "lat": node['lat'],
                "is_walkable": node['is_walkable'],
                "terrain_type": node['terrain_type']
            }
        })
        
    for edge in edges:
        src_id = edge['source_id'] if isinstance(edge, dict) else edge.source_id
        tgt_id = edge['target_id'] if isinstance(edge, dict) else edge.target_id
        
        src_coords = node_coords.get(src_id)
        tgt_coords = node_coords.get(tgt_id)
        
        if src_coords and tgt_coords:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [src_coords, tgt_coords]
                },
                "properties": {
                    "id": edge['id'] if isinstance(edge, dict) else edge.id,
                    "weight": edge.get('weight', 0) if isinstance(edge, dict) else edge.weight
                }
            })

    return {
        "type": "FeatureCollection",
        "features": features
    }