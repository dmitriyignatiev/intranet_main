"""req_d

Revision ID: 5e3ecf32efed
Revises: 2963e2857f53
Create Date: 2019-07-28 12:32:55.383368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e3ecf32efed'
down_revision = '2963e2857f53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'documents', 'request', ['req_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    # ### end Alembic commands ###
