import os
from mailmerge import MailMerge
from sqlalchemy import desc

from werkzeug.utils import secure_filename
from flask import render_template, flash, url_for, redirect, request
from flask import send_from_directory

from app_main import app
from flask_login import current_user, login_required, login_user, logout_user
from app_main.models import *
from app_main.forms import *

from app_main import mail
from flask_mail import Message


@app.before_request
def before_request():
    if current_user.is_authenticated:
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    requests = Request.query.filter(Request.user_id==current_user.id).order_by(desc(Request.created)).all()
    req_cost = Request.query.filter(Request.user_id==current_user.id).filter(Request.cost==None).all()
    now = datetime.now()

    return render_template('base.html', title = 'Home', requests=requests, req_cost=len(req_cost), now=now)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/new_request', methods = ['GET', 'POST'])
def new_request():
    form = NewRequestForm()
    if form.validate_on_submit():

        choose_direction = form.direction.data
        choose_customer = form.customer.data
        cargo_type = form.cargo_type.data
        quantity_all = form.quantity.data

        new = Request(org=form.org.data,
                      pick_up_date=form.pick_up_date.data,
                      dest = form.dest.data,
                      cargo_desciption = form.cargo_desciption.data,
                      cargo_value=form.cargo_value.data,
                      direction=choose_direction.name,
                      user_id=current_user.id,
                      customer_name = choose_customer.name,
                      customer_id = choose_customer.id,
                      payment_day = choose_customer.payment_day,
                      cargo_type = form.cargo_type.data,
                      quantity = quantity_all.quantity,
                      type_of_loading=form.type_of_loading.data,
                      type_of_truck = form.type_of_truck.data,
                      weigth_cargo = form.weigth_cargo.data,
                      request_comments = form.request_comments.data,
                      request_status = form.request_status.data
                      )
        db.session.add(new)
        db.session.commit()
        print('da')
        ######выбираем закупщика с наименьшем количеством запросов
        if new.customer.name == 'Шенкер Екатеринбург':
            buyer = User.query.get(3)
        elif new.customer.name == 'ДСВ':
            buyer = User.query.get(1)
        elif new.direction == 'INT':
            buyer = User.query.filter(User.competention=='int').order_by(User.request_count.asc()).first()
        else:
            buyer = User.query.filter(User.role=='buyer').order_by(User.request_count.asc()).first()
        new.users.append(buyer)
        buyer.request_count +=1
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        print('net')
    return render_template('new_request_form.html', form=form)

# маршрут для указания стоимости для закупщика
@app.route('/cost/<int:id>', methods = ['GET', 'POST'])
def cost(id):
    update_request = Request.query.get(id)
    form = ConfirmRate()
    if form.validate_on_submit():
        cost = form.cost.data
        update_request.cost = cost
        db.session.add(update_request)
        db.session.commit()
        update_request.cost_created = datetime.utcnow ()
        db.session.commit ()
        return redirect(url_for('index'))
    return render_template('confirm_rate.html', form=form, id=id, update_request=update_request)

#маршрут для редактирования запроса продавцом
@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    update_request = Request.query.get(id)
    form = EditForm()
    if form.validate_on_submit():
        choose_direction = form.direction.data
        choose_customer = form.customer.data
        cargo_type = form.cargo_type.data
        quantity_all = form.quantity.data

        org = form.org.data,
        dest = form.dest.data,
        cargo_desciption = form.cargo_desciption.data,
        cargo_value = form.cargo_value.data,
        direction = choose_direction.name,
        user_id = current_user.id,
        customer_name = choose_customer.name,
        customer_id = choose_customer.id,
        payment_day = choose_customer.payment_day,
        cargo_type = form.cargo_type.data,
        quantity = quantity_all.quantity,
        type_of_loading = form.type_of_loading.data,
        type_of_truck = form.type_of_truck.data,
        weigth_cargo = form.weigth_cargo.data,
        request_comments = form.request_comments.data,
        update_request.org = org
        update_request.dest = dest
        update_request.cargo_desciption = cargo_desciption
        update_request.cargo_value = cargo_value
        update_request.direction = direction
        update_request.customer_name = customer_name
        update_request.customer_id = customer_id
        update_request.payment_day = payment_day
        update_request.cargo_type = cargo_type
        update_request.quantity = quantity
        update_request.type_of_loading = type_of_loading
        update_request.type_of_truck = type_of_truck
        update_request.weigth_cargo = weigth_cargo
        update_request.request_comments = request_comments
        update_request.created = datetime.utcnow()
        update_request.request_status  = form.request_status.data

        db.session.add(update_request)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, id=id, request=update_request)

#маршрут, чтобы смотреть кто поехал
@app.route('/orders')
def orders():
    requests = db.session.query(Request).filter(Request.request_status=='ЕДЕМ'). filter(Request.user_id==current_user.id).all()
    return render_template('request_confirmed.html', requests = requests)


#форма для заявки
@app.route('/form-for-dogovor')
def form_for_dogovor():
    pass


@app.route('/redirect/<int:id>', methods = ['GET', 'POST'])
def re_direct(id):
    update_request = Request.query.get(id)
    form = RedirectForm()
    if form.validate_on_submit():
        buyer_form = form.buyer.data
        buyer_form_id = buyer_form.id
        buyer = User.query.filter(User.id == buyer_form_id).first()
        buyer.request_count += 1
        update_request.users.append(buyer)
        if current_user.request_count > 0:
            current_user.request_count -=1
        else:
            current_user.request_count = 0
        update_request.redirect_comment=current_user.name
        update_request.users.remove(current_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('redirect.html', form = form, id=id, update_request=update_request)



@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    form = Remove()
    if form.validate_on_submit():
        request = Request.query.get(form.remove.data)
        db.session.delete(request)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('remove.html', form=form, id=id)



@app.route('/delete_req/<int:id>', methods = ['GET', 'POST'])
def delete_req(id):
    request = Request.query.get(id)
    if request.cost == None:
        for u in request.users.all():
            if u.request_count > 0:
                u.request_count -= 1
            else:
                u.request_count = 0
        db.session.delete(request)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash("невозможно удалить запрос который содержит цену")
    return redirect(url_for('index'))



@app.route('/request_with_cost')
def request_with_cost():
    db = Request.query.filter(Request.cost != None)
    return render_template('request_with_cost.html', db=db)

#вид обртаной связи
@app.route('/feedback/<int:id>', methods=['GET', 'POST'])
def feedback(id):
    req = Request.query.get(id)


    user = User.query.get(current_user.id)
    posts = Posts.query.filter(Posts.request_id==id).order_by(Posts.post_date.desc()).all()
    form = FeedBack()


    if form.validate_on_submit():
        req = Request.query.get(id)
        req_sale = req.user.id
        sale = user.query.get(req_sale)
        sale_email = sale.user_email

        buyer = req.users.first()
        buyer_email = buyer.user_email
        feedback = form.comments.data

        req.comment.append(Posts(post=feedback, user_id=current_user.id))
        db.session.commit()

        # функция отправки письма
        if current_user.role == 'buyer':
            msg = Message ('New comment in request{}'.format(str(req.id)), sender='redmessageinfo@gmail.com',
                           recipients=[sale_email])
            msg.body = "{}, \n \n http://192.168.1.117:5000/feedback/{}".format(form.comments.data, str(req.id))
            mail.send(msg)

        else:
            msg = Message('New comment in request{}'.format(str(req.id)), sender='redmessageinfo@gmail.com',
                          recipients=[buyer_email])
            print(buyer_email)
            msg.body = "{}, \n \n http://192.168.1.117:5000/feedback/{}".format(form.comments.data, str(req.id))
            mail.send(msg)


        return redirect(url_for('feedback', id=id))
    return render_template('feedback.html', form=form, req=req, user=user, posts=posts)

@app.route('/recive_order', methods = ['POST', 'GET'])
def recieve_order():
    return render_template('recieve_order.html')

# блок вспомогательных функций
def count(id):
    user = User.query.get(id)
    return user

#функция загрузки файла

UPLOAD_FOLDER = 'app_main/templates/agreements'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
AGG_FOLDER ='app_main/templates/agreements'
app.config['AGG_FOLDER'] = AGG_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upl', filename=filename))
    return render_template('uploads.html')

#рут для подтверждения загрузки
@app.route('/upl/<filename>')
def upl(filename):
    return render_template('upl.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#функция выгрузки файла

# #функция выбора номер договора
# @app_main.route('/agrement_number', methods=['POST', 'GET'])
# def agrement_number():
#     form = Who()
#     if form.validate_on_submit():
#         choice = form.who_number.data
#         if choice == 'наш номер договора':
#             count = 3
#             agreement = Agreement.query.filter(Agreement.count).first()
#             add_count = agreement.count
#
#             new = Agreement(number=str())





# функция работы с договорами клиентов
@app.route('/agreement_form', methods=['POST', 'GET'])
def agreement_form():
    template = "app_main/templates/agreements/ДОГОВОР_ТЭО_РЭД_2019 v python.docx"
    form = Agreement_form()
    name = 'РЭД_С_2019-'
    if form.validate_on_submit():
        numb = Agg_number()
        db.session.add(numb)
        db.session.commit()
        numb.numb = name+str(numb.id)
        agreement = Agreement(user_id=current_user.id,date=form.date.data, number=form.number.data,
                              customer_name=form.customer_name.data)
        document = MailMerge(template)
        print(document.get_merge_fields ())
        document.merge (
            date=form.date.data,
            number=numb.numb,
            customer_type = form.customer_type.data,
            customer_name = form.customer_name.data,
            by_who = form.by_who.data,
            name = form.name.data,
            basis_on = form.basis_on.data,
            untill = form.untill.data,
            legal_add = form.legal_add.data,
            fact_add = form.fact_add.data,
            inn = form.inn.data,
            kpp = form.kpp.data,
            ogrn = form.ogrn.data,
            bank = form.bank.data,
            bic = form.bic.data,
            kor_acc = form.kor_acc.data,
            acc_number = form.acc_number.data,
        )
        db.session.add (agreement)
        db.session.commit ()
        print(document.get_merge_fields())
        document.write('app_main/templates/agreements/ДОГОВОР {}.docx'.format(form.customer_name.data))
        filename = '{}.docx' .format(form.customer_name.data)
        agreement.filename = filename
        db.session.commit()
        return redirect(url_for('my_agreements'))
        #return redirect(url_for('download_agreement', filename=filename))
    return render_template('order_doc.html', form=form)


#функция показывает все договора юзера
@app.route('/my_agreements')
def my_agreements():
    base = Agreement.query.filter(Agreement.user_id==current_user.id).all()
    return render_template('my_agreements.html', base=base)
        #send_from_directory(app_main.config['AGG_FOLDER'], filename=filename, base=base)

#Функция вскачивает договор
@app.route('/download_agreement/<filename>')
def download_agreement(filename):
    return send_from_directory(app.config['AGG_FOLDER'], filename=filename)

@app.route('/test')
def test():
    msg = Message('Hello', sender='rosexport.200@gmail.com', recipients=['dmitriy@rosexport.su'])
    mail.send(msg)
    return 'Message sent'


@app.route('/new_customer', methods=['POST', 'GET'])
def new_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        ttn = form.payment_terms.data
        base = form.customer_base.data
        new_customer = Customer(
            user_id = current_user.id,
            name = form.name.data,
            dm = form.dm.data,
            phone = form.phone.data,
            email = form.email.data,
            payment_day = form.payment_day.data,
            payment_terms =form.payment_terms.data,
            customer_base = form.customer_base.name,


        )
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_customer.html', form=form)

@app.route('/my_customers')
def my_customers():
    customers = Customer.query.filter(Customer.user_id==current_user.id).all()
    return render_template('my_customers.html', customers=customers)

#форма заявки с перевозами
@app.route('/agreement_form_subc', methods=['POST', 'GET'])
def agreement_form_subc():
    template = '/Users/Yabloko/PycharmProjects/Mega/untitled_29/intranet_2/app_main/templates/agreements/dogovor_z_subc_python.docx'
    form = Agreement_zyavka_supplier()
    name = 'РЭД_ДЗ_2019-'
    if form.validate_on_submit():
        numb = Agg_number()
        db.session.add(numb)
        db.session.commit()
        numb.numb = name+str(numb.id)

        agreement = Supplier(user_id=current_user.id)

        document = MailMerge(template)
        print(document.get_merge_fields ())
        document.merge (
            from_=form.from_.data,
            number=numb.numb,
            to = form.to.data,
            date_loading = form.date_loading.data,
            time_loading = form.time_loading.data,
            shipper_name = form.shipper_name.data,
            shipper_phone = form.shipper_phone.data,
            date_unloading = form.date_unloading.data,
            time_unloading = form.time_unloading.data,
            cnee_name = form.cnee_name.data,
            cnee_address = form.cnee_address.data,
            cnee_fio = form.cnee_fio.data,
            cargo_description = form.cargo_description.data,
            number_request = form.number_request.data,
            cargo_value = form.cargo_value.data,
            loading_type = form.loading_type.data,
            unloading_type = form.unloading_type.data,
            cargo_pallets = form.cargo_pallets.data,

            cargo_total_weight=form.cargo_total_weight.data,
            cargo_m3=form.cargo_m3.data,
            truck_description = form.truck_description.data,

            truck_type=form.truck_type.data,
            special=form.special.data,
            truck_cost=form.truck_cost.data,
            cost_payment_day=form.cost_payment_day.data,
            truck_model=form.truck_model.data,

            driver_fio=form.driver_fio.data,
            passort_seria_nomer=form.passort_seria_nomer.data,
            passport_vydan=form.passport_vydan.data,
            truck_plate=form.truck_plate.data,
            cargo_phone=form.cargo_phone.data,

            driver_license=form.driver_license.data,
            contact_name=form.contact_name.data,
            contact_phone=form.contact_phone.data,
            cargo_name=form.cargo_name.data,
            driver_phone=form.driver_phone.data,

            llc=form.driver_license.data,
            llc_name=form.contact_name.data,
            legal_add=form.contact_phone.data,
            fact_address=form.cargo_name.data,
            inn=form.driver_phone.data,

            kpp=form.kpp.data,
            ogrn=form.ogrn.data,
            bank=form.bank.data,
            bik=form.bik.data,
            rc=form.rc.data,

            kc=form.kc.data,
            driver_director=form.driver_director.data,

        )
        db.session.add(agreement)
        db.session.commit ()
        print(document.get_merge_fields())
        document.write('/Users/Yabloko/PycharmProjects/Mega/untitled_29/intranet_2/app_main/templates/agreements/dogovor_z_subc{} .docx'.format(form.llc_name.data))
        filename = '{}.docx' .format(form.llc_name.data)
        agreement.filename = filename
        db.session.commit()
        return redirect(url_for('my_agreements_subc'))
        #return redirect(url_for('download_agreement', filename=filename))
    return render_template('dogovor_zayvka_s.html', form=form)

#функция показывает все договора юзера
@app.route('/my_agreements_subc')
def my_agreements_subc():
    base = Supplier.query.filter(Supplier.user_id==current_user.id).all()
    return render_template('my_agreements_subc.html', base=base)
        #send_from_directory(app_main.config['AGG_FOLDER'], filename=filename, base=base)

#статус запроса
@app.route('/status_for_request/<int:id>', methods=['POST', 'GET'])
def status_for_request(id):
    request = Request.query.get(id)
    form = StatusForm()
    if form.validate_on_submit():
        request.request_status = form.name.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('status_request.html', request = request, form=form)

@app.route('/my_orders')
def my_orders():
    requests = Request.query.filter(Request.user_id == current_user.id, Request.request_status=='ЕДЕМ').all()
    return render_template('include.html', requests=requests)
