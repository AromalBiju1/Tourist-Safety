from pydantic import BaseModel, Field
from typing import Optional


class EmergencyContactBase(BaseModel):
    state: str = Field(..., min_length=1, max_length=100)
    service_type: str = Field(..., min_length=1, max_length=50)
    service_name: Optional[str] = None
    phone_number: str = Field(..., min_length=1, max_length=50)
    alternate_number: Optional[str] = None
    description: Optional[str] = None
    available_24x7: str = "Yes"


class EmergencyContactResponse(EmergencyContactBase):
    id: int
    
    class Config:
        from_attributes = True


class StateEmergencyContacts(BaseModel):
    """All emergency contacts for a state"""
    state: str
    contacts: list[EmergencyContactResponse]


class NationalEmergencyNumbers(BaseModel):
    """National emergency numbers applicable across India"""
    police: str = "100"
    ambulance: str = "102"
    fire: str = "101"
    women_helpline: str = "1091"
    tourist_helpline: str = "1363"
    disaster_management: str = "108"
    child_helpline: str = "1098"
    senior_citizen: str = "14567"
