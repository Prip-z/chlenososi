"""комментарий

Revision ID: e44bfbcccabf
Revises: 
Create Date: 2026-06-26 18:54:35.437651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import geoalchemy2


revision: str = 'e44bfbcccabf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('maps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pmtiles_url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maps_name'), 'maps', ['name'], unique=False)
    
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_token')
    )
    
    op.create_table('nodes',
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('map_id', sa.Integer(), nullable=False),
    sa.Column('is_walkable', sa.Boolean(), nullable=False),
    sa.Column('terrain_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['map_id'], ['maps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nodes_map_id'), 'nodes', ['map_id'], unique=False)
    
    op.create_table('edges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('map_id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['map_id'], ['maps.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['nodes.id'], ),
    sa.ForeignKeyConstraint(['target_id'], ['nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_edges_map_id'), 'edges', ['map_id'], unique=False)
    op.create_index(op.f('ix_edges_source_id'), 'edges', ['source_id'], unique=False)
    op.create_index(op.f('ix_edges_target_id'), 'edges', ['target_id'], unique=False)
    
    


def downgrade() -> None:
    op.drop_index(op.f('ix_edges_target_id'), table_name='edges')
    op.drop_index(op.f('ix_edges_source_id'), table_name='edges')
    op.drop_index(op.f('ix_edges_map_id'), table_name='edges')
    op.drop_table('edges')
    op.drop_index(op.f('ix_nodes_map_id'), table_name='nodes')
    op.drop_table('nodes')
    op.drop_table('user')
    op.drop_index(op.f('ix_maps_name'), table_name='maps')
    op.drop_table('maps')
