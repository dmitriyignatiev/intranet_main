"""cookies

Revision ID: a2b78a33629c
Revises: b4d90f3f8595
Create Date: 2019-07-13 17:17:47.836053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2b78a33629c'
down_revision = 'b4d90f3f8595'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documents', sa.Column('req_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('documents', 'req_id')
    # ### end Alembic commands ###
