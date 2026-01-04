from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class SafetyZone(str, enum.Enum):
    GREEN = "green"      # Safe - Low crime
    ORANGE = "orange"    # Moderate risk
    RED = "red"          # High risk


class City(Base):
    """City model with safety classification"""
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    population = Column(Integer)
    
    # Safety metrics
    crime_index = Column(Float, default=0.0)  # 0-100 scale
    safety_zone = Column(String(10), default=SafetyZone.ORANGE.value)
    
    # Relationships
    crime_statistics = relationship("CrimeStatistic", back_populates="city")
    attractions = relationship("Attraction", back_populates="city")
    
    def calculate_safety_zone(self) -> str:
        """Determine safety zone based on crime index"""
        if self.crime_index <= 30:
            return SafetyZone.GREEN.value
        elif self.crime_index <= 60:
            return SafetyZone.ORANGE.value
        else:
            return SafetyZone.RED.value
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "population": self.population,
            "crime_index": self.crime_index,
            "safety_zone": self.safety_zone
        }
