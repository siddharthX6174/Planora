# Task Manager API - Backend Service

A robust Task Management REST API built with Flask and PostgreSQL, featuring JWT authentication, task categorization, and complete CRUD operations with soft delete functionality.

---

## 🚀 Features

- **User Authentication** - Register, login, JWT token refresh, password reset
- **Task Management** - Create, read, update, delete tasks with status tracking
- **Categories** - Organize tasks with custom categories
- **Advanced Filtering** - Filter tasks by status, priority, due date
- **Pagination** - Built-in pagination for list endpoints
- **Soft Delete** - Tasks are soft-deleted, preserving data integrity
- **Rate Limiting** - Protection against brute force attacks
- **Input Validation** - Comprehensive request validation
- **Ownership Verification** - Users can only access their own data

## 🛠 Tech Stack

| Component       | Technology                            |
|----------------|---------------------------------------|
| Framework       | Flask + Flask-RESTx                   |
| Database        | PostgreSQL                            |
| ORM             | SQLAlchemy 2.0                        |
| Migrations      | Alembic                               |
| Authentication  | JWT (python-jose)                     |
| Password Hashing| bcrypt (passlib)                      |
| Validation      | Marshmallow                           |
| Rate Limiting   | Flask-Limiter                         |
| Environment     | python-dotenv                         |
| Testing         | pytest + pytest-flask                 |

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 13+
- pip (Python package manager)
- virtualenv (recommended)

## ⚙️ Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**

Create a `.env` file in the root directory:
```
Create a `.env` file in the root directory. Example for a MySQL development setup (we use `pymysql`):
# Database (MySQL)
DATABASE_URL=mysql+pymysql://root:Password123@localhost:3306/Planora

# JWT Settings
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days

# Application
FLASK_ENV=development
FLASK_APP=app/main.py
# Optional: app uses python run.py to start in development
```

5. **Create Database**
```sql
CREATE DATABASE taskmanager;
```

6. **Run Database Migrations**
```bash
flask db upgrade
```

7. **Seed Initial Data (Optional)**
```bash
flask seed-db
```

8. **Start the Server**
```bash
On Windows (PowerShell):
```powershell
cd d:\kitetsu\Planora
.\venv\Scripts\Activate.ps1
# Run the app (development)
python run.py
```

On macOS / Linux:
```bash
cd /path/to/Planora
source venv/bin/activate
python run.py
```

The API will be available at `http://localhost:5000/api/v1`

## 📁 Project Structure

```
task_manager/
├── app/
│   ├── __init__.py              # App factory
│   ├── main.py                  # Entry point
│   ├── config.py                # Configuration
│   ├── database.py              # DB setup
│   │
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── task.py
│   │   └── category.py
│   │
│   ├── schemas/                 # Marshmallow schemas
│   │   ├── user.py
│   │   ├── task.py
│   │   └── category.py
│   │
│   ├── routes/                  # Blueprints
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   ├── users.py
│   │   └── categories.py
│   │
│   ├── services/                # Business logic
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   └── user_service.py
│   │
│   └── utils/                   # Helpers
│       ├── decorators.py        # @jwt_required, etc.
│       ├── validators.py
│       └── rate_limiter.py
│
├── migrations/                  # Alembic migrations
├── tests/                       # Test suite
├── requirements.txt
├── .env
└── alembic.ini
```

## 🔌 API Endpoints

**Base URL:** `http://localhost:5000/api/v1`

### Authentication

| Method | Endpoint             | Description                         | Body                             |
|--------|----------------------|-------------------------------------|----------------------------------|
| POST   | /auth/register       | Register new user                   | {name, email, password}          |
| POST   | /auth/login          | Login & get tokens                  | {email, password}                |
| POST   | /auth/logout         | Revoke refresh token                | -                                |
| POST   | /auth/refresh        | Get new access token                | {refresh_token}                  |
| POST   | /auth/forgot-password| Request password reset              | {email}                          |
| POST   | /auth/reset-password | Reset with token                    | {token, new_password}            |

### Tasks (JWT Required)

| Method | Endpoint                       | Description                        |
|--------|--------------------------------|------------------------------------|
| GET    | /tasks                         | List all tasks (filter/paginate)   |
| POST   | /tasks                         | Create new task                    |
| GET    | /tasks/{id}                    | Get single task                    |
| PUT    | /tasks/{id}                    | Update full task                   |
| PATCH  | /tasks/{id}/status             | Update status only                 |
| DELETE | /tasks/{id}                    | Soft delete task                   |
| GET    | /tasks/search?q=               | Search tasks                       |
| POST   | /tasks/{id}/assign             | Assign task to user                |

### Users (JWT Required)

| Method | Endpoint             | Description           |
|--------|----------------------|-----------------------|
| GET    | /users/me            | Get profile           |
| PUT    | /users/me            | Update profile        |
| PUT    | /users/me/password   | Change password       |

### Categories (JWT Required)

| Method | Endpoint             | Description           |
|--------|----------------------|-----------------------|
| GET    | /categories          | List categories       |
| POST   | /categories          | Create category       |
| DELETE | /categories/{id}     | Delete category       |

## 📊 Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo',
    priority VARCHAR(20) DEFAULT 'medium',
    due_date TIMESTAMP,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    assigned_to UUID REFERENCES users(id),
    category_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#808080',
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    is_default BOOLEAN DEFAULT FALSE
);
```

## 🔐 Authentication Flow

1. **Registration**
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"SecurePass123"}'
```

2. **Login**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"SecurePass123"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

3. **Authenticated Request**
```bash
curl -X GET http://localhost:5000/api/v1/tasks \
  -H "Authorization: Bearer <access_token>"
```

4. **Refresh Token**
```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

## 📝 Usage Examples

### Create a Task
```bash
curl -X POST http://localhost:5000/api/v1/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write API docs and README",
    "priority": "high",
    "due_date": "2026-03-10T17:00:00Z",
    "category_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### List Tasks with Filters
```bash
curl "http://localhost:5000/api/v1/tasks?status=in_progress&priority=high&page=1&limit=10" \
  -H "Authorization: Bearer <token>"
```

### Update Task Status
```bash
curl -X PATCH http://localhost:5000/api/v1/tasks/{task_id}/status \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

## ⚡ Rate Limiting

| Endpoint             | Limit                          |
|----------------------|--------------------------------|
| /auth/login          | 10 requests per 15 minutes     |
| /auth/register       | 5 requests per hour            |
| /auth/forgot-password| 3 requests per hour            |
| All other endpoints  | 100 requests per day           |

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 📦 Deployment

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/taskmanager
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=taskmanager
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔒 Security Considerations

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens with short expiration (15 min access, 7 days refresh)
- Refresh tokens stored in database for revocation
- Input validation on all endpoints
- SQL injection prevention via SQLAlchemy
- CORS properly configured
- Rate limiting on auth endpoints
- Environment variables for secrets

## 🚦 Status Codes

| Code | Description                              |
|------|------------------------------------------|
| 200  | OK - Successful GET/PUT/PATCH            |
| 201  | Created - Resource created               |
| 204  | No Content - Successful DELETE           |
| 400  | Bad Request - Invalid input              |
| 401  | Unauthorized - Missing/invalid JWT       |
| 403  | Forbidden - Not resource owner           |
| 404  | Not Found - Resource doesn't exist       |
| 409  | Conflict - Duplicate email/category      |
| 422  | Unprocessable - Validation error         |
| 429  | Too Many Requests - Rate limit exceeded  |
| 500  | Server Error - Something went wrong      |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the maintainer.
