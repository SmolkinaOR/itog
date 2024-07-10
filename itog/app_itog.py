from flask import Flask, request, render_template
import sqlite3  
from flask_wtf import FlaskForm
from sqlalchemy import func, desc
from wtforms import *
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy




# Определение формы для добавления тура
class MyForm(FlaskForm):
    #id = IntegerField('идентификатор')
    # Поле для названия тура
    destination = StringField('Пункт назначения', validators=[DataRequired()])
    # Поле для года выпуска тура
    d_date = StringField('дата отправления')
    r_date = StringField('дата прибытия')
    # Поле для бюджета тура
    budget = IntegerField('Рейтинг')
    # Поле для сервиса тура
    services = StringField('сервис')
    # Поле для типа тура
    nametype = StringField('тип тура')

class MyForm_f_sh(FlaskForm):
    id = IntegerField('идентификатор', validators=[DataRequired()])


# Инициализация Flask приложения
app = Flask(__name__)

# Настройка соединения с базой данных (sqlite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
db = SQLAlchemy(app)

# Модель тура для SQLAlchemy
class Trevels(db.Model):
    __tablename__ = 'journey'  # Указываем название таблицы

    # Определяем столбцы таблицы
    id = db.Column(db.Integer, primary_key=True)  # ID тура (первичный ключ)
    destination = db.Column(db.String(80))  # Название тура
    d_date = db.Column(db.String(80))  # дата отправления тура
    r_date = db.Column(db.String(80))  # дата отправления тура
    budget = db.Column(db.Integer)  # бюджет тура
    services = db.Column(db.String(80))  # сервис тура
    nametype = db.Column(db.String(80))  # тип тура

    # Конструктор для создания нового объекта Trevels
    def __init__(self, destination, d_date, r_date, budget, services, nametype):
        self.destination = destination
        self.d_date = d_date
        self.r_date = r_date
        self.budget = budget
        self.services = services
        self.nametype = nametype

# Создание соединения с базой данных
con = sqlite3.connect('./instance/travel.db', check_same_thread=False)
# Создание курсора для выполнения SQL запросов  
cur = con.cursor()

# Маршрут для корневой страницы
@app.route("/")
def hello_world():
    # Возвращение приветственного сообщения
    return render_template('main.html')

# Маршрут для получения информации о фильме по ID
@app.route("/trev/<id>")
def trev(id):
    # Выполнение SQL запроса для получения данных о фильме по ID
    #res = cur.execute(f"select * from Movies where id = ?", (id,))
    # Получение результата запроса
    #film = res.fetchone()
    #print(film)
    trevel = Trevels.query.filter_by(id=id).all()
    print(trevel)
    # Проверка, найден ли фильм
    if trevel != []:
        # Возвращение результата
        return render_template('trev.html', trev = trevel[0] )
    else:
        # Сообщение о том, что тура не существует   
        return "Такого тура нет"


# Маршрут для отображения формы выбора тура
@app.route("/trev_form_sh", methods=['GET', 'POST'])
def trev_form_sh():
    # Создание формы
    form = MyForm_f_sh()
    # Проверка, была ли отправлена заполненная форма на сервер
    if form.validate_on_submit():
        # Извлекаем данные из формы
        id=form.data['id']
        trevel = Trevels.query.filter_by(id=id).all()
        #print(trevel)
        # Проверка, найден ли фильм
        if trevel != []:
            # Возвращение результата
            return render_template('trev.html', trev=trevel[0])
        else:
            # Сообщение о том, что тура не существует
            return "Такого тура нет"

    return render_template('form_sh.html', form=form)



# Маршрут для получения информации о фильме по ID из формы
@app.route("/trev_sh")
def trev_sh(id):
    # Выполнение SQL запроса для получения данных о фильме по ID
    #res = cur.execute(f"select * from Movies where id = ?", (id,))
    # Получение результата запроса
    #film = res.fetchone()
    #print(film)
    trevel = Trevels.query.filter_by(id=id).all()
    ##print(film)
    # Проверка, найден ли фильм
    if trevel != []:
        # Возвращение результата
        return render_template('trev.html', trev = trevel[0] )
    else:
        # Сообщение о том, что тура не существует
        return "Такого тура нет"


# Маршрут для получения списка всех фильмов
@app.route("/trevs" )
def trevs():
    # Выполнение SQL запроса для получения всех фильмов
    #res = cur.execute("select * from Movies")
    # Получение результата запроса
    #films = res.fetchall()
    trevel = Trevels.query.all()
    pqq=Trevels.query.count()
    #qqqqq=films.order_by(desc(Film.rating))
    qqqqq=Trevels.query.order_by(Trevels.budget).first()
    qqqqq1 = Trevels.query.order_by(Trevels.budget.desc()).first()
    # Возвращение списка фильмов (все, кол-во фильнов - число, с мин рейтингом, с мах рейтингом)
    return render_template('trevs.html', trev = trevel, pwww = pqq, pww1=qqqqq1, pww2=qqqqq)





# Маршрут для отображения формы добавления тура
@app.route("/trev_form", methods=['GET', 'POST'])
def trev_form():
    # Создание формы
    form = MyForm()
    # Проверка, была ли отправлена заполненная форма на сервер
    if form.validate_on_submit():
        # Извлекаем данные из формы
        destination=form.data['destination']
        d_date=form.data['d_date']
        r_date=form.data['r_date']
        budget=form.data['budget']
        services=form.data['services']
        nametype=form.data['nametype']
        #Создаем объект тура
        new_trev = Trevels(destination, d_date, r_date, budget, services, nametype)
        #Добавляем в БД
        db.session.add(new_trev)
        #Фиксируем изменения
        db.session.commit()
        # ниже вариант с использованием sqlite3
        # film_data = (name, genre, year, rating)
        # # Выполнение SQL запроса для добавления тура в базу данных
        # cur.execute('INSERT INTO Movies (name, genre, year, rating) VALUES (?, ?, ?, ?)', film_data)
        # # Сохранение изменений в базе данных
        # con.commit()
        return 'Фильм добавлен!'
    # Возвращаем форму для отображения к заполнению
    return render_template('form.html', form=form)




#Маршрут для добавления нового тура
@app.route("/trev_add")
def trev_add():
    # Получение данных о фильме из параметров запроса
    destination = request.args.get('destination')
    d_date = request.args.get('d_date')
    r_date = request.args.get('r_date')
    budget = request.args.get('budget')
    services = request.args.get('services')
    nametype = request.args.get('nametype')
    # Формирование кортежа с данными о фильме
    trev_data = (destination, d_date, r_date, budget, services, nametype)
    # Выполнение SQL запроса для добавления тура в базу данных
    cur.execute('INSERT INTO journey (destination, d_date, r_date, budget, services, nametype) VALUES (?, ?, ?, ?, ?, ?)', trev_data)
    # Сохранение изменений в базе данных
    con.commit()
    # Возвращение подтверждения о добавлении тура
    return "destination = {};d_date = {}; r_date = {};budget = {}; services = {}; nametype = {} ".format(destination, d_date, r_date, budget, services, nametype) 

# Запуск приложения, если оно выполняется как главный модуль
if __name__ == '__main__':
    # Отключение проверки CSRF для WTForms
    app.config["WTF_CSRF_ENABLED"] = False  
    # Запуск приложения в режиме отладки
    app.run(debug=True)
