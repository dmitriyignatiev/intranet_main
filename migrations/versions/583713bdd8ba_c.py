"""'c'

Revision ID: 583713bdd8ba
Revises: b9af47a09df9
Create Date: 2019-09-17 18:53:55.915276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '583713bdd8ba'
down_revision = 'b9af47a09df9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_payment_c', sa.Column('customer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'invoice_payment_c', 'customer', ['customer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invoice_payment_c', type_='foreignkey')
    op.drop_column('invoice_payment_c', 'customer_id')
    # ### end Alembic commands ###