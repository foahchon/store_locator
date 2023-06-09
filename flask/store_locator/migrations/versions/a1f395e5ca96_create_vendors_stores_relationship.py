"""Create vendors_stores relationship

Revision ID: a1f395e5ca96
Revises: bc6b2fec8776
Create Date: 2023-02-21 22:05:18.519387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1f395e5ca96'
down_revision = 'bc6b2fec8776'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vendors_stores',
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('store_id', 'vendor_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vendors_stores')
    # ### end Alembic commands ###
