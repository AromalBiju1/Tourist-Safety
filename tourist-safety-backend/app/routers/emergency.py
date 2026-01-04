from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.emergency_contact import EmergencyContact
from app.schemas.emergency import EmergencyContactResponse, StateEmergencyContacts, NationalEmergencyNumbers

router = APIRouter(prefix="/emergency", tags=["Emergency"])


@router.get("/national", response_model=NationalEmergencyNumbers)
async def get_national_emergency_numbers():
    """
    Get national emergency numbers applicable across India.
    These numbers work from any location in India.
    """
    return NationalEmergencyNumbers()


@router.get("/state/{state_name}", response_model=StateEmergencyContacts)
async def get_state_emergency_contacts(
    state_name: str,
    db: Session = Depends(get_db)
):
    """
    Get emergency contacts specific to a state.
    """
    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.state.ilike(f"%{state_name}%")
    ).all()
    
    if not contacts:
        # Return national numbers if no state-specific data
        return StateEmergencyContacts(
            state=state_name,
            contacts=[]
        )
    
    return StateEmergencyContacts(
        state=state_name,
        contacts=[EmergencyContactResponse.model_validate(c) for c in contacts]
    )


@router.get("/all-states")
async def get_all_states_contacts(db: Session = Depends(get_db)):
    """
    Get list of all states with emergency contact data.
    """
    states = db.query(EmergencyContact.state).distinct().all()
    return {
        "states": [s[0] for s in states],
        "total_states": len(states)
    }


@router.get("/by-service/{service_type}")
async def get_contacts_by_service(
    service_type: str,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get emergency contacts by service type.
    Service types: police, ambulance, fire, women_helpline, tourist_helpline
    """
    query = db.query(EmergencyContact).filter(
        EmergencyContact.service_type.ilike(f"%{service_type}%")
    )
    
    if state:
        query = query.filter(EmergencyContact.state.ilike(f"%{state}%"))
    
    contacts = query.all()
    
    return {
        "service_type": service_type,
        "count": len(contacts),
        "contacts": [EmergencyContactResponse.model_validate(c) for c in contacts]
    }


@router.get("/quick-help")
async def get_quick_help():
    """
    Get quick-access emergency information card.
    """
    return {
        "title": "Emergency Help",
        "message": "In case of emergency, call the following numbers:",
        "primary_numbers": [
            {"service": "Police", "number": "100", "icon": "🚔"},
            {"service": "Ambulance", "number": "102", "icon": "🚑"},
            {"service": "Fire", "number": "101", "icon": "🚒"},
            {"service": "Women Helpline", "number": "1091", "icon": "👩"},
            {"service": "Tourist Helpline", "number": "1363", "icon": "🧳"},
        ],
        "tips": [
            "Stay calm and speak clearly",
            "Provide your exact location",
            "Describe the emergency type",
            "Follow operator instructions",
            "Keep your phone charged"
        ],
        "universal_emergency": "112"
    }


@router.get("/sos")
async def sos_information():
    """
    Get SOS emergency information with step-by-step guidance.
    """
    return {
        "immediate_actions": [
            {
                "step": 1,
                "title": "Call for Help",
                "description": "Dial 112 (Universal Emergency) or 100 (Police)",
                "icon": "📞"
            },
            {
                "step": 2,
                "title": "Share Location",
                "description": "Share your GPS location with emergency services",
                "icon": "📍"
            },
            {
                "step": 3,
                "title": "Stay Safe",
                "description": "Move to a safe, visible location if possible",
                "icon": "🏃"
            },
            {
                "step": 4,
                "title": "Contact Embassy",
                "description": "If you're a foreign tourist, contact your embassy",
                "icon": "🏛️"
            }
        ],
        "important_embassies": {
            "US": "+91-11-2419-8000",
            "UK": "+91-11-2419-2100",
            "Canada": "+91-11-4178-2000",
            "Australia": "+91-11-4139-9900",
            "Germany": "+91-11-4419-9199"
        }
    }
