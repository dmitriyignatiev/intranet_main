"""'fin_cust'

Revision ID: 961d830a009c
Revises: 52ffcaa009f4
Create Date: 2019-09-13 20:26:46.754640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '961d830a009c'
down_revision = '52ffcaa009f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoicecust', sa.Column('customer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'invoicecust', 'customer', ['customer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invoicecust', type_='foreignkey')
    op.drop_column('invoicecust', 'customer_id')
    # ### end Alembic commands ###
