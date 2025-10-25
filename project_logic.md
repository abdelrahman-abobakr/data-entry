# Project Logic and Endpoints Documentation

## Overview
This is a Django REST API project for data entry management. It consists of two main apps: `accounts` for user management and authentication, and `entry` for handling data entries. The project uses JWT authentication, role-based permissions (USER and ADMIN), and supports CRUD operations on entries with approval/rejection workflows.

## Apps Structure

### 1. Accounts App
Handles user registration, authentication, and profile management.

#### Models
- **User**: Custom user model extending Django's AbstractUser
  - Fields: username, email, first_name, last_name, age, role (USER/ADMIN)
  - Role-based permissions for different access levels

#### Views
- **RegisterView**: Public endpoint for user registration
- **ProfileView**: Authenticated endpoint to retrieve current user's profile

#### Endpoints
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - JWT token obtain (login)
- `POST /api/accounts/token/refresh/` - JWT token refresh
- `GET /api/accounts/profile/` - Get current user profile

### 2. Entry App
Manages data entries with approval workflow.

#### Models
- **Entry**: Main model for data entries
  - Fields: user (FK), amount, entry_date, description, category (PERSONAL/WORK/EDUCATION), status (PENDING/APPROVED/REJECTED), approved_by, approved_at, rejection_reason
  - Validation: Amount > 0, date not in future, no duplicate entries per day per user

#### Views
- **EntryViewSet**: ModelViewSet with custom permissions and actions
  - Admins see all entries, users see only their own
  - Custom actions: approve, reject (admin only)

#### Endpoints
- `GET /api/entry/entry/` - List entries (filtered by user role)
- `POST /api/entry/entry/` - Create new entry
- `GET /api/entry/entry/{id}/` - Retrieve specific entry
- `PUT /api/entry/entry/{id}/` - Update entry
- `PATCH /api/entry/entry/{id}/` - Partial update entry
- `DELETE /api/entry/entry/{id}/` - Delete entry
- `POST /api/entry/entry/{id}/approve/` - Approve entry (admin only)
- `POST /api/entry/entry/{id}/reject/` - Reject entry (admin only, requires rejection_reason)

## Authentication & Authorization
- JWT-based authentication using `rest_framework_simplejwt`
- Default permission: IsAuthenticated
- Role-based access:
  - USER: Can only view/edit their own entries
  - ADMIN: Can view all entries, approve/reject pending entries

## Key Features
1. **User Registration & Login**: JWT tokens for secure authentication
2. **Entry Management**: Full CRUD operations with user-specific filtering
3. **Approval Workflow**: Pending entries can be approved or rejected by admins
4. **Data Validation**: Prevents invalid entries (negative amounts, future dates, duplicates)
5. **CORS Support**: Configured for frontend integration (localhost:5173)

## API Flow Examples

### User Registration & Login
1. Register: `POST /api/accounts/register/` with user details
2. Login: `POST /api/accounts/login/` to get JWT tokens
3. Use access token in Authorization header for subsequent requests

### Entry Submission & Approval
1. User creates entry: `POST /api/entry/entry/` (status: PENDING)
2. Admin views all entries: `GET /api/entry/entry/`
3. Admin approves/rejects: `POST /api/entry/entry/{id}/approve/` or `reject/`

## Settings
- Django 5.2.7 with DRF
- SQLite database
- JWT tokens (60 min access, 1 day refresh)
- CORS enabled for frontend development
- API documentation with drf-spectacular
