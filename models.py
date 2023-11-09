from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Exercise(Base):
    __tablename__: str = 'exercise'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    exercise_type_id = Column(Integer, ForeignKey('exercise_type.id'))
    exercise_type = relationship('ExerciseType')

class ExerciseType(Base):
    __tablename__: str = 'exercise_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class User(Base):
    __tablename__: str = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)

    active = Column(Boolean)

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

    parent_superset_id = Column(Integer, ForeignKey('set.id'))
    parent_superset = relationship('Entry')
    child_superset_id = Column(Integer, ForeignKey('set.id'))
    child_superset = relationship('Entry')

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    active = Column(Boolean)

    #squats - rest - squats - rest - squats - rest - rdl - rest - rdl