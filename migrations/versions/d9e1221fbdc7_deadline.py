"""'deadline'

Revision ID: d9e1221fbdc7
Revises: 216c74b8e7ee
Create Date: 2019-03-13 11:33:51.357403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9e1221fbdc7'
down_revision = '216c74b8e7ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('deadline_buyer', sa.DateTime(), nullable=True))
    op.add_column('request', sa.Column('deadline_sale', sa.DateTime(), nullable=True))
    op.add_column('request', sa.Column('questions', sa.String(length=240), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request', 'questions')
    op.drop_column('request', 'deadline_sale')
    op.drop_column('request', 'deadline_buyer')
    # ### end Alembic commands ###