"""tr_comp

Revision ID: f1a28d83034f
Revises: acca149ab211
Create Date: 2019-10-17 19:50:31.023169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f1a28d83034f'
down_revision = 'acca149ab211'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_payment_s', sa.Column('transit', sa.String(length=120), nullable=True))
    op.drop_constraint('transit_ibfk_1', 'transit', type_='foreignkey')
    op.drop_column('transit', 'status')
    op.drop_column('transit', 'payment_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transit', sa.Column('payment_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('transit', sa.Column('status', mysql.TEXT(), nullable=True))
    op.create_foreign_key('transit_ibfk_1', 'transit', 'invoice_payment_s', ['payment_id'], ['id'])
    op.drop_column('invoice_payment_s', 'transit')
    # ### end Alembic commands ###
