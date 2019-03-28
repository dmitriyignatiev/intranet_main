"""'rr'

Revision ID: 93fa63d7dd77
Revises: e7958a49dea4
Create Date: 2019-02-18 12:54:10.236902

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '93fa63d7dd77'
down_revision = 'e7958a49dea4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('request_order', sa.String(length=120), nullable=True))
    op.add_column('request', sa.Column('truck_available_opt', sa.Integer(), nullable=True))
    op.drop_column('request', 'truck_available')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('truck_available', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('request', 'truck_available_opt')
    op.drop_column('request', 'request_order')
    # ### end Alembic commands ###
