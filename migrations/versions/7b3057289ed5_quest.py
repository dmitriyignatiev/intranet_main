"""'quest'

Revision ID: 7b3057289ed5
Revises: 4940e4b24002
Create Date: 2019-03-25 16:43:59.885409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b3057289ed5'
down_revision = '4940e4b24002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('quest', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request', 'quest')
    # ### end Alembic commands ###
