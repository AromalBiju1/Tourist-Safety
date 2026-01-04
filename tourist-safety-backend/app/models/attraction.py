from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Attraction(Base):
    """Tourist attraction model"""
    __tablename__ = "attractions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(500))
    
    # Details
    category = Column(String(50), index=True)  # monument, temple, nature, museum, etc.
    description = Column(Text)
    rating = Column(Float, default=4.0)
    review_count = Column(Integer, default=0)
    
    # Media
    image_url = Column(String(500))
    
    # Visiting info
    opening_hours = Column(String(200))
    entry_fee = Column(String(100))
    best_time_to_visit = Column(String(200))
    
    # Popularity score (for recommendations)
    popularity_score = Column(Float, default=50.0)
    
    # Relationships
    city = relationship("City", back_populates="attractions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city_id": self.city_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "category": self.category,
            "description": self.description,
            "rating": self.rating,
            "review_count": self.review_count,
            "image_url": self.image_url,
            "opening_hours": self.opening_hours,
            "entry_fee": self.entry_fee,
            "best_time_to_visit": self.best_time_to_visit,
            "popularity_score": self.popularity_score
        }
