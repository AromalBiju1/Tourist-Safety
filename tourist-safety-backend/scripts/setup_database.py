"""
Database Setup Script
Creates the PostgreSQL database and runs initial setup
"""
import subprocess
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_postgres_connection():
    """Check if PostgreSQL is accessible"""
    try:
        import psycopg2
        from app.config import settings
        
        # Parse connection string
        db_url = settings.DATABASE_URL
        
        # Try to connect
        conn = psycopg2.connect(db_url)
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False


def create_database():
    """Create the database if it doesn't exist"""
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        # Connect to default database
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'tourist_safety'")
        exists = cur.fetchone()
        
        if not exists:
            print("📦 Creating database 'tourist_safety'...")
            cur.execute("CREATE DATABASE tourist_safety")
            print("✅ Database created!")
        else:
            print("✅ Database 'tourist_safety' already exists")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Could not create database: {e}")
        print("\n💡 Please create the database manually:")
        print("   psql -U postgres -c \"CREATE DATABASE tourist_safety;\"")
        return False


def create_postgis_extension():
    """Enable PostGIS extension if available"""
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            dbname="tourist_safety"
        )
        cur = conn.cursor()
        
        try:
            cur.execute("CREATE EXTENSION IF NOT EXISTS postgis")
            conn.commit()
            print("✅ PostGIS extension enabled")
        except Exception as e:
            print(f"⚠️ PostGIS not available (optional): {e}")
            conn.rollback()
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"⚠️ Could not enable PostGIS: {e}")
        return True  # Non-critical


def setup_tables():
    """Create all database tables"""
    print("📋 Creating database tables...")
    
    from app.database import init_db, engine
    from app.models import City, CrimeStatistic, Attraction, EmergencyContact
    
    init_db()
    print("✅ Tables created successfully!")


def run_seed():
    """Run the seed script"""
    print("\n🌱 Seeding database with initial data...")
    
    from scripts.seed_database import seed_database
    seed_database()


def main():
    """Main setup function"""
    print("=" * 50)
    print("🚀 Tourist Safety Database Setup")
    print("=" * 50)
    print()
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        print("\n⚠️ Continuing without automatic database creation...")
    
    # Step 2: Create PostGIS extension (optional)
    print("\nStep 2: Enabling PostGIS extension...")
    create_postgis_extension()
    
    # Step 3: Check connection
    print("\nStep 3: Verifying connection...")
    if not check_postgres_connection():
        print("\n❌ Cannot connect to database. Please check your PostgreSQL setup.")
        print("\nMake sure:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'tourist_safety' exists")
        print("  3. User 'postgres' with password 'postgres' has access")
        print("\nOr update DATABASE_URL in .env file")
        return
    
    print("✅ Connection verified!")
    
    # Step 4: Create tables
    print("\nStep 4: Creating tables...")
    setup_tables()
    
    # Step 5: Seed data
    print("\nStep 5: Seeding data...")
    run_seed()
    
    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print("\nYou can now run the server:")
    print("  uvicorn app.main:app --reload")
    print("\nAPI will be available at:")
    print("  http://localhost:8000")
    print("  http://localhost:8000/docs (Swagger UI)")


if __name__ == "__main__":
    main()
