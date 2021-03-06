"""empty message

Revision ID: fa07a4b138d0
Revises: 
Create Date: 2019-11-25 08:22:12.325283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa07a4b138d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agg_number',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('numb', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inn', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer_base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('finance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('dtae', sa.DateTime(), nullable=True),
    sa.Column('new_cost', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('incoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('new_sup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.Column('path', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quantity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tr_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inn', sa.String(length=10), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('truck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('truck_opt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ttn',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('role', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=120), nullable=True),
    sa.Column('request_count', sa.Integer(), nullable=True),
    sa.Column('user_email', sa.String(length=240), nullable=True),
    sa.Column('last_message_read_time', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=240), nullable=True),
    sa.Column('competention', sa.String(length=240), nullable=True),
    sa.Column('active', sa.Integer(), nullable=True),
    sa.Column('fio', sa.String(length=240), nullable=True),
    sa.Column('mobile', sa.String(length=120), nullable=True),
    sa.Column('external', sa.String(length=120), nullable=True),
    sa.Column('start_work', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('who_number',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('agreements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Text(), nullable=True),
    sa.Column('path', sa.Text(), nullable=True),
    sa.Column('shipper_name', sa.Text(), nullable=True),
    sa.Column('shipper_address', sa.Text(), nullable=True),
    sa.Column('shipper_phone', sa.Text(), nullable=True),
    sa.Column('cnee_name', sa.Text(), nullable=True),
    sa.Column('cnee_address', sa.Text(), nullable=True),
    sa.Column('cnee_phone', sa.Text(), nullable=True),
    sa.Column('cargo', sa.Text(), nullable=True),
    sa.Column('date_loading', sa.DateTime(), nullable=True),
    sa.Column('date_unloading', sa.DateTime(), nullable=True),
    sa.Column('driver', sa.Text(), nullable=True),
    sa.Column('date_order', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.Column('phone', sa.String(length=240), nullable=True),
    sa.Column('email', sa.String(length=240), nullable=True),
    sa.Column('payment_day', sa.Integer(), nullable=True),
    sa.Column('dm', sa.String(length=240), nullable=True),
    sa.Column('payment_terms', sa.String(length=240), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('customer_base', sa.String(length=240), nullable=True),
    sa.Column('customer_character', sa.String(length=120), nullable=True),
    sa.Column('customer_inn', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    op.create_table('paid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('summ', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('finance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['finance'], ['finance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('agreement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation', sa.DateTime(), nullable=True),
    sa.Column('date', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_agreement', sa.DateTime(), nullable=True),
    sa.Column('filename', sa.String(length=120), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('customer_name', sa.String(length=240), nullable=True),
    sa.Column('number', sa.String(length=240), nullable=True),
    sa.Column('choice', sa.String(length=240), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('count'),
    sa.UniqueConstraint('customer_name')
    )
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('cost_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=True),
    sa.Column('rate_idea', sa.Integer(), nullable=True),
    sa.Column('redirect_comment', sa.String(length=120), nullable=True),
    sa.Column('direction', sa.String(length=120), nullable=True),
    sa.Column('cost_created', sa.DateTime(), nullable=True),
    sa.Column('dest', sa.String(length=120), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('customer_name', sa.String(length=120), nullable=True),
    sa.Column('payment_day', sa.Integer(), nullable=True),
    sa.Column('cargo_type', sa.String(length=120), nullable=True),
    sa.Column('cargo_desciption', sa.String(length=120), nullable=True),
    sa.Column('cargo_value', sa.String(length=120), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('Truck_type', sa.String(length=120), nullable=True),
    sa.Column('ttn', sa.String(length=140), nullable=True),
    sa.Column('type_of_loading', sa.String(length=120), nullable=True),
    sa.Column('type_of_truck', sa.String(length=120), nullable=True),
    sa.Column('weigth_cargo', sa.Integer(), nullable=True),
    sa.Column('request_comments', sa.Text(), nullable=True),
    sa.Column('pick_up_date', sa.DateTime(), nullable=True),
    sa.Column('request_status', sa.String(length=120), nullable=True),
    sa.Column('request_order', sa.String(length=120), nullable=True),
    sa.Column('truck_available_opt', sa.Integer(), nullable=True),
    sa.Column('dogovor_zayavka', sa.Integer(), nullable=True),
    sa.Column('deadline_buyer', sa.DateTime(), nullable=True),
    sa.Column('deadline_sale', sa.DateTime(), nullable=True),
    sa.Column('questions', sa.String(length=800), nullable=True),
    sa.Column('actual', sa.String(length=120), nullable=True),
    sa.Column('min_sale', sa.Integer(), nullable=True),
    sa.Column('quest', sa.String(length=120), nullable=True),
    sa.Column('nonactf_buyer', sa.Integer(), nullable=True),
    sa.Column('test_new', sa.Integer(), nullable=True),
    sa.Column('complete_fin', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supplier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('llc', sa.String(length=240), nullable=True),
    sa.Column('llc_name', sa.String(length=240), nullable=True),
    sa.Column('legal_add', sa.String(length=240), nullable=True),
    sa.Column('fact_address', sa.String(length=240), nullable=True),
    sa.Column('inn', sa.String(length=240), nullable=True),
    sa.Column('kpp', sa.String(length=240), nullable=True),
    sa.Column('ogrn', sa.String(length=240), nullable=True),
    sa.Column('bank', sa.String(length=240), nullable=True),
    sa.Column('bik', sa.String(length=240), nullable=True),
    sa.Column('rc', sa.String(length=240), nullable=True),
    sa.Column('kc', sa.String(length=240), nullable=True),
    sa.Column('driver_director', sa.String(length=240), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('finance', sa.Integer(), nullable=True),
    sa.Column('pay', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['finance'], ['finance.id'], ),
    sa.ForeignKeyConstraint(['pay'], ['paid.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('agreement_supplier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation', sa.DateTime(), nullable=True),
    sa.Column('date', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_agreement', sa.DateTime(), nullable=True),
    sa.Column('filename', sa.String(length=120), nullable=True),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('supplier_name', sa.String(length=240), nullable=True),
    sa.Column('number', sa.String(length=240), nullable=True),
    sa.Column('choice', sa.String(length=240), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('count'),
    sa.UniqueConstraint('supplier_name')
    )
    op.create_table('comp_supp',
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], )
    )
    op.create_table('costs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('direction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post', sa.Text(), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_post_date'), 'posts', ['post_date'], unique=False)
    op.create_table('prefin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('req_id', sa.Integer(), nullable=True),
    sa.Column('tora_red', sa.String(length=120), nullable=True),
    sa.Column('direction', sa.String(length=120), nullable=True),
    sa.Column('sale', sa.String(length=120), nullable=True),
    sa.Column('buyer', sa.String(length=120), nullable=True),
    sa.Column('status_of_request', sa.String(length=120), nullable=True),
    sa.Column('blank_option_1', sa.String(length=120), nullable=True),
    sa.Column('customer_name', sa.String(length=120), nullable=True),
    sa.Column('customer_accept_invoice_status', sa.String(length=120), nullable=True),
    sa.Column('customer_order_number', sa.String(length=120), nullable=True),
    sa.Column('customer_order_date', sa.DateTime(), nullable=True),
    sa.Column('customer_order_month', sa.Integer(), nullable=True),
    sa.Column('loading_place', sa.String(length=120), nullable=True),
    sa.Column('loading_date', sa.DateTime(), nullable=True),
    sa.Column('cargo_character', sa.Text(), nullable=True),
    sa.Column('unloading_place', sa.String(length=120), nullable=True),
    sa.Column('unloading_date', sa.DateTime(), nullable=True),
    sa.Column('supplier_name', sa.String(length=120), nullable=True),
    sa.Column('s_invoice_number', sa.String(length=120), nullable=True),
    sa.Column('ttn_cmr_available', sa.String(length=120), nullable=True),
    sa.Column('s_inv_amount', sa.Float(), nullable=True),
    sa.Column('s_inv_vat', sa.Text(), nullable=True),
    sa.Column('s_inv_currency', sa.String(length=120), nullable=True),
    sa.Column('s_prepaid_amount', sa.Integer(), nullable=True),
    sa.Column('s_prepaid_data', sa.DateTime(), nullable=True),
    sa.Column('cost_with_vat', sa.Integer(), nullable=True),
    sa.Column('cost_pochta', sa.Integer(), nullable=True),
    sa.Column('cost_final', sa.Integer(), nullable=True),
    sa.Column('cost_we_still_need_pay', sa.Integer(), nullable=True),
    sa.Column('s_inv_status_payment', sa.String(length=120), nullable=True),
    sa.Column('s_inv_credit_terms', sa.Integer(), nullable=True),
    sa.Column('s_credit_terms_scan_org', sa.String(length=120), nullable=True),
    sa.Column('s_inv_status', sa.String(length=120), nullable=True),
    sa.Column('blank_option_2', sa.String(length=120), nullable=True),
    sa.Column('s_inv_act_date_payment', sa.DateTime(), nullable=True),
    sa.Column('s_invoice_transit_name', sa.String(length=120), nullable=True),
    sa.Column('c_inv_number', sa.String(length=120), nullable=True),
    sa.Column('c_invoice_date', sa.DateTime(), nullable=True),
    sa.Column('c_inv_amount', sa.String(length=120), nullable=True),
    sa.Column('c_inv_currency', sa.String(length=120), nullable=True),
    sa.Column('c_invfacture_number', sa.String(length=120), nullable=True),
    sa.Column('c_invfacture_data', sa.DateTime(), nullable=True),
    sa.Column('c_inv_issue', sa.String(length=120), nullable=True),
    sa.Column('c_ems_tracking', sa.String(length=120), nullable=True),
    sa.Column('c_inv_post_send_data', sa.DateTime(), nullable=True),
    sa.Column('c_inv_plan_pay', sa.DateTime(), nullable=True),
    sa.Column('c_inv_week_plan_pay', sa.Integer(), nullable=True),
    sa.Column('c_inv_status_payment', sa.String(length=120), nullable=True),
    sa.Column('c_inv_act_pay_date', sa.DateTime(), nullable=True),
    sa.Column('profit', sa.Integer(), nullable=True),
    sa.Column('month_number', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('s_inv_put_reestr', sa.Integer(), nullable=True),
    sa.Column('s_np_ati', sa.String(length=120), nullable=True),
    sa.Column('s_inv_part_payment_16wk', sa.Integer(), nullable=True),
    sa.Column('s_inv_part_pay_issue', sa.String(length=120), nullable=True),
    sa.Column('blank_option_3', sa.String(length=120), nullable=True),
    sa.Column('s_inv_part_payment_29wk_2019', sa.Integer(), nullable=True),
    sa.Column('blank_option_4', sa.String(length=120), nullable=True),
    sa.Column('s_inv_part_march_2019', sa.Integer(), nullable=True),
    sa.Column('blank_option_5', sa.String(length=120), nullable=True),
    sa.Column('blank_option_6', sa.String(length=120), nullable=True),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('vat', sa.Integer(), nullable=True),
    sa.Column('pochta_full_cost', sa.Integer(), nullable=True),
    sa.Column('s_inv_date_to_pay', sa.DateTime(), nullable=True),
    sa.Column('s_inv_date', sa.DateTime(), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('req_id')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subs',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.Text(), nullable=True),
    sa.Column('req_id', sa.Integer(), nullable=True),
    sa.Column('prefin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prefin_id'], ['prefin.id'], ),
    sa.ForeignKeyConstraint(['req_id'], ['request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('finsup',
    sa.Column('prefin_id', sa.Integer(), nullable=True),
    sa.Column('supp_ip', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prefin_id'], ['prefin.id'], ),
    sa.ForeignKeyConstraint(['supp_ip'], ['supplier.id'], )
    )
    op.create_table('invoicecust',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fin_id', sa.Integer(), nullable=True),
    sa.Column('path', sa.Text(), nullable=True),
    sa.Column('prefin_id', sa.Integer(), nullable=True),
    sa.Column('req_id', sa.Integer(), nullable=True),
    sa.Column('invoice_number', sa.Text(), nullable=True),
    sa.Column('invoice_amount', sa.Float(), nullable=True),
    sa.Column('invoice_date', sa.DateTime(), nullable=True),
    sa.Column('invoice_deadline_payment', sa.DateTime(), nullable=True),
    sa.Column('invoice_tracking_number', sa.Text(), nullable=True),
    sa.Column('invoice_tracking_company', sa.Text(), nullable=True),
    sa.Column('invoice_tracking_day', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['prefin_id'], ['prefin.id'], ),
    sa.ForeignKeyConstraint(['req_id'], ['request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pochta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track_number', sa.String(length=500), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('fin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fin_id'], ['prefin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supp_payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_inv_number', sa.String(length=120), nullable=True),
    sa.Column('s_invoice_date', sa.DateTime(), nullable=True),
    sa.Column('s_inv_amount', sa.Integer(), nullable=True),
    sa.Column('s_inv_currency', sa.String(length=120), nullable=True),
    sa.Column('s_inv_pay_day', sa.DateTime(), nullable=True),
    sa.Column('s_payment_summ', sa.Integer(), nullable=True),
    sa.Column('bank', sa.String(length=240), nullable=True),
    sa.Column('tora_red', sa.String(length=240), nullable=True),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('fin_id', sa.Integer(), nullable=True),
    sa.Column('day_plan_pay', sa.DateTime(), nullable=True),
    sa.Column('vat', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['fin_id'], ['prefin.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tn',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.Text(), nullable=True),
    sa.Column('req_id', sa.Integer(), nullable=True),
    sa.Column('prefin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prefin_id'], ['prefin.id'], ),
    sa.ForeignKeyConstraint(['req_id'], ['request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('zayvka',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('req_id', sa.Integer(), nullable=True),
    sa.Column('path', sa.Text(), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.Column('prefin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prefin_id'], ['prefin.id'], ),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice_payment_c',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('summ', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('invoice_number', sa.Text(), nullable=True),
    sa.Column('invoicecust_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['invoicecust_id'], ['invoicecust.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice_payment_s',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_inv_number', sa.String(length=120), nullable=True),
    sa.Column('summ_pay', sa.Integer(), nullable=True),
    sa.Column('transit', sa.String(length=120), nullable=True),
    sa.Column('date_payment', sa.DateTime(), nullable=True),
    sa.Column('supp_payment', sa.Integer(), nullable=True),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('commision', sa.Float(), nullable=True),
    sa.Column('cost_for_us', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['supp_payment'], ['supp_payment.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoicesup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fin_id', sa.Integer(), nullable=True),
    sa.Column('path', sa.Text(), nullable=True),
    sa.Column('prefin_id', sa.Integer(), nullable=True),
    sa.Column('req_id', sa.Integer(), nullable=True),
    sa.Column('supp_id', sa.Integer(), nullable=True),
    sa.Column('supp_payment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prefin_id'], ['prefin.id'], ),
    sa.ForeignKeyConstraint(['req_id'], ['request.id'], ),
    sa.ForeignKeyConstraint(['supp_id'], ['supplier.id'], ),
    sa.ForeignKeyConstraint(['supp_payment_id'], ['supp_payment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tr_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sum', sa.Integer(), nullable=True),
    sa.Column('transit_id', sa.Integer(), nullable=True),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('transit_date_send', sa.DateTime(), nullable=True),
    sa.Column('transit_date_recieved', sa.DateTime(), nullable=True),
    sa.Column('doc_path', sa.Text(), nullable=True),
    sa.Column('confirm', sa.Integer(), nullable=True),
    sa.Column('commision', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['invoice_payment_s.id'], ),
    sa.ForeignKeyConstraint(['transit_id'], ['transit.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tr_payments')
    op.drop_table('invoicesup')
    op.drop_table('invoice_payment_s')
    op.drop_table('invoice_payment_c')
    op.drop_table('zayvka')
    op.drop_table('tn')
    op.drop_table('supp_payment')
    op.drop_table('pochta')
    op.drop_table('invoicecust')
    op.drop_table('finsup')
    op.drop_table('documents')
    op.drop_table('subs')
    op.drop_table('status')
    op.drop_table('prefin')
    op.drop_index(op.f('ix_posts_post_date'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('direction')
    op.drop_table('costs')
    op.drop_table('comp_supp')
    op.drop_table('agreement_supplier')
    op.drop_table('supplier')
    op.drop_table('request')
    op.drop_table('agreement')
    op.drop_table('paid')
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_table('message')
    op.drop_table('customer')
    op.drop_table('bank')
    op.drop_table('agreements')
    op.drop_table('who_number')
    op.drop_table('user')
    op.drop_table('ttn')
    op.drop_table('truck_opt')
    op.drop_table('truck')
    op.drop_table('transit')
    op.drop_table('tr_status')
    op.drop_table('quantity')
    op.drop_table('new_sup')
    op.drop_table('incoice')
    op.drop_table('finance')
    op.drop_table('customer_base')
    op.drop_table('companies')
    op.drop_table('agg_number')
    # ### end Alembic commands ###
