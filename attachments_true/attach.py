from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

pk = 'C:/Users/User/Desktop/tg_bot_mus/post_tg/1/attachments_true/media.db'
# home_dir = os.path.expanduser('~')
# da = os.path.join(home_dir,'bots/tg_bot_vis/attachments_true/media.db')


Base = declarative_base()
engine = create_engine(f'sqlite:///{pk}')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)

    def __init__(self, telegram_id, first_name, last_name):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.last_name = last_name

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    file_id = Column(String)
    caption = Column(String)

    def __init__(self, user_id, file_id, caption):
        self.user_id = user_id
        self.file_id = file_id
        self.caption = caption

def create_tables():
    Base.metadata.create_all(engine)

def check_user(user_id, message):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            # Если пользователя нет, создаем новую запись
            user = User(telegram_id=user_id, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
            session.add(user)

def save_media_entry(user_id, file_id, caption):
    with Session() as session:
        media_entry = Media(user_id=user_id, file_id=file_id, caption=caption)
        session.add(media_entry)
        session.commit()

def delete_media_entries():
    with Session() as session:
        session.query(Media).delete()
        session.commit()
