"""new

Revision ID: bfde02925828
Revises: c3e17cb5f703
Create Date: 2019-07-20 13:23:50.496040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bfde02925828'
down_revision = 'c3e17cb5f703'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pre_fin', sa.Column('req_id', sa.Integer(), nullable=True))
    op.add_column('pre_fin', sa.Column('supplier_id', sa.Integer(), nullable=True))
    op.add_column('pre_fin', sa.Column('vat', sa.Integer(), nullable=True))
    op.drop_index('ix_pre_fin_id', table_name='pre_fin')
    op.create_unique_constraint(None, 'pre_fin', ['req_id'])
    op.create_foreign_key(None, 'pre_fin', 'supplier', ['supplier_id'], ['id'])
    op.drop_column('pre_fin', 'Unnamed: 75')
    op.drop_column('pre_fin', 'Unnamed: 74')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pre_fin', sa.Column('Unnamed: 74', mysql.TEXT(), nullable=True))
    op.add_column('pre_fin', sa.Column('Unnamed: 75', mysql.DOUBLE(asdecimal=True), nullable=True))
    op.drop_constraint(None, 'pre_fin', type_='foreignkey')
    op.drop_constraint(None, 'pre_fin', type_='unique')
    op.create_index('ix_pre_fin_id', 'pre_fin', ['id'], unique=False)
    op.drop_column('pre_fin', 'vat')
    op.drop_column('pre_fin', 'supplier_id')
    op.drop_column('pre_fin', 'req_id')
    # ### end Alembic commands ###
