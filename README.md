# Blog App - Full Stack Project

A modern blog application with separate backend and frontend deployments.

## 🏗️ Project Structure

```
blog-app/
├── backend/                 # Django REST API
│   ├── Dockerfile          # Backend Docker configuration
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Backend deployment config
│   ├── DEPLOYMENT.md       # Backend deployment guide
│   └── blog_backend/       # Django project
├── frontend/               # Frontend (Coming Soon)
│   ├── Dockerfile          # Frontend Docker configuration
│   ├── package.json        # Frontend dependencies
│   ├── render.yaml         # Frontend deployment config
│   └── DEPLOYMENT.md       # Frontend deployment guide
└── README.md               # This file
```

## 🚀 Deployment Strategy

### Backend (Django API)
- **Technology**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Deployment**: Render (Docker)
- **API Base URL**: `https://your-backend.onrender.com/api/`

### Frontend (Coming Soon)
- **Technology**: React/Vue/Next.js
- **Deployment**: Render (Static Site)
- **Domain**: `https://your-frontend.onrender.com`

## 🔧 Development

### Backend Development
```bash
cd backend
python manage.py runserver
```

### Frontend Development (When Ready)
```bash
cd frontend
npm start
```

## 📚 Documentation

- [Backend Deployment Guide](./backend/DEPLOYMENT.md)
- [Frontend Deployment Guide](./frontend/DEPLOYMENT.md) (Coming Soon)
- [API Documentation](./backend/doc/api-design.md)

## 🔗 API Endpoints

### Authentication
- `POST /api/token/` - JWT Token obtain
- `POST /api/token/refresh/` - JWT Token refresh
- `POST /api/users/` - User registration
- `POST /api/users/login/` - User login

### Blog Features
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create comment
- `GET /api/categories/` - List categories
- `GET /api/tags/` - List tags

## 🛠️ Tech Stack

### Backend
- Django 4.2+
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Docker

### Frontend (Planned)
- React/Vue/Next.js
- TypeScript
- Tailwind CSS
- Docker

## 📝 License

MIT License 