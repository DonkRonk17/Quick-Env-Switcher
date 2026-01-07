# Quick Environment Switcher - Example Configurations

Here are some real-world examples to get you started.

## Web Development

### Flask Application
```bash
python envswitch.py add flask-blog ~/projects/flask-blog \
  --python ~/projects/flask-blog/.venv \
  --env FLASK_APP=app.py \
  --env FLASK_ENV=development \
  --env DATABASE_URL=sqlite:///blog.db \
  --cmd "flask run" \
  --desc "Personal blog built with Flask"
```

### Django Project
```bash
python envswitch.py add django-shop ~/projects/django-shop \
  --python .venv \
  --env DJANGO_SETTINGS_MODULE=shop.settings.development \
  --env SECRET_KEY=dev-secret-key-123 \
  --env DEBUG=True \
  --cmd "python manage.py runserver" \
  --desc "E-commerce site with Django"
```

### React Frontend
```bash
python envswitch.py add react-dashboard ~/projects/react-dashboard \
  --env NODE_ENV=development \
  --env REACT_APP_API_URL=http://localhost:8000 \
  --cmd "npm start" \
  --desc "Admin dashboard in React"
```

## Data Science & ML

### Jupyter Notebook Environment
```bash
python envswitch.py add ml-research ~/research/ml-experiments \
  --python ~/research/ml-experiments/venv \
  --env JUPYTER_PORT=8888 \
  --env CUDA_VISIBLE_DEVICES=0 \
  --cmd "jupyter notebook --port 8888" \
  --desc "Machine learning research project"
```

### Data Analysis Project
```bash
python envswitch.py add data-analysis ~/data/sales-analysis \
  --python .venv \
  --env DATA_PATH=~/data/sales-analysis/raw \
  --env OUTPUT_PATH=~/data/sales-analysis/processed \
  --cmd "jupyter lab" \
  --desc "Sales data analysis Q4 2025"
```

## API Development

### FastAPI Microservice
```bash
python envswitch.py add user-api ~/microservices/user-service \
  --python .venv \
  --env SERVICE_PORT=8001 \
  --env DB_HOST=localhost \
  --env DB_NAME=users \
  --env JWT_SECRET=dev-jwt-secret \
  --cmd "uvicorn main:app --reload --port 8001" \
  --desc "User authentication microservice"
```

### REST API with Express
```bash
python envswitch.py add express-api ~/projects/express-api \
  --env NODE_ENV=development \
  --env PORT=3000 \
  --env DATABASE_URL=mongodb://localhost:27017/myapp \
  --cmd "npm run dev" \
  --desc "RESTful API with Express.js"
```

## DevOps & Infrastructure

### Terraform Project
```bash
python envswitch.py add terraform-aws ~/infrastructure/aws \
  --env AWS_PROFILE=dev \
  --env TF_VAR_environment=development \
  --env TF_VAR_region=us-east-1 \
  --cmd "terraform init" \
  --desc "AWS infrastructure as code"
```

### Docker Compose Setup
```bash
python envswitch.py add docker-stack ~/projects/docker-stack \
  --env COMPOSE_PROJECT_NAME=mystack \
  --env DOCKER_BUILDKIT=1 \
  --cmd "docker-compose up -d" \
  --desc "Multi-container Docker application"
```

## Testing & QA

### Test Environment
```bash
python envswitch.py add tests ~/projects/myapp/tests \
  --python ../.venv \
  --env TESTING=true \
  --env DATABASE_URL=sqlite:///:memory: \
  --cmd "pytest -v" \
  --desc "Test suite for myapp"
```

## Mobile Development

### React Native
```bash
python envswitch.py add mobile-app ~/projects/mobile-app \
  --env REACT_NATIVE_PACKAGER_HOSTNAME=192.168.1.100 \
  --env API_URL=http://192.168.1.100:8000 \
  --cmd "npx react-native start" \
  --desc "Cross-platform mobile app"
```

## Documentation

### Static Site Generator
```bash
python envswitch.py add docs ~/projects/docs \
  --python .venv \
  --cmd "mkdocs serve" \
  --desc "Project documentation site"
```

## Game Development

### Unity Project
```bash
python envswitch.py add unity-game ~/games/my-game \
  --env UNITY_VERSION=2021.3.20f1 \
  --cmd "open -a Unity MyGame.unity" \
  --desc "3D puzzle game"
```

## Multiple Related Projects

You can create environments for different parts of the same system:

```bash
# Frontend
python envswitch.py add myapp-frontend ~/myapp/frontend \
  --env API_URL=http://localhost:8000 \
  --cmd "npm run dev" \
  --desc "MyApp frontend"

# Backend
python envswitch.py add myapp-backend ~/myapp/backend \
  --python .venv \
  --env PORT=8000 \
  --env DB_HOST=localhost \
  --cmd "uvicorn main:app --reload" \
  --desc "MyApp backend API"

# Database
python envswitch.py add myapp-db ~/myapp \
  --cmd "docker-compose up postgres" \
  --desc "MyApp database"
```

Then switch between them:
```bash
python envswitch.py switch myapp-frontend
python envswitch.py switch myapp-backend
python envswitch.py switch myapp-db
```

---

## Tips for Organizing Environments

### Naming Conventions

Use consistent naming:
- `projectname` - Main development environment
- `projectname-test` - Testing environment
- `projectname-prod` - Production configuration
- `projectname-docs` - Documentation

### Group by Type

- `web-*` - Web applications
- `api-*` - API services
- `ml-*` - Machine learning projects
- `data-*` - Data analysis projects

### Search by Tags

While the tool doesn't have explicit tags, use descriptions:

```bash
python envswitch.py add project1 /path --desc "python, web, api"
python envswitch.py add project2 /path --desc "nodejs, frontend, react"

# Then search:
python envswitch.py list -s python
python envswitch.py list -s react
```

---

**More examples? Submit a PR with your configurations!**
