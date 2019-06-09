"""Payd off

Revision ID: 497b91dbdf53
Revises: 5ae73f6dbef5
Create Date: 2019-06-02 08:39:35.425536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '497b91dbdf53'
down_revision = '5ae73f6dbef5'
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
    op.add_column('finance', sa.Column('cost', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('finance', 'cost')
    op.drop_table('paid')
    # ### end Alembic commands ###
