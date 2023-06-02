from sqlalchemy import create_engine, Column, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Создание подключения к базе данных SQLite
engine = create_engine('sqlite:///C:/Users/User/Desktop/tg_bot_mus/post_tg/1/бот запрещающий вложения/users.db')
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    active = Column(Boolean, default=True)

# Создание таблицы в базе данных
# Base.metadata.create_all(engine)



# Функция для добавления нового IaD пользователя в БД
def add_user(user_id):
    user = User(user_id=user_id)
    session.add(user)
    session.commit()





# Функция для обновления статуса активности пользователя
def update_user_active_status(user_id, active):
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        user.active = active
        session.commit()
    except SQLAlchemyError as e:
        print(f"Ошибка при обновлении статуса активности пользователя {user_id}: {str(e)}")
        session.rollback()


