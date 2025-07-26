#!/bin/bash

# Stop any existing containers
docker stop $(docker ps -q --filter ancestor=blog-app-backend) 2>/dev/null || true

# Run the container with SQLite database
docker run -d \
  --name blog-app-local \
  -p 8000:8000 \
  -e DEBUG=true \
  -e DB_PASSWORD="" \
  blog-app-backend

# Wait for container to start
sleep 5

# Run migrations
docker exec blog-app-local python manage.py migrate

# Create superuser
docker exec blog-app-local python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "🚀 Blog App is running at http://localhost:8000"
echo "📊 Admin interface: http://localhost:8000/admin"
echo "🔑 Admin credentials: admin/admin123"
echo "🔗 API root: http://localhost:8000/api/" 