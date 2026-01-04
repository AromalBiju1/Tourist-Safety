"""
Seed database with ALL India districts and tourist attractions.
Covers 700+ districts across all states and union territories.
"""
from app.database import SessionLocal, init_db
from app.models.city import City
from app.models.attraction import Attraction
from app.models.emergency_contact import EmergencyContact

# Import all district data
from scripts.data.north_india import NORTH_INDIA_DISTRICTS
from scripts.data.west_central_india import WEST_CENTRAL_INDIA_DISTRICTS
from scripts.data.south_india import SOUTH_INDIA_DISTRICTS
from scripts.data.east_india import EAST_NORTHEAST_INDIA_DISTRICTS
from scripts.data.northeast_rajasthan import NORTHEAST_RAJASTHAN_DISTRICTS

# Combine all districts
ALL_DISTRICTS = (
    NORTH_INDIA_DISTRICTS +
    WEST_CENTRAL_INDIA_DISTRICTS +
    SOUTH_INDIA_DISTRICTS +
    EAST_NORTHEAST_INDIA_DISTRICTS +
    NORTHEAST_RAJASTHAN_DISTRICTS
)

# Tourist attractions data (major sites)
ATTRACTIONS_DATA = [
    # Delhi
    ("Red Fort", "New Delhi", 28.6562, 77.2410, "monument", "UNESCO World Heritage Site", 4.5, None),
    ("India Gate", "New Delhi", 28.6129, 77.2295, "monument", "War memorial", 4.6, None),
    ("Qutub Minar", "South Delhi", 28.5245, 77.1855, "monument", "UNESCO site", 4.5, None),
    ("Lotus Temple", "South Delhi", 28.5535, 77.2588, "temple", "Baha'i House of Worship", 4.5, None),
    # Mumbai
    ("Gateway of India", "Mumbai City", 18.9220, 72.8347, "monument", "Iconic arch", 4.5, None),
    ("Marine Drive", "Mumbai City", 18.9432, 72.8235, "nature", "Promenade", 4.6, None),
    ("Elephanta Caves", "Mumbai Suburban", 18.9633, 72.9315, "monument", "UNESCO caves", 4.3, None),
    # Jaipur
    ("Hawa Mahal", "Jaipur", 26.9239, 75.8267, "monument", "Palace of Winds", 4.4, None),
    ("Amber Fort", "Jaipur", 26.9855, 75.8513, "monument", "Hilltop fort", 4.6, None),
    ("City Palace", "Jaipur", 26.9258, 75.8237, "monument", "Royal palace", 4.4, None),
    # Agra
    ("Taj Mahal", "Agra", 27.1751, 78.0421, "monument", "UNESCO symbol of love", 4.8, None),
    ("Agra Fort", "Agra", 27.1795, 78.0211, "monument", "Mughal fort", 4.5, None),
    # Varanasi
    ("Dashashwamedh Ghat", "Varanasi", 25.3050, 83.0100, "temple", "Main ghat, Ganga Aarti", 4.6, None),
    ("Kashi Vishwanath Temple", "Varanasi", 25.3109, 83.0107, "temple", "Sacred Hindu temple", 4.5, None),
    # Kerala
    ("Backwaters", "Alappuzha", 9.4981, 76.3388, "nature", "Scenic lagoons", 4.7, None),
    ("Fort Kochi Beach", "Ernakulam", 9.9639, 76.2425, "nature", "Historic beach", 4.3, None),
    # Karnataka
    ("Mysore Palace", "Mysuru", 12.3052, 76.6552, "monument", "Grand royal palace", 4.6, None),
    ("Hampi", "Bellary", 15.3350, 76.4600, "monument", "UNESCO ruins", 4.7, None),
    # Tamil Nadu
    ("Meenakshi Temple", "Madurai", 9.9195, 78.1193, "temple", "Ancient temple", 4.7, None),
    ("Marina Beach", "Chennai", 13.0500, 80.2824, "nature", "Urban beach", 4.3, None),
    # Goa
    ("Calangute Beach", "North Goa", 15.5449, 73.7551, "nature", "Popular beach", 4.2, None),
    ("Basilica of Bom Jesus", "North Goa", 15.5009, 73.9116, "monument", "UNESCO church", 4.4, None),
    # Himachal
    ("Mall Road Shimla", "Shimla", 31.1048, 77.1734, "nature", "Hill station center", 4.3, None),
    ("Rohtang Pass", "Kullu", 32.3725, 77.2477, "nature", "Mountain pass", 4.5, None),
    # Uttarakhand
    ("Har Ki Pauri", "Haridwar", 29.9561, 78.1691, "temple", "Sacred ghat", 4.6, None),
    ("Laxman Jhula", "Rishikesh", 30.1214, 78.3192, "monument", "Iconic bridge", 4.4, None),
    # Rajasthan
    ("Mehrangarh Fort", "Jodhpur", 26.2979, 73.0183, "monument", "Majestic fort", 4.7, None),
    ("Lake Pichola", "Udaipur", 24.5708, 73.6809, "nature", "Lake with palaces", 4.7, None),
    ("Jaisalmer Fort", "Jaisalmer", 26.9124, 70.9073, "monument", "Living fort", 4.6, None),
    # Ladakh/J&K
    ("Dal Lake", "Srinagar", 34.1000, 74.8500, "nature", "Scenic lake", 4.7, None),
    ("Pangong Lake", "Leh", 33.7595, 78.6669, "nature", "High altitude lake", 4.8, None),
    # Northeast
    ("Kaziranga", "Nagaon", 26.5775, 93.1711, "nature", "UNESCO wildlife", 4.6, None),
    ("Tawang Monastery", "Tawang", 27.5861, 91.8594, "temple", "Buddhist monastery", 4.5, None),
    ("Living Root Bridges", "East Khasi Hills", 25.2500, 91.7500, "nature", "Natural wonder", 4.6, None),
    # Kolkata/Bengal
    ("Victoria Memorial", "Kolkata", 22.5448, 88.3426, "monument", "Marble building", 4.5, None),
    ("Howrah Bridge", "Howrah", 22.5851, 88.3468, "monument", "Iconic bridge", 4.4, None),
    # Andaman
    ("Radhanagar Beach", "South Andaman", 11.9833, 92.9833, "nature", "Best beach in Asia", 4.8, None),
]

# Emergency contacts data  
EMERGENCY_CONTACTS_DATA = [
    ("All States", "police", "Police Control Room", "100", "112", "24x7 police emergency", "Yes"),
    ("All States", "ambulance", "Ambulance", "102", "108", "Medical emergency", "Yes"),
    ("All States", "fire", "Fire Brigade", "101", None, "Fire emergency", "Yes"),
    ("All States", "women_helpline", "Women Helpline", "1091", "181", "Women safety", "Yes"),
    ("All States", "tourist_helpline", "Tourist Helpline", "1363", None, "Tourist assistance", "Yes"),
    ("All States", "child_helpline", "Child Helpline", "1098", None, "Child protection", "Yes"),
    ("All States", "disaster", "Disaster Management", "108", None, "Emergencies", "Yes"),
    ("Delhi", "police", "Delhi Police", "100", "112", "Delhi Police", "Yes"),
    ("Maharashtra", "police", "Maharashtra Police", "100", "112", "MH Police", "Yes"),
    ("Kerala", "tourist_helpline", "Kerala Tourism", "1800-425-4747", None, "Kerala tourism", "Yes"),
    ("Rajasthan", "tourist_helpline", "Rajasthan Tourism", "1800-180-6127", None, "Raj tourism", "Yes"),
    ("Tamil Nadu", "police", "Tamil Nadu Police", "100", "112", "TN Police", "Yes"),
    ("Karnataka", "police", "Karnataka Police", "100", "112", "KA Police", "Yes"),
    ("Goa", "tourist_helpline", "Goa Tourism", "1800-233-7554", None, "Goa tourism", "Yes"),
    ("West Bengal", "police", "WB Police", "100", "112", "WB Police", "Yes"),
    ("Uttar Pradesh", "police", "UP Police", "100", "112", "UP Police", "Yes"),
]


def seed_database():
    """Seed the database with comprehensive India data."""
    print("🌱 Seeding database with ALL India districts...")
    print(f"📊 Total districts to seed: {len(ALL_DISTRICTS)}")
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_cities = db.query(City).count()
        if existing_cities > 0:
            print(f"Database already has {existing_cities} cities. Clearing and re-seeding...")
            db.query(Attraction).delete()
            db.query(EmergencyContact).delete()
            db.query(City).delete()
            db.commit()
        
        # Seed districts/cities
        print("Adding districts...")
        city_map = {}
        for i, city_data in enumerate(ALL_DISTRICTS):
            city = City(
                name=city_data[0],
                state=city_data[1],
                latitude=city_data[2],
                longitude=city_data[3],
                population=city_data[4],
                crime_index=city_data[5],
                safety_zone=city_data[6]
            )
            db.add(city)
            db.flush()
            city_map[city_data[0]] = city
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"  ... added {i + 1} districts")
        
        db.commit()
        print(f"  ✓ Added {len(ALL_DISTRICTS)} districts")
        
        # Seed attractions
        print("Adding attractions...")
        attractions_added = 0
        for attr_data in ATTRACTIONS_DATA:
            city_name = attr_data[1]
            city = city_map.get(city_name) or db.query(City).filter(City.name == city_name).first()
            
            if city:
                attraction = Attraction(
                    name=attr_data[0],
                    city_id=city.id,
                    latitude=attr_data[2],
                    longitude=attr_data[3],
                    category=attr_data[4],
                    description=attr_data[5],
                    rating=attr_data[6],
                    image_url=attr_data[7],
                    popularity_score=attr_data[6] * 20
                )
                db.add(attraction)
                attractions_added += 1
        
        db.commit()
        print(f"  ✓ Added {attractions_added} attractions")
        
        # Seed emergency contacts
        print("Adding emergency contacts...")
        for contact_data in EMERGENCY_CONTACTS_DATA:
            contact = EmergencyContact(
                state=contact_data[0],
                service_type=contact_data[1],
                service_name=contact_data[2],
                phone_number=contact_data[3],
                alternate_number=contact_data[4],
                description=contact_data[5],
                available_24x7=contact_data[6]
            )
            db.add(contact)
        
        db.commit()
        print(f"  ✓ Added {len(EMERGENCY_CONTACTS_DATA)} emergency contacts")
        
        # Final summary
        print("\n" + "=" * 50)
        print("✅ Database seeded successfully!")
        print("=" * 50)
        
        # Stats by zone
        green = db.query(City).filter(City.safety_zone == 'green').count()
        orange = db.query(City).filter(City.safety_zone == 'orange').count()
        red = db.query(City).filter(City.safety_zone == 'red').count()
        
        print(f"\n📊 Summary:")
        print(f"  - Total Districts: {db.query(City).count()}")
        print(f"    🟢 Green (Safe): {green}")
        print(f"    🟠 Orange (Moderate): {orange}")
        print(f"    🔴 Red (High Risk): {red}")
        print(f"  - Attractions: {db.query(Attraction).count()}")
        print(f"  - Emergency Contacts: {db.query(EmergencyContact).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
