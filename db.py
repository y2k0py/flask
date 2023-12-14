from sqlalchemy import create_engine, Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy import inspect

engine = create_engine('postgresql://postgres:4AFDaA1*-4c52db-*3DAd-aa1FEDF*CG@monorail.proxy.rlwy.net:32226/railway')
# test db postgresql://postgres:1F4DD3-1gE443ddfGDc45gGA5e2261b2@viaduct.proxy.rlwy.net:17121/railway
# real db postgresql://postgres:4AFDaA1*-4c52db-*3DAd-aa1FEDF*CG@monorail.proxy.rlwy.net:32226/railway
# Create a base class for declarative class definitions
Base = sqlalchemy.orm.declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True)
    region_id = Column(String)
    near_regions = Column(Boolean, default=False)
    additional_region = Column(String)
    notifications = Column(Boolean, default=True)
    time_zone = Column(Integer, default=0)


inspector = inspect(engine)
if not inspector.has_table(User.__tablename__):
    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)

# Create a session class
Session = sessionmaker(bind=engine)
session = Session()


def get_all_users():
    try:
        users = session.query(User).all()
        user_list = [{'telegram_id': user.telegram_id, 'region_id': user.region_id, 'near_region': user.near_regions,
                      'additional_region': user.additional_region, 'notifications': user.notifications,
                      'time_zone': user.time_zone} for user in users]
        return user_list
    except Exception as e:
        session.rollback()
        print(f'Помилка, get_all_users: {e}')


def get_region_by_user_id(user_id):
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        session.close()
        return user.region_id

    except Exception as e:
        session.rollback()
        print(f'Помилка, get_region_by_user_id: {e}')


def get_near_region_turned_on():
    try:
        users = session.query(User).filter_by(near_regions=True).all()
        user_list = [{'telegram_id': user.telegram_id, 'region_id': user.region_id} for user in users]
        return user_list
    except Exception as e:
        session.rollback()
        print(f'Помилка, get_near_region_turned_on: {e}')


def get_time_zone(user_id):
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        return user.time_zone
    except Exception as e:
        session.rollback()
        print(f'Помилка, get_time_zone: {e}')
