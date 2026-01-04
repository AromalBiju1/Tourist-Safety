from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


class CrimeStatistic(Base):
    """Crime statistics for a city by year"""
    __tablename__ = "crime_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    year = Column(Integer, nullable=False, index=True)
    
    # Crime categories (from NCRB data)
    murder = Column(Integer, default=0)
    robbery = Column(Integer, default=0)
    burglary = Column(Integer, default=0)
    theft = Column(Integer, default=0)
    riots = Column(Integer, default=0)
    kidnapping = Column(Integer, default=0)
    crimes_against_women = Column(Integer, default=0)
    cyber_crimes = Column(Integer, default=0)
    
    # Aggregates
    total_ipc_crimes = Column(Integer, default=0)
    total_sll_crimes = Column(Integer, default=0)  # Special & Local Laws
    
    # Calculated metrics
    crime_rate = Column(Float, default=0.0)  # Per 100,000 population
    
    # Data source
    source = Column(String(100), default="NCRB")
    
    # Relationships
    city = relationship("City", back_populates="crime_statistics")
    
    def calculate_crime_index(self, population: int) -> float:
        """
        Calculate a normalized crime index (0-100)
        Weighted formula prioritizing violent crimes and crimes against women
        """
        if population == 0:
            return 50.0
        
        # Weights for different crime types
        violent_crimes = (self.murder * 10 + self.robbery * 5 + 
                         self.kidnapping * 7 + self.riots * 3)
        property_crimes = (self.burglary * 2 + self.theft * 1)
        women_safety = self.crimes_against_women * 8
        
        # Normalize per 100,000 population
        weighted_score = (violent_crimes * 0.4 + 
                         property_crimes * 0.25 + 
                         women_safety * 0.35)
        
        normalized = (weighted_score / population) * 100000
        
        # Cap at 100
        return min(normalized / 10, 100)
    
    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "year": self.year,
            "murder": self.murder,
            "robbery": self.robbery,
            "burglary": self.burglary,
            "theft": self.theft,
            "riots": self.riots,
            "kidnapping": self.kidnapping,
            "crimes_against_women": self.crimes_against_women,
            "cyber_crimes": self.cyber_crimes,
            "total_ipc_crimes": self.total_ipc_crimes,
            "crime_rate": self.crime_rate,
            "source": self.source
        }
