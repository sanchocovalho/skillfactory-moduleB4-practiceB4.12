import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()

class User(Base):
	# задаем название таблиц
    __tablename__ = 'user'
    id = sa.Column(sa.Integer,      # идентификатор пользователя
    	primary_key=True, 
    	autoincrement=True)
    first_name = sa.Column(sa.Text) # имя пользователя
    last_name = sa.Column(sa.Text)  # фамилия пользователя
    gender = sa.Column(sa.Text)     # пол пользователя
    email = sa.Column(sa.Text)      # адрес электронной почты пользователя
    birthdate = sa.Column(sa.Text)  # дата рождения пользователя
    height = sa.Column(sa.Float)    # рост пользователя

def connect_db(path):
    engine = sa.create_engine(path) # создаем соединение к базе данных
    Base.metadata.create_all(engine)# создаем описанные таблицы
    session = sessionmaker(engine)  # создаем фабрику сесси
    return session()                # возвращаем сессию

def request_data():
	# выводим приветствие
    print("Пожалуйста! Введите данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введите имя: ")  
    last_name = input("Введите фамилию: ")
    gender = input("Введите пол (Male/Female): ")
    while gender not in ['Male', 'Female']:
        gender = input('Введите "Male" или "Female". Попробуйте снова: ')
    email = input("Введите адрес электронной почты: ")
    while is_valid_email(email):
        email = input('Некорректный адрес. Попробуйте снова: ')    
    birth_date = input("Введите дату рождения (ГГГГ-ММ-ДД): ")
    height = input("Введите рост в метрах (например, 1.65): ")
    # if '.' in height:
    # 	height = input("Введите значение роста снова: ")
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birthdate=birth_date.replace(',', '-').replace('.', '-').replace('/', '-'),
        email=email,
        height=height
    )
    return user

def is_valid_email(email):
	# Проверка валидности электронной почты
    if email:
        if '@' in email:
            if '.' in email.split('@')[1]:
                return False
    return True

def main():
    session = connect_db(DB_PATH) # создаем сессию
    user = request_data() # запрашиваем данные пользователя
    session.add(user)     # добавляем нового пользователя в сессию
    session.commit()      # сохраняем все изменения, накопленные в сессии
    print("Данные были сохранены в базе данных!")

if __name__ == "__main__":
    main()