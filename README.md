# Planora

Planora is a Flask-based task management application with:

- A server-rendered web UI (`/`, `/login`, `/dashboard`, etc.)
- A JWT-protected REST API under `/api/v1/*`
- User auth, tasks, categories, and profile management

## Preview

![Planora Webpage](webpage.png)

## Status

Core functionality is working based on the current codebase and included verification scripts:

- User registration/login with JWT access + refresh tokens
- Task CRUD, search, filtering, pagination, assignment, and soft delete
- Category CRUD with default categories for new users
- Profile read/update and password change

## Tech Stack

- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- Flask-JWT-Extended
- Flask-Limiter
- Flask-CORS
- Pydantic
- Passlib (PBKDF2-SHA256)
- python-dotenv

## Project Layout

```text
Planora/
|-- app/
|   |-- main.py                  # App factory and blueprint registration
|   |-- config.py                # Environment-backed config
|   |-- database.py              # SQLAlchemy + Flask-Migrate init
|   |-- middleware/
|   |   `-- auth_middleware.py   # JWT auth decorator
|   |-- models/
|   |   |-- user.py
|   |   |-- task.py
|   |   |-- category.py
|   |   `-- token.py
|   |-- routes/
|   |   |-- auth_routes.py
|   |   |-- task_routes.py
|   |   |-- user_routes.py
|   |   |-- category_routes.py
|   |   `-- frontend_routes.py
|   |-- schemas/
|   |   |-- user.py
|   |   |-- task.py
|   |   `-- category.py
|   |-- services/
|   |   |-- auth_service.py
|   |   |-- task_service.py
|   |   |-- user_service.py
|   |   `-- category_service.py
|   |-- static/
|   `-- templates/
|-- migrations/
|-- tests/
|-- requirements.txt
|-- run.py
`-- README.md
```

## Quick Start

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`

Create `.env` in the project root:

```env
FLASK_APP=app/main.py
FLASK_ENV=development

SECRET_KEY=change-this-in-production
JWT_SECRET_KEY=change-this-too

# Use any SQLAlchemy-compatible URI
# Example (MySQL, driver included in requirements):
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/planora

# Example (PostgreSQL, install psycopg driver first):
# DATABASE_URL=postgresql://username:password@localhost:5432/planora
```

If you use PostgreSQL, install a Postgres driver (for example):

```bash
pip install psycopg2-binary
```

### 4. Initialize or apply migrations

```bash
flask --app run.py db upgrade
```

### 5. Run the app

```bash
python run.py
```

App URLs:

- Frontend: `http://localhost:5000`
- API base: `http://localhost:5000/api/v1`

## Authentication Model

Planora uses two auth styles:

- Frontend pages (`/dashboard`, `/tasks`, etc.) use Flask session auth (`session['user_id']`)
- API routes use JWT Bearer tokens in the `Authorization` header

Access token and refresh token are returned at login/registration. Refresh tokens are persisted in the `refresh_tokens` table.

## API Reference

Base URL: `/api/v1`

### Auth Routes

| Method | Endpoint         | Description |
|---|---|---|
| POST | `/auth/register` | Register a user and issue tokens |
| POST | `/auth/login` | Login and issue tokens |
| POST | `/auth/refresh` | Exchange refresh token for new access token |
| POST | `/auth/logout` | Revoke refresh token |
| GET | `/auth/me` | Get current user from JWT |

### User Routes

| Method | Endpoint             | Description |
|---|---|---|
| GET | `/users/me` | Get profile |
| PUT | `/users/me` | Update profile |
| PUT | `/users/me/password` | Change password |

### Task Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks` | List tasks (supports filters and pagination) |
| POST | `/tasks` | Create task |
| GET | `/tasks/<task_id>` | Get single task |
| PUT | `/tasks/<task_id>` | Update task |
| PATCH | `/tasks/<task_id>/status` | Update only status |
| DELETE | `/tasks/<task_id>` | Soft delete task |
| GET | `/tasks/search?q=<query>` | Search tasks by title |
| POST | `/tasks/<task_id>/assign` | Assign task to another user |

Query params for `GET /tasks`:

- `status`: `todo`, `in_progress`, `done`, `archived`
- `priority`: `low`, `medium`, `high`
- `category_id`: category UUID
- `page`: page number (default `1`)
- `limit`: page size (default `10`)

### Category Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/categories` | List categories |
| POST | `/categories` | Create category |
| PUT | `/categories/<category_id>` | Update category |
| DELETE | `/categories/<category_id>` | Delete category |

## Validation Rules

### User

- Name: `2-100` characters
- Email: valid email format
- Password: minimum 8 chars, includes at least one uppercase letter and one number

### Task

- Title: max 255 chars
- Priority: `low`, `medium`, `high`
- Status: `todo`, `in_progress`, `done`, `archived`
- `category_id`: must be UUID if provided

### Category

- Name: `1-50` chars
- Color: hex format (`#RRGGBB`)

## Task Status Transitions

Enforced in `TaskService.update_status`:

- `todo` -> `in_progress`, `done`
- `in_progress` -> `done`, `todo`
- `done` -> `archived`, `in_progress`, `todo`
- `archived` -> `todo`, `done`

When status becomes `done`, `completed_at` is set. For other statuses, `completed_at` is cleared.

## Testing

Run automated tests:

```bash
pytest
```

Run auth-focused tests:

```bash
pytest tests/test_auth.py -v
```

Manual verification scripts (require app running at `localhost:5000`):

```bash
python verify_all.py
python test_final_report.py
python test_functionality.py
```

## Notes and Limitations

- Rate limiting uses in-memory storage by default; use Redis-backed storage for production.
- Task deletion is soft delete (`deleted_at`), so deleted tasks are excluded from normal queries.
- New users are auto-seeded with default categories (`Work`, `Personal`, `Shopping`).
- Default category deletion is blocked.

## Production Checklist

- Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
- Use a production WSGI server (for example, Gunicorn)
- Configure persistent rate-limit storage (Redis)
- Serve static files via Nginx/CDN
- Enable HTTPS
- Configure logging and monitoring

## License

No license file is currently included in this repository. Add one if you plan to distribute this project publicly.
