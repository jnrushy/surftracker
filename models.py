from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum
from datetime import datetime

Base = declarative_base()

class WaveQuality(enum.Enum):
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Name/model of the board
    length = Column(Float)  # Length in feet
    volume = Column(Float)  # Volume in liters
    board_type = Column(String(50))  # Type of board (shortboard, longboard, etc.)
    purchase_date = Column(DateTime)
    condition = Column(String(50))  # Current condition
    notes = Column(String(500))
    
    # Relationship with sessions
    sessions = relationship("SurfSession", back_populates="board")
    
    def __repr__(self):
        return f"<Board(name={self.name}, length={self.length}ft)>"

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
    waves_caught = Column(Integer)  # number of waves caught
    notes = Column(String(500))
    rating = Column(Integer)  # 1-5 rating
    
    # Add relationship with Board
    board_id = Column(Integer, ForeignKey('boards.id'))
    board = relationship("Board", back_populates="sessions")

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