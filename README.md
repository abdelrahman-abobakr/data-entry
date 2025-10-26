# Data Entry Management System

A full-stack web application for managing data entries with an approval workflow. Users can submit entries (e.g., expenses, time logs, or other data submissions) that require administrative approval before being finalized.

## Table of Contents
- [Setup and Running Instructions](#setup-and-running-instructions)
- [Design Decisions](#design-decisions)
- [Technology Stack](#technology-stack)
- [API Documentation](#api-documentation)
- [Assumptions and Limitations](#assumptions-and-limitations)
- [Future Improvements](#future-improvements)

## Setup and Running Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+ (for Vue frontend)
- pip (Python package manager)
- npm or yarn (for Vue dependencies)

### Backend Setup (Django)

1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone <repository-url>
   cd data-entry-frappy-task
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Django development server:**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup (Vue.js)

1. **Navigate to the frontend directory (assuming it's in a separate `frontend` folder):**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at `http://localhost:5173`

### Testing the Application

1. **Access the API documentation:**
   - Swagger UI: `http://localhost:8000/api/docs/swagger/`
   - ReDoc: `http://localhost:8000/api/docs/redoc/`

2. **Register a new user** via the API or admin panel.

3. **Obtain JWT tokens** by logging in.

4. **Test entry submission and approval workflow.**

## Design Decisions

### Problem Domain
This application addresses the need for organizations to manage user-submitted data entries that require approval workflows. Common use cases include:
- Expense report submissions
- Time tracking entries
- Project data submissions
- Any scenario where user input needs validation and approval by administrators

### Why This Approach?
- **Role-based Access Control:** Separates user and admin responsibilities, ensuring data integrity and proper oversight.
- **Approval Workflow:** Prevents invalid or unauthorized entries from being processed immediately, allowing for review and compliance checks.
- **RESTful API Design:** Provides a clean, scalable interface for frontend integration and potential mobile app development.
- **JWT Authentication:** Secure, stateless authentication suitable for modern web applications.
- **Data Validation:** Built-in validation prevents common errors like duplicate entries, future dates, and invalid amounts.

### Key Features
- User registration and authentication
- Entry submission with categorization
- Admin approval/rejection system
- Comprehensive filtering and search capabilities
- API documentation with OpenAPI/Swagger

## Technology Stack

### Backend
- **Django 5.2.7:** Robust web framework with excellent security features and ORM
- **Django REST Framework (DRF):** Powerful toolkit for building Web APIs
- **JWT Authentication:** `djangorestframework-simplejwt` for secure token-based auth
- **Database:** SQLite (development) - easily configurable for PostgreSQL/MySQL in production
- **API Documentation:** `drf-spectacular` for OpenAPI/Swagger documentation
- **CORS Support:** `django-cors-headers` for frontend integration

### Frontend
- **Vue.js:** Progressive JavaScript framework for building user interfaces
- **Axios:** HTTP client for API communication
- **Vue Router:** Official routing library for Vue.js
- **Pinia/Vuex:** State management (depending on Vue version)

### Development Tools
- **Python Virtual Environment:** Isolated dependency management
- **Django Admin:** Built-in admin interface for data management
- **DRF Browsable API:** Interactive API testing interface

## API Documentation

### Authentication Endpoints

#### Register User
- **URL:** `POST /api/accounts/register/`
- **Permissions:** Public
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "password": "securepassword123",
    "password2": "securepassword123",
    "role": "USER"
  }
  ```
- **Response:** User object with all fields

#### Login (Obtain JWT Tokens)
- **URL:** `POST /api/accounts/login/`
- **Permissions:** Public
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Response:**
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### Refresh Token
- **URL:** `POST /api/accounts/token/refresh/`
- **Request Body:**
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### Get User Profile
- **URL:** `GET /api/accounts/profile/`
- **Permissions:** Authenticated
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Current user profile data

### Entry Management Endpoints

#### List Entries
- **URL:** `GET /api/entry/entry/`
- **Permissions:** Authenticated (users see own entries, admins see all)
- **Query Parameters:**
  - `status`: Filter by PENDING/APPROVED/REJECTED
  - `category`: Filter by PERSONAL/WORK/EDUCATION
  - `search`: Search in title and description
  - `ordering`: Order by created_at (use `-created_at` for descending)
- **Response:** Paginated list of entries

#### Create Entry
- **URL:** `POST /api/entry/entry/`
- **Permissions:** Authenticated
- **Request Body:**
  ```json
  {
    "title": "Office Supplies",
    "amount": 150.00,
    "entry_date": "2023-10-15",
    "description": "Purchased notebooks and pens",
    "category": "WORK"
  }
  ```
- **Response:** Created entry object (status: PENDING)

#### Retrieve/Update/Delete Entry
- **URLs:**
  - `GET /api/entry/entry/{id}/` - Retrieve
  - `PUT /api/entry/entry/{id}/` - Full update
  - `PATCH /api/entry/entry/{id}/` - Partial update
  - `DELETE /api/entry/entry/{id}/` - Delete
- **Permissions:** Authenticated (users can only modify their own entries)

#### Approve Entry
- **URL:** `POST /api/entry/entry/{id}/approve/`
- **Permissions:** Admin only
- **Response:** Updated entry with APPROVED status

#### Reject Entry
- **URL:** `POST /api/entry/entry/{id}/reject/`
- **Permissions:** Admin only
- **Request Body:**
  ```json
  {
    "rejection_reason": "Amount exceeds budget limit"
  }
  ```
- **Response:** Updated entry with REJECTED status

### Entry Model Fields
```json
{
  "id": 1,
  "user": 1,
  "title": "Office Supplies",
  "amount": "150.00",
  "entry_date": "2023-10-15",
  "description": "Purchased notebooks and pens",
  "category": "WORK",
  "status": "PENDING",
  "approved_by": null,
  "approved_at": null,
  "rejection_reason": null,
  "created_at": "2023-10-15T10:00:00Z",
  "updated_at": "2023-10-15T10:00:00Z"
}
```

## Assumptions and Limitations

### Assumptions
- Users are trusted to submit accurate data initially
- Administrators will review entries promptly
- The application is used within an organizational context
- Entry amounts represent monetary values (USD or similar)
- Categories (PERSONAL, WORK, EDUCATION) cover all use cases
- JWT tokens are stored securely on the frontend
- CORS configuration is sufficient for the development environment

### Limitations
- **Database:** SQLite is used for development; production deployments should use PostgreSQL or MySQL
- **Authentication:** No password reset functionality implemented
- **File Uploads:** No support for attaching receipts or documents to entries
- **Notifications:** No email or in-app notifications for approval/rejection
- **Audit Trail:** Limited tracking of entry modifications
- **Scalability:** Basic pagination; may need optimization for large datasets
- **Security:** No rate limiting or advanced security measures implemented
- **Frontend Integration:** Vue frontend is assumed but not included in this repository
- **Testing:** Limited unit and integration tests
- **Deployment:** No Docker configuration or production deployment scripts

## Future Improvements

### High Priority
- **Email Notifications:** Notify users when entries are approved/rejected
- **File Attachments:** Allow users to upload receipts or supporting documents
- **Advanced Filtering:** Date range filters, amount range filters
- **Dashboard Analytics:** Charts and reports for admins
- **Password Reset:** Implement forgot password functionality
- **Two-Factor Authentication:** Enhanced security for admin accounts

### Medium Priority
- **Bulk Operations:** Allow admins to approve/reject multiple entries at once
- **Comments System:** Enable admins to add comments during approval/rejection
- **Entry Templates:** Pre-defined templates for common entry types
- **Export Functionality:** Export entries to CSV/PDF
- **Mobile App:** Native mobile application using React Native or Flutter
- **Real-time Updates:** WebSocket integration for live notifications

### Low Priority
- **Advanced Search:** Full-text search with Elasticsearch
- **Workflow Customization:** Configurable approval workflows
- **Multi-tenancy:** Support for multiple organizations
- **API Rate Limiting:** Prevent abuse with request throttling
- **Audit Logs:** Comprehensive logging of all user actions
- **Internationalization:** Support for multiple languages
- **Progressive Web App:** PWA features for better mobile experience

### Technical Improvements
- **Testing Suite:** Comprehensive unit, integration, and E2E tests
- **CI/CD Pipeline:** Automated testing and deployment
- **Docker Containerization:** Easy deployment and scaling
- **Monitoring:** Application performance monitoring and error tracking
- **Caching:** Redis integration for improved performance
- **API Versioning:** Support for multiple API versions
- **GraphQL:** Alternative API interface for complex queries
