from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(r'sqlite:///C:\Users\User\Desktop\tg_bot_mus\post_tg\1\bot_forbidding_attachments\stories.db')
Base = declarative_base()

class Story(Base):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    story_text = Column(String)
    sent = Column(Boolean, default=False)


# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_story(user_id, story_text):
    new_session = Session()
    new_story = Story(user_id=user_id, story_text=story_text)
    new_session.add(new_story)
    new_session.commit()
    new_session.close()


def get_stories():
    session = Session()
    stories = session.query(Story).all()
    session.close()
    return stories


def delete_story(user_id, story_text):
    session = Session()
    story = session.query(Story).filter_by(user_id=user_id, story_text=story_text).first()
    session.delete(story)
    session.commit()
    session.close()
