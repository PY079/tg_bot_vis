from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# home_dir= os.path.expanduser('~')
# da = os.path.join(home_dir,'bots/tg_bot_vis/attacments_true/blacklist.db')
# pk = 'C:/Users/User/Desktop/tg_bot_mus/post_tg/1/attachments_true/blacklist.db'
s = '/root/bots/tg_bot_vis/attachments_true/blacklist.db'

engine = create_engine(f'sqlite:///{s}')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class BlacklistedUser(Base):
    __tablename__ = 'blacklisted_users'
    user_id = Column(String, primary_key=True)

# Base.metadata.create_all(bind=engine)

def ban_user(user_id):
    with Session() as session:
        user = BlacklistedUser(user_id=user_id)
        session.add(user)
        session.commit()

def unban_user(user_id):
    with Session() as session:
        user = session.query(BlacklistedUser).filter_by(user_id=user_id).first()
        if user:
            session.delete(user)
            session.commit()

# Функция для проверки наличия пользователя в черном списке
def check_user_existence(user_id):
    with Session() as session:
        user = session.query(BlacklistedUser).filter_by(user_id=user_id).first()
        return user is not None