# DevLogg - Full Stack Blog Platform

A modern, Medium-like blog platform built with Django REST Framework and Next.js.

## 🏗️ Project Structure

```
blog-app/
├── backend/                 # Django REST API
│   ├── Dockerfile          # Backend Docker configuration
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Backend deployment config
│   ├── DEPLOYMENT.md       # Backend deployment guide
│   └── blog_backend/       # Django project
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities and configs
│   │   └── types/        # TypeScript types
│   ├── package.json       # Frontend dependencies
│   └── .env.local        # Environment variables
└── README.md              # This file
```

## 🚀 Deployment Strategy

### Backend (Django API) - ✅ Deployed
- **Technology**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Deployment**: Render (Docker)
- **API Base URL**: `https://blog-app-api-jyib.onrender.com/api/`

### Frontend (Next.js) - 🚧 In Development
- **Technology**: Next.js 15 (App Router)
- **UI Framework**: Tailwind CSS
- **Rich Text Editor**: TipTap
- **State Management**: TanStack Query
- **Authentication**: JWT with localStorage
- **Deployment**: Vercel/Render (Static Site)

## 🔧 Development

### Backend Development
```bash
cd backend
python manage.py runserver
```

### Frontend Development
```bash
cd frontend
npm run dev
```

## 📚 Documentation

- [Backend Deployment Guide](./backend/DEPLOYMENT.md)
- [Frontend Development Guide](./frontend/README.md)
- [API Documentation](./backend/doc/api-design.md)

## 🔗 API Endpoints

### Authentication
- `POST /api/token/` - JWT Token obtain
- `POST /api/token/refresh/` - JWT Token refresh
- `POST /api/users/` - User registration
- `GET /api/users/me/` - Get current user

### Blog Features
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `GET /api/posts/{id}/` - Get single post
- `PUT /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post
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

### Frontend
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- TipTap Rich Text Editor
- TanStack Query
- React Hook Form + Zod
- Lucide React Icons

## 📝 License

MIT License 