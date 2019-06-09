"""newCost

Revision ID: 8a114e9c77f2
Revises: 67dedcb01352
Create Date: 2019-06-02 09:07:36.029825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a114e9c77f2'
down_revision = '67dedcb01352'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('finance', sa.Column('cost', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('finance', 'cost')
    # ### end Alembic commands ###
