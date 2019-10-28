"""'k'

Revision ID: 8d7cd2859161
Revises: 9bb9b639ab4d
Create Date: 2019-10-23 20:24:48.835703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d7cd2859161'
down_revision = '9bb9b639ab4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tr_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tr_status')
    # ### end Alembic commands ###
