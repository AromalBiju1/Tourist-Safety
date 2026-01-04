# 🛠️ Complete Setup Guide for Tourist Safety Website

This guide covers multiple ways to run the project based on your environment.

---

## Prerequisites

You'll need to install these dependencies first:

### Option A: Local Development (Recommended for learning)

1. **Python 3.11+**  
   Download: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **PostgreSQL 15+**  
   Download: https://www.postgresql.org/download/windows/
   - Remember the password you set for the `postgres` user

3. **Node.js 18+** (Already installed ✅)

### Option B: Docker (Easiest, everything containerized)

1. **Docker Desktop**  
   Download: https://www.docker.com/products/docker-desktop/

---

## 🐳 Docker Setup (Recommended)

If you have Docker installed, this is the easiest way:

```bash
# Navigate to project root
cd c:\Users\Elysia\Downloads\Development

# Start all services (DB + Backend + Frontend)
docker-compose up -d

# View logs
docker-compose logs -f
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Stop:**
```bash
docker-compose down
```

---

## 🖥️ Local Setup (Manual)

### Step 1: Install Python

1. Download Python 3.11+ from https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Restart your terminal after installation
4. Verify: `python --version`

### Step 2: Install PostgreSQL

1. Download from https://www.postgresql.org/download/windows/
2. During installation:
   - Set password to `postgres` (or remember what you set)
   - Keep default port `5432`
3. Add to PATH: `C:\Program Files\PostgreSQL\15\bin`

### Step 3: Create Database

```bash
# Open Command Prompt or PowerShell
psql -U postgres

# In psql prompt:
CREATE DATABASE tourist_safety;
\q
```

### Step 4: Setup Backend

```bash
cd c:\Users\Elysia\Downloads\Development\tourist-safety-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Update .env if your PostgreSQL password is different
# Edit .env file: DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tourist_safety

# Seed the database
python scripts/seed_database.py

# Run the server
uvicorn app.main:app --reload
```

Backend will be at: http://localhost:8000

### Step 5: Setup Frontend

Open a new terminal:

```bash
cd c:\Users\Elysia\Downloads\Development\tourist-safety-frontend

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local

# Run the development server
npm run dev
```

Frontend will be at: http://localhost:3000

---

## 📦 Alternative: SQLite (No PostgreSQL Needed)

If you can't install PostgreSQL, I can modify the backend to use SQLite instead. Just ask!

---

## 🔧 Troubleshooting

### "Python not found"
- Reinstall Python with "Add to PATH" checked
- Or run: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`

### "psql not found"
- Add PostgreSQL to PATH: `C:\Program Files\PostgreSQL\15\bin`
- Or use pgAdmin GUI instead

### "Connection refused on port 8000"
- Make sure the backend is running
- Check if another app is using port 8000

### "CORS error in browser"
- Make sure frontend is running on http://localhost:3000
- Backend should be on http://localhost:8000

---

## 🧪 Verify Everything Works

1. **Backend Health Check:**
   Open: http://localhost:8000/health
   Should show: `{"status": "healthy"}`

2. **API Documentation:**
   Open: http://localhost:8000/docs
   Should show Swagger UI with all endpoints

3. **Frontend:**
   Open: http://localhost:3000
   Should show the homepage

---

## 📞 Need Help?

If you run into issues, let me know:
1. What step failed?
2. What error message did you see?
3. What operating system are you using?
