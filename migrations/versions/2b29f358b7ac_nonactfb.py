"""'nonactfb'

Revision ID: 2b29f358b7ac
Revises: 7b3057289ed5
Create Date: 2019-03-27 11:25:40.640229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b29f358b7ac'
down_revision = '7b3057289ed5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('nonactf_buyer', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request', 'nonactf_buyer')
    # ### end Alembic commands ###
