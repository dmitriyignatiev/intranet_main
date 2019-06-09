"""'request_status'

Revision ID: e7958a49dea4
Revises: 5e6050b7954d
Create Date: 2019-01-18 11:51:54.744917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7958a49dea4'
down_revision = '5e6050b7954d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('request_order', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request', 'request_order')
    # ### end Alembic commands ###
