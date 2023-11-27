from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from keyboards import on_near_regions, off_near_regions
engine = create_engine('postgresql://postgres:4AFDaA1*-4c52db-*3DAd-aa1FEDF*CG@monorail.proxy.rlwy.net:32226/railway', echo=True)

# Create a base class for declarative class definitions
Base = sqlalchemy.orm.declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(Integer, primary_key=True)
    region_id = Column(String)
    near_regions = Column(Boolean, default=False)
    additional_region = Column(String)


from sqlalchemy import inspect

inspector = inspect(engine)
if not inspector.has_table(User.__tablename__):
    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)

# Create a session class
Session = sessionmaker(bind=engine)
session = Session()

def get_all_users():
    users = session.query(User).all()
    user_list = [{'telegram_id': user.telegram_id, 'region_id': user.region_id} for user in users]
    return user_list

def get_region_by_id(user_id):
    user = session.query(User).filter_by(telegram_id=user_id).first()
    return user.region_id

def get_near_region_turned_on():
    users = session.query(User).filter_by(near_regions=True).all()
    user_list = [{'telegram_id': user.telegram_id, 'region_id': user.region_id} for user in users]
    return user_list

def add_user(user_id):
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if user is None:
            # User doesn't exist, create a new user entry
            new_user = User(telegram_id=user_id, region_id=None, near_regions=False, additional_region=None)
            session.add(new_user)
            session.commit()
            session.close()
            return "Привіт, я бот повітряних тривог, введи /set_region щоб встановити свій регіон"
        else:
            # User already exists, send a message
            return "Привіт, ти вже є зареєстрованим користувачем. Введи перейди в меню й обери то, що тобі потрібно."
    except Exception as e:
        print(f'Помилка: {e}')

def add_near_region(user_id, status):
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()

        if user is not None:
            # User found, update region_id
            user.near_regions = status
        else:
            # User not found, create a new user entry
            new_user = User(telegram_id=user_id, near_regions=status)
            session.add(new_user)

        session.commit()
        session.close()
    except Exception as e:
        print(f'Помилка: {e}')


def add_user_region(user_id, region_id):
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()

        if user is not None:
            # User found, update region_id
            user.region_id = region_id
        else:
            # User not found, create a new user entry
            new_user = User(telegram_id=user_id, region_id=region_id)
            session.add(new_user)

        session.commit()
        session.close()
    except Exception as e:
        print(f'Помилка: {e}')

def near_regions_status(user_id):
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if user.near_regions:
            return off_near_regions
        else:
            return on_near_regions
    except Exception as e:
        print(f'Помилка: {e}')