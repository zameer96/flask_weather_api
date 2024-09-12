"""Add initial city data

Revision ID: 38b679fc05d0
Revises: b54146ac3372
Create Date: 2024-09-12 19:22:41.146392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, Integer, String, Float


# revision identifiers, used by Alembic.
revision = '38b679fc05d0'
down_revision = 'b54146ac3372'
branch_labels = None
depends_on = None



def upgrade():
    city_table = table(
        'city',
        column('id', Integer),
        column('name', String),
        column('lat', Float),
        column('long', Float)
    )
    op.bulk_insert(
        city_table,
        [
            {"name": "New York", "lat": 40.7128, "long": -74.0060},
            {"name": "London", "lat": 51.5074, "long": -0.1278},
            {"name": "Tokyo", "lat": 35.6762, "long": 139.6503},
            {"name": "Paris", "lat": 48.8566, "long": 2.3522},
            {"name": "Sydney", "lat": -33.8688, "long": 151.2093},
            {"name": "Berlin", "lat": 52.5200, "long": 13.4050},
            {"name": "Moscow", "lat": 55.7558, "long": 37.6173},
            {"name": "Calgary", "lat": 51.0447, "long": -114.0719},
            {"name": "Waterloo", "lat": 43.4643, "long": -80.5204},
            {"name": "Edmonton", "lat": 53.5461, "long": -113.4938}
        ]
    )

def downgrade():
    op.execute('DELETE FROM city')