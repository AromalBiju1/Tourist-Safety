# 🗺️ SafeTravel India

A Tourist Safety & Assistance platform for India with 697 districts, ML-powered safety analysis, and Google OAuth authentication.

![Next.js](https://img.shields.io/badge/Next.js-15-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## ✨ Features

- 🗺️ **Safety Map** - 697 districts with Green/Orange/Red safety zones
- 🛤️ **Safe Routes** - OSRM-powered routing with safety scoring
- 🤖 **ML Analytics** - Crime prediction and trend analysis
- 🔐 **Authentication** - Google OAuth + JWT
- 🆘 **Emergency** - Quick access to emergency contacts
- 📱 **Responsive** - Works on all devices

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/AromalBiju1/tourist-safety.git
cd tourist-safety

# Start all services
docker compose up --build
```

Access:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Local Development

#### Backend
```bash
cd tourist-safety-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Run server
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd tourist-safety-frontend

# Install dependencies
npm install

# Copy env file
cp env.template .env.local

# Run dev server
npm run dev
```

## ⚙️ Configuration

### Backend (`tourist-safety-backend/.env`)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tourist_safety
USE_SQLITE=true  # Set to false for PostgreSQL
JWT_SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
```

### Frontend (`tourist-safety-frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

## 📁 Project Structure

```
├── docker-compose.yml
├── tourist-safety-backend/
│   ├── app/
│   │   ├── models/      # SQLAlchemy models
│   │   ├── routers/     # API endpoints
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   └── scripts/
│       └── data/        # 697 district data
└── tourist-safety-frontend/
    └── src/
        ├── app/         # Next.js pages
        ├── components/  # React components
        └── lib/         # API client, auth
```

## 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs
6. Copy Client ID to your `.env` files

## 📊 Database

The app seeds 697 Indian districts automatically:
- 🟢 112 Green (Safe)
- 🟠 568 Orange (Moderate)
- 🔴 17 Red (High Risk)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React, TailwindCSS |
| Backend | FastAPI, SQLAlchemy |
| Database | PostgreSQL / SQLite |
| Auth | Google OAuth, JWT |
| Maps | Leaflet.js |
| Routing | OSRM |

## 📝 License

MIT
