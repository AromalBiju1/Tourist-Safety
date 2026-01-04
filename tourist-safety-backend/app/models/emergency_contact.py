from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class EmergencyContact(Base):
    """Emergency contact numbers by state"""
    __tablename__ = "emergency_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(100), nullable=False, index=True)
    
    # Service type
    service_type = Column(String(50), nullable=False)  # police, ambulance, fire, women_helpline, tourist_helpline
    service_name = Column(String(200))
    
    # Contact details
    phone_number = Column(String(50), nullable=False)
    alternate_number = Column(String(50))
    
    # Additional info
    description = Column(Text)
    available_24x7 = Column(String(10), default="Yes")
    
    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "service_type": self.service_type,
            "service_name": self.service_name,
            "phone_number": self.phone_number,
            "alternate_number": self.alternate_number,
            "description": self.description,
            "available_24x7": self.available_24x7
        }
