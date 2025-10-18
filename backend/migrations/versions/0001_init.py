from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('barcode', sa.String(64), index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('brand', sa.String(255)),
        sa.Column('ingredients_text', sa.Text()),
        sa.Column('nutriscore', sa.String(5)),
        sa.Column('nova_group', sa.Integer()),
        sa.Column('nutrition', JSON())
    )
    op.create_table(
        'evaluations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
        sa.Column('score', sa.Float, nullable=False),
        sa.Column('issues', JSON()),
        sa.Column('rules_snapshot', JSON())
    )
    op.create_table(
        'rules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(128)),
        sa.Column('exclude_ingredients', JSON()),
        sa.Column('max_sugars_g_per_100g', sa.Float()),
        sa.Column('max_salt_g_per_100g', sa.Float())
    )

def downgrade():
    op.drop_table('evaluations')
    op.drop_table('products')
    op.drop_table('rules')
