# Planora - Task Management Application

A modern, full-stack Task Management application built with Flask backend and dynamic frontend, featuring JWT authentication, real-time task synchronization, and comprehensive task categorization with an intuitive user interface.

---

## 🚀 Features

### User Management
- **User Registration & Authentication** - Secure registration with email validation and password requirements
- **JWT Token Authentication** - Access tokens (15 min) and refresh tokens (7 days)
- **Profile Management** - View and edit user profile information
- **Password Management** - Change password functionality
- **Dynamic User Statistics** - Real-time task insights and completion metrics

### Task Management
- **Full CRUD Operations** - Create, read, update, delete tasks with soft delete
- **Task Status Tracking** - Flexible status transitions (todo → in_progress → done → archived)
- **Task Priorities** - Low, Medium, High priority levels
- **Due Dates** - Task deadline management
- **Task Search & Filtering** - Filter by status, priority, categories
- **Task Pagination** - Built-in pagination support

### Dashboard Features
- **Dynamic Dashboard** - Real-time task overview with statistics
- **Task Insights** - Track total tasks, completed tasks, categories, and completion rate
- **Grid & List Views** - Switch between grid and list view for task management
- **Task Actions** - Complete, edit, and delete tasks directly from dashboard
- **Responsive Design** - Mobile-friendly interface with Flexbox and CSS Grid

### Categories & Organization
- **Custom Categories** - Create and manage task categories
- **Category Colors** - Assign colors to categories for better organization
- **Category-Task Association** - Link tasks to categories
- **Dynamic Category Loading** - Categories populate dynamically from database

---

## 🛠 Tech Stack

| Layer       | Technology                                |
|-------------|-------------------------------------------|
| **Frontend**| HTML5, CSS3, Vanilla JavaScript          |
| **Backend** | Flask, Flask-RESTx                       |
| **Database**| MySQL with SQLAlchemy 2.0 ORM            |
| **Auth**    | JWT (python-jose), bcrypt hashing        |
| **Validation** | Marshmallow schemas                   |
| **Migrations** | Alembic                                |
| **Environment** | python-dotenv                          |

---

## 📋 Prerequisites

- Python 3.9+
- MySQL 5.7+
- pip (Python package manager)
- virtualenv (recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Planora.git
cd Planora
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create `.env` file in root directory:
```
# Flask Configuration
FLASK_APP=app/main.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=604800

# Database (MySQL)
DATABASE_URL=mysql+pymysql://root:Password123@localhost:3306/planora
```

### 5. Create Database
```sql
CREATE DATABASE planora;
```

### 6. Run Database Migrations
```bash
flask db upgrade
```

### 7. Start Application
```bash
python run.py
```

The application will be available at:
- **Frontend**: http://localhost:5000
- **API**: http://localhost:5000/api/v1

---

## 📁 Project Structure

```
Planora/
├── app/
│   ├── __init__.py              # App factory
│   ├── main.py                  # Flask app entry point
│   ├── config.py                # Configuration
│   ├── database.py              # SQLAlchemy setup
│   │
│   ├── models/                  # Database models
│   │   ├── user.py              # User model
│   │   ├── task.py              # Task model
│   │   ├── category.py          # Category model
│   │   └── token.py             # Token model
│   │
│   ├── schemas/                 # Marshmallow validation schemas
│   │   ├── user.py
│   │   ├── task.py
│   │   └── category.py
│   │
│   ├── routes/                  # API blueprints
│   │   ├── auth_routes.py       # /api/v1/auth/*
│   │   ├── task_routes.py       # /api/v1/tasks/*
│   │   ├── user_routes.py       # /api/v1/users/*
│   │   ├── category_routes.py   # /api/v1/categories/*
│   │   └── frontend_routes.py   # Frontend pages
│   │
│   ├── services/                # Business logic layer
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── user_service.py
│   │   └── category_service.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth_middleware.py   # JWT verification
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Main stylesheet
│   │   └── js/
│   │       ├── api.js           # API integration
│   │       └── script.js        # Frontend logic
│   │
│   └── templates/               # HTML templates
│       ├── base.html            # Base template
│       ├── index.html           # Homepage
│       ├── login.html           # Login page
│       ├── register.html        # Registration page
│       ├── dashboard.html       # Task dashboard (dynamic)
│       ├── tasks.html           # Tasks list/grid view (dynamic)
│       ├── categories.html      # Categories page
│       └── profile.html         # User profile
│
├── migrations/                  # Alembic database migrations
├── tests/                       # Test suite
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md
```

---

## 🔌 API Endpoints

**Base URL:** `http://localhost:5000/api/v1`

### Authentication

| Method | Endpoint           | Description              | Auth Required |
|--------|-------------------|--------------------------|---------------|
| POST   | `/auth/register`  | Register new user         | No            |
| POST   | `/auth/login`     | Login & get tokens        | No            |
| POST   | `/auth/logout`    | Logout & revoke token     | Yes           |
| POST   | `/auth/refresh`   | Get new access token      | No            |

### Tasks

| Method | Endpoint                   | Description                  | Auth Required |
|--------|---------------------------|------------------------------|---------------|
| GET    | `/tasks`                  | List all tasks (paginated)   | Yes           |
| POST   | `/tasks`                  | Create new task              | Yes           |
| GET    | `/tasks/{id}`             | Get single task              | Yes           |
| PUT    | `/tasks/{id}`             | Update task details          | Yes           |
| PATCH  | `/tasks/{id}/status`      | Update task status only      | Yes           |
| DELETE | `/tasks/{id}`             | Soft delete task             | Yes           |
| GET    | `/tasks/search?q=query`   | Search tasks by title        | Yes           |

### Users

| Method | Endpoint             | Description           | Auth Required |
|--------|----------------------|-----------------------|---------------|
| GET    | `/users/me`          | Get user profile      | Yes           |
| PUT    | `/users/me`          | Update profile        | Yes           |
| PUT    | `/users/me/password` | Change password       | Yes           |

### Categories

| Method | Endpoint           | Description        | Auth Required |
|--------|--------------------|--------------------|---------------|
| GET    | `/categories`      | List all categories| Yes           |
| POST   | `/categories`      | Create category    | Yes           |
| PUT    | `/categories/{id}` | Update category    | Yes           |
| DELETE | `/categories/{id}` | Delete category    | Yes           |

---

## 📊 Frontend Pages

### Dashboard (`/dashboard`)
- **Real-time Task Statistics**: Total tasks, completed tasks, categories, completion rate
- **Task Management**: View, complete, delete tasks
- **Filters**: Search by title, filter by status and priority
- **Sorting**: Sort by due date, priority, or title
- **Dynamic Loading**: Tasks loaded from API on page load

### Tasks (`/tasks`)
- **Grid & List Views**: Toggle between grid and list layouts
- **Dynamic Grid Cards**: Task cards populated from database
- **Full Task Details**: Title, description, priority, status, due date
- **Quick Actions**: Edit, complete, delete buttons
- **Filtering & Searching**: Search and filter by status/priority

### Profile (`/profile`)
- **Edit Profile**: Edit name, email, phone, location
- **Profile Statistics**: Real-time task insights
- **Account Management**: View account status and member since date
- **Security Settings**: Change password, 2FA settings

### Categories (`/categories`)
- **View All Categories**: Display user categories
- **Create Categories**: Add new categories with custom colors
- **Manage Categories**: Edit and delete categories

---

## 🔄 Task Status Transitions

The application supports flexible task status transitions:

```
todo ──→ in_progress ──→ done ──→ archived
  ↓          ↓           ↓         ↓
  └──────────┴───────────┴─────────┘
```

- **todo**: New tasks start here
- **in_progress**: Task is currently being worked on
- **done**: Task is completed
- **archived**: Completed/inactive tasks

You can transition directly from `todo` to `done` using the "Complete" button for quick task completion.

---

## 🔐 Authentication & Security

### JWT Token Flow
1. User registers or logs in
2. Server returns `access_token` (15 minutes) and `refresh_token` (7 days)
3. Client includes `access_token` in Authorization header
4. When access token expires, use `refresh_token` to get a new one
5. Tokens stored in browser `localStorage`

### Password Security
- Minimum 8 characters
- Must contain uppercase letter
- Must contain number
- Hashed with bcrypt (12 rounds)

### Data Protection
- SQL injection prevention via SQLAlchemy ORM
- XSS protection via template escaping
- CSRF tokens for form submissions
- Input validation on all endpoints
- Ownership verification - users can only access their own data

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app tests/
```

---

## 🚀 Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app/main.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.main:app"]
```

---

## 🐛 Troubleshooting

### Issue: "Database connection refused"
- Ensure MySQL is running
- Check DATABASE_URL in .env file
- Verify MySQL credentials

### Issue: "JWT token invalid"
- Clear browser cache and localStorage
- Log out and log back in
- Ensure JWT_SECRET_KEY matches in .env

### Issue: "Tasks not loading on dashboard"
- Check browser console for errors (F12)
- Ensure user is authenticated
- Verify API is running on correct port
- Check network tab for API response

### Issue: "Password change fails"
- Ensure old password is correct
- Password must meet requirements (8+ chars, uppercase, number)
- Check console for validation errors

---

## 📝 Recent Updates

### Version 1.1.0 (March 2026)
✅ **Dashboard Improvements**
- Fixed hardcoded task cards - now dynamic
- Real-time task statistics
- Task filtering and sorting
- Completion/status tracking

✅ **Profile Management**
- Functional edit profile modal
- Password change feature
- Dynamic user statistics

✅ **Task Management**
- Fixed task status transitions (todo → done directly supported)
- Dynamic grid view in tasks page
- Complete, edit, delete functionality
- Search and filter features

✅ **Frontend Polish**
- Responsive design improvements
- Better error handling
- Loading states

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review test files for usage examples

---

**Last Updated:** March 6, 2026  
**Status:** ✅ Fully Functional
