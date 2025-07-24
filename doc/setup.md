# Backend and Frontend Setup Steps

This document covers the setup steps for both backend (Django + DRF) and frontend (to be defined).

## Backend Setup (Django + DRF) ✅ COMPLETED

### Prerequisites
- Python 3.8+
- PostgreSQL database (Supabase recommended)
- Git

### 1. Project Initialization
```bash
# Clone or create project
mkdir blog-app && cd blog-app
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Required packages:**
- `django>=4.2` - Web framework
- `djangorestframework>=3.14` - API framework
- `corsheaders>=4.0` - CORS handling
- `django-filter>=23.0` - Advanced filtering
- `Pillow>=10.0` - Image processing
- `psycopg2-binary>=2.9` - PostgreSQL adapter
- `python-decouple>=3.8` - Environment management

### 3. Database Configuration (Supabase PostgreSQL)

#### Create `.env` file in backend directory:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase Database Configuration
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-db-password
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432
DB_SSLMODE=require

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
```

#### Get Supabase credentials:
1. Go to Supabase project dashboard
2. Settings → Database
3. Copy connection details

### 4. Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

**Access points:**
- Django Admin: `http://localhost:8000/admin/`
- API Root: `http://localhost:8000/api/`
- DRF Browsable API: `http://localhost:8000/api-auth/`

## Frontend Setup

*To be added when frontend stack is chosen.*

## Project Structure ✅ COMPLETED

```
backend/
├── blog_backend/          # Django project settings
│   ├── settings.py       # Main settings with PostgreSQL config
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── users/                # Custom user app
│   ├── models.py         # CustomUser model
│   ├── serializers.py    # User serializers
│   ├── views.py          # User viewsets
│   ├── urls.py           # User URL routing
│   └── admin.py          # Admin interface
├── posts/                # Blog posts app
│   ├── models.py         # Post, Category, Tag models
│   ├── serializers.py    # Post serializers
│   ├── views.py          # Post viewsets
│   ├── urls.py           # Post URL routing
│   └── admin.py          # Admin interface
├── comments/             # Comments app
│   ├── models.py         # Comment model with nested replies
│   ├── serializers.py    # Comment serializers
│   ├── views.py          # Comment viewsets
│   ├── urls.py           # Comment URL routing
│   └── admin.py          # Admin interface
├── reactions/            # Reactions app
│   ├── models.py         # Reaction model with emojis
│   ├── serializers.py    # Reaction serializers
│   ├── views.py          # Reaction viewsets
│   ├── urls.py           # Reaction URL routing
│   └── admin.py          # Admin interface
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── env.example           # Environment variables template
└── .env                  # Environment variables (create this)
```
