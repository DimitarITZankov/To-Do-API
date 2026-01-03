# To-Do API (Django REST Framework)

A secure and structured **To-Do REST API** built with **Django REST Framework** and **JWT authentication**.  
The API allows users to create, manage, and view tasks, with proper access control and object-level permissions.

---

## Features

- JWT Authentication (Login required)
- User-owned tasks
- Public & private tasks
- Object-level permissions (only owners can update/delete)
- Separate endpoints for:
  - Public tasks
  - User’s own tasks
- Clean serializer separation (list vs detailed views)
- Priority system (Low / Medium / High)

---

## Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- PostgreSQL (Database)

---

## API Endpoints

### Authentication
- POST /api/user/register/
- POST /api/user/login-jwt/
- POST /api/user/refresh-jwt/

### User

- GET /api/user/me
- PATCH /api/user/change-password/
- PUT /api/user/change-password/

### Tasks

- GET /api/tasks/tasks/
- POST /api/tasks/tasks/
- GET /api/tasks/tasks/{id}/
- PUT /api/tasks/tasks/{id}/
- PATCH /api/tasks/tasks/{id}/
- DELETE /api/tasks/tasks/{id}/
- POST /api/tasks/tasks/{id}/complete-task/

- GET /api/tasks/my-tasks/
- GET /api/tasks/my-tasks/{id}/
- PUT /api/tasks/my-tasks/{id}/
- PATCH /api/tasks/my-tasks/{id}/
- DELETE /api/tasks/my-tasks/{id}/

- GET /api/tasks/all-tasks/
- GET /api/tasks/all-tasks/{id}

- GET /api/tasks/completed-tasks/
- GET /api/tasks/completed-tasks/{id}/

## Instalation

1.Clone the repository
`git clone https://github.com/DimitarITZankov/To-Do-API.git
    cd To-Do-API`

2.Build and run the docker image
`docker compose up --build`

## How to setup the project
1. After installation, the server will be running on your localhost at: `http://localhost:4000/`
2. You can start exploring all endpoints from the main page: `http://localhost:4000/`

## How to use JWT Authentication
1. First, register a new account at: `http://localhost:4000/api/user/register/`
2. Log in using your credentials at: `http://localhost:4000/api/user/login-jwt/`
3. After logging in successfully, you will receive **two tokens**:
   - `access` token → use this in the **Authorization header** for all requests requiring authentication.
   - `refresh` token → use this to refresh your access token when it expires.
4. Example of using the `access` token in request headers:
  - `Authorization: Bearer <your_access_token>`

# Testing

The project includes **automated tests** for both the **tasks** and **user APIs** to ensure correctness and reliability.

## User API Tests
Tests cover:
- **User registration** – creating new users and ensuring passwords are properly handled.
- **Duplicate emails** – prevents creating multiple accounts with the same email.
- **Password validation** – enforces minimum password length.
- **JWT authentication** – ensures login works and returns access and refresh tokens.
- **Invalid credentials** – returns errors for wrong email or password.

## Tasks API Tests
Tests cover:
- **Authentication enforcement** – ensures only authenticated users can access the tasks endpoint.
- **Public visibility filtering** – returns only tasks marked as public=True.
- **Completion status filtering** – excludes tasks that are already completed.
- **Correct serialization** – verifies that the response data matches the expected task serializer output.
- **List endpoint behavior** – confirms the tasks list endpoint returns only active (not completed) public tasks.

## How to Run Tests
To run all automated tests for the project:

1. Make sure your virtual environment is active and dependencies are installed:

```bash
pip install -r requirements.txt
```

2. Run in the terminal while you are in the project's root:

```bash
docker compose run --rm app sh -c "python manage.py test"
```

### ------------------------------

```md
## Author
Dimitar Zankov  
GitHub: https://github.com/DimitarITZankov  
LinkedIn: https://linkedin.com/in/dimitar-zankov-581081379