"""newSupTest

Revision ID: b3a7b98a5605
Revises: 9aa8b1bf3c20
Create Date: 2019-06-10 15:28:30.264609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3a7b98a5605'
down_revision = '9aa8b1bf3c20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('new_sup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('new_sup')
    # ### end Alembic commands ###
