"""stat

Revision ID: f3590c26372e
Revises: 6a71b4cf0300
Create Date: 2019-07-11 16:37:27.007865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3590c26372e'
down_revision = '6a71b4cf0300'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pre_fin', sa.Column('status', sa.String(length=240), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pre_fin', 'status')
    # ### end Alembic commands ###
