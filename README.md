
# User Management & Permissions

This project is designed for user management and permissions using Django and Django REST Framework. Users can view, edit, and delete their information, and access control is managed based on user roles (Admin and non-Admin).

## Features

1. **CustomUser Model**  
   The `CustomUser` model has been created with `is_admin` and `is_user` fields to manage user roles and permissions.

2. **CustomUserManager**  
   Methods `create_user` and `create_superuser` have been added to create regular and admin users.

3. **Views**  
   - `UserListView`: Used for listing and creating users using `ListCreateAPIView`.
   - `UserDetailView`: Used for retrieving, updating, and deleting users using `RetrieveUpdateDestroyAPIView`.

4. **Permissions**  
   - `IsAuthenticated`: Ensures only authenticated users can access the API.
   - `IsAdminUser`: Restricts access to admin users for editing, deleting, and viewing other users' details.

5. **CustomUser Serializer**  
   A serializer for the `CustomUser` model has been created to convert data into JSON format for API use.

6. **URL Configuration**  
   API endpoints for listing and retrieving user details have been configured.

7. **Role-based Access Testing**  
   Role-based access control has been tested, ensuring that only admin users can access specific API endpoints.

8. **Simple Admin Panel**  
   A simple admin panel has been created using Django Templates and Bootstrap for user management and access control.

9. **Change Password**  
   Users can change their passwords.

10. **Forgot Password**  
    A feature for sending email to users for password recovery has been added.

11. **Testing**  
    Tests have been written to ensure the proper functionality of the API endpoints, including various scenarios like authentication success, admin access, and error handling.

12. **Logging**  
    Logging has been added for important events like user login, updates to user data, and error tracking to help with debugging.

13. **API Documentation with Swagger**  
    API documentation is available using Swagger for easy integration and use by others.

## Installation and Setup

Follow these steps to get the project up and running:

1. **Create a Virtual Environment**  
   Create a virtual environment using `venv`:
   ```bash
   python -m venv .venv
   ```

2. **Install Dependencies**  
   Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**  
   Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

4. **Start the Server**  
   Run the Django server:
   ```bash
   python manage.py runserver
   ```

## Using the API

### Login

- **Endpoint**: `/api/login/`
- **Method**: POST
- **Input Data**:  
  - `email`: User's email  
  - `password`: User's password

### Signup

- **Endpoint**: `/api/signup/`
- **Method**: POST
- **Input Data**:  
  - `email`: User's email  
  - `password`: User's password  
  - `is_admin`: User's role (optional)

### User CRUD (Create, Read, Update, Delete)

- **Endpoint**: `/api/users/{user_id}/`
- **Methods**: GET, PUT, DELETE
- **Input Data**:  
  - For PUT: Provide the new data for the user  

### Change Password

- **Endpoint**: `/api/change-password/`
- **Method**: POST
- **Input Data**:  
  - `old_password`: Current password  
  - `new_password`: New password  

## API Documentation

API documentation is available via Swagger. After running the server, visit the following URL:
```
http://localhost:8000/swagger/
```

## Project Structure

```
user_management/
├── users/                # User management app
│   ├── migrations/       # Database migration files
│   ├── models.py         # Models
│   ├── serializers.py    # Serializers
│   ├── views.py          # Views
│   ├── urls.py           # URL routing
│   └── tests.py          # Tests
├── user_management/      # Main project settings
│   └── settings.py       # Django settings
├── manage.py             # Django management script
```

