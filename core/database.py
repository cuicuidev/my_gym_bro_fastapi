from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.sql import func

from dotenv import load_dotenv
import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "../app/.env"))
sys.path.append(BASE_DIR)

engine = create_engine(url=os.environ["POSTGRES_URL"], echo=True, future=True)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

############################################################## SCHEMA ##############################################################

########################### auth

class User(Base):
    __tablename__: str = 'user'

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    username = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))

    active = Column(Boolean)

    def __repr__(self):
        return f"<User {self.full_name!r}>"
    

class Exercise(Base):
    __tablename__: str = 'exercise'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    exercise_type_id = Column(Integer, ForeignKey('exercise_type.id'))
    exercise_type = relationship('ExerciseType')


class ExerciseType(Base):
    __tablename__: str = 'exercise_type'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)


class Set(Base):
    __tablename__: str = 'set'

    id = Column(Integer, primary_key=True, index=True)
    unix_timestamp_ms = Column(Float)

    weight_kg = Column(Float)
    n_repetitions = Column(Integer)
    rir = Column(Float)
    duration_ms = Column(Float)
    tir_ms = Column(Float)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    exercise = relationship('Exercise')

    previous_set_id = Column(Integer, ForeignKey('set.id'))
    previous_set = relationship('Set', foreign_keys=[previous_set_id], remote_side=[id])

    next_set_id = Column(Integer, ForeignKey('set.id'))
    next_set = relationship('Set', foreign_keys=[next_set_id], remote_side=[id])

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    active = Column(Boolean)