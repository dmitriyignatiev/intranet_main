from app_main.models import *
from datetime import datetime
from datetime import date



today = datetime.now()

today = today.replace(hour=0, minute=0, second=0, microsecond=0)
print('current day is ', today)

start_month = today.replace(day=1)
print('start month is ', start_month)
diff = today-start_month

start_week = datetime.weekday(today)
print(start_week)

# общее количество запросов за месяц
query_totall_month = Request.query.filter(Request.created>=start_month).all()
print('общее количество запросов за месяц =', len(query_totall_month))
# Из них с укзаанием стоимости
query_totall_month_cost = Request.query.filter(db.and_(Request.created>=start_month, Request.cost>0)).all()
print('общее количество запросов за месяц с указанием цены за перевозку =', len(query_totall_month_cost ))
## Количество запросов за месяц по каждому продавцу
# Количество запросов по
print()
query_month_tatiana_b = Request.query.filter(db.and_(Request.created>=start_month, Request.user_id == 13)).all()
print('общее количество запросов от Татьяны за месяц', len(query_month_tatiana_b))
query_month_tatiana_b = Request.query.filter(Request.created>=start_month, Request.cost>0, Request.user_id == 13).all()
print('общее количество прокотированных запросов Татьяне от закупок за месяц', len(query_month_tatiana_b))
print()
query_month_konstantin_g = Request.query.filter(db.and_(Request.created>=start_month, Request.user_id == 9)).all()
print('общее количество запросов от Константина за месяц', len(query_month_konstantin_g))
query_month_tatiana_b = Request.query.filter(Request.created>=start_month, Request.cost>0, Request.user_id == 9).all()
print('общее количество прокотированных запросов Константину от закупок за месяц', len(query_month_tatiana_b))
print()
query_month_konstantin_g = Request.query.filter(db.and_(Request.created>=start_month, Request.user_id == 9)).all()
print('общее количество запросов от Константина за месяц', len(query_month_konstantin_g))
query_month_tatiana_b = Request.query.filter(Request.created>=start_month, Request.cost>0, Request.user_id == 9).all()
print('общее количество прокотированных запросов Константину от закупок за месяц', len(query_month_tatiana_b))
print()
query_month_artem_a = Request.query.filter(db.and_(Request.created>=start_month, Request.user_id == 8)).all()
print('общее количество запросов от Артема за месяц', len(query_month_artem_a))
query_month_artem_a = Request.query.filter(Request.created>=start_month, Request.cost>0, Request.user_id == 8).all()
print('общее количество прокотированных запросов Артему от закупок за месяц', len(query_month_artem_a))
print()



# все продавцы
sales = User.query.filter(User.role=='sale').all()
for person in sales:
    print(person.name, ' ' , person.id)

