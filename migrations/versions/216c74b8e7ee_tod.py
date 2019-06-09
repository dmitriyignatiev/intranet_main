"""'tod'

Revision ID: 216c74b8e7ee
Revises: 405dc6804a51
Create Date: 2019-03-13 10:52:46.271660

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '216c74b8e7ee'
down_revision = '405dc6804a51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('customer_inn', table_name='customer')
    op.drop_column('customer', 'customer_inn_1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('customer_inn_1', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_index('customer_inn', 'customer', ['customer_inn'], unique=True)
    # ### end Alembic commands ###
