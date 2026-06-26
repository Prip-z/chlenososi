CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE maps (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pmtiles_url VARCHAR(500) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nodes (
    id VARCHAR(50) PRIMARY KEY,
    map_id INT REFERENCES maps(id) ON DELETE CASCADE,
    geom GEOMETRY(Point, 4326), 
    is_walkable BOOLEAN DEFAULT TRUE,
    terrain_type VARCHAR(50) DEFAULT 'dirt_trail'
);

CREATE INDEX nodes_geom_idx ON nodes USING GIST(geom);

CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    map_id INT REFERENCES maps(id) ON DELETE CASCADE,
    source_id VARCHAR(50) REFERENCES nodes(id) ON DELETE CASCADE,
    target_id VARCHAR(50) REFERENCES nodes(id) ON DELETE CASCADE,
    weight FLOAT NOT NULL
);

CREATE INDEX edges_source_idx ON edges(source_id);
CREATE INDEX edges_target_idx ON edges(target_id);