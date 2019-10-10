# импортируем библиотеку datetime
import datetime
# импортируем библиотеку sqlalchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class Athelete(Base):
    __tablename__ = 'athelete' # задаем название таблиц
    id = sa.Column(sa.Integer, primary_key=True) # идентификатор пользователя, первичный ключ
    age = sa.Column(sa.Integer)     # возраст атлета
    birthdate = sa.Column(sa.Text)  # дата рождения атлета
    gender = sa.Column(sa.Text)     # пол атлета
    height = sa.Column(sa.Float)    # рост атлета
    weight = sa.Column(sa.Integer)  # вес атлета
    name = sa.Column(sa.Text)       # имя атлета
    gold_medals = sa.Column(sa.Integer) # число завоеванных золотых медалей
    silver_medals = sa.Column(sa.Integer) # число завоеванных серебряных медалей
    bronze_medals = sa.Column(sa.Integer) # число завоеванных бронзовых медалей
    total_medals = sa.Column(sa.Integer)  # общее число завоеванных медалей
    sport = sa.Column(sa.Text)      # вид спорта атлета
    country = sa.Column(sa.Text)    # из какой страны атлет

class User(Base):
    __tablename__ = 'user' # задаем название таблиц
    id = sa.Column(sa.Integer, primary_key=True) # идентификатор пользователя, первичный ключ
    first_name = sa.Column(sa.Text)# имя пользователя
    last_name = sa.Column(sa.Text) # фамилия пользователя
    gender = sa.Column(sa.Text)    # пол пользователя
    email = sa.Column(sa.Text)     # адрес электронной почты пользователя
    birthdate = sa.Column(sa.Text) # дата рождения пользователя
    height = sa.Column(sa.Float)   # рост пользователя

def connect_db():
    engine = sa.create_engine(DB_PATH) # создаем соединение к базе данных
    Base.metadata.create_all(engine)   # создаем описанные таблицы
    session = sessionmaker(engine)     # создаем фабрику сесси
    return session()                   # возвращаем сессию

def request_data():
    # выводим запрос
    print("Поищем атлетов похожих на одного из пользователей.")
    user_id = input("Введите идентификатор пользователя: ")
    return int(user_id)

def convert_str_to_date(str_date):
    parts = str_date.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def nearest_by_bd(user, session):
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd

    user_bd = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd

    return athlete_id, athlete_bd

def nearest_by_height(user, session):
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height

    return athlete_id, athlete_height

def main():
    session = connect_db()   # создаем сессию
    user_id = request_data() # запрашиваем id данные пользователя
    user = session.query(User).filter(User.id == user_id).first() # поиск пользователя по id
    if not user:
        print("Такого пользователя не нашлось:(")
    else:
        bd_athlete, bd = nearest_by_bd(user, session)
        height_athlete, height = nearest_by_height(user, session)
        print("Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd))
        print("Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height))

if __name__ == "__main__":
	main()