from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
from datetime import datetime

Base = declarative_base()

class WaveQuality(enum.Enum):
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

class SurfSession(Base):
    __tablename__ = 'surf_sessions'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    location = Column(String(100), nullable=False)
    wave_height = Column(Float)  # in feet
    wave_quality = Column(Enum(WaveQuality))
    wind_speed = Column(Float)  # in mph
    wind_direction = Column(String(50))
    tide_height = Column(Float)  # in feet
    water_temp = Column(Float)  # in fahrenheit
    session_duration = Column(Integer)  # in minutes
    notes = Column(String(500))
    rating = Column(Integer)  # 1-5 rating

    def __repr__(self):
        return f"<SurfSession(date={self.date}, location={self.location}, rating={self.rating})>"

# Database connection configuration
DATABASE_URL = "postgresql://localhost/surftracker"

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session() 