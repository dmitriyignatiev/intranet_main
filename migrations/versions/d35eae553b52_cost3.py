"""cost3

Revision ID: d35eae553b52
Revises: 8a114e9c77f2
Create Date: 2019-06-02 15:06:19.344919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd35eae553b52'
down_revision = '8a114e9c77f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('summ', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('finance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['finance'], ['finance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('finance', sa.Column('new_cost', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('finance', 'new_cost')
    op.drop_table('paid')
    # ### end Alembic commands ###