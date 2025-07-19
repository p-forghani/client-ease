# ClientEase
ClientEase simplifies managing clients, projects, and finances.

## Prerequisites

Set the following environment variables before starting the application:

- `SECURITY_PASSWORD_SALT`
- `EMAIL_VERIFICATION_SALT`
- `DATABASE_URL`
- `SECRET_KEY`
- `SENDGRID_API_KEY`


## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Database Schema](#database-schema)
5. [Application Structure](#application-structure)
6. [Core Features](#core-features)
7. [API Endpoints](#api-endpoints)
8. [Authentication & Security](#authentication--security)
9. [Email System](#email-system)
10. [PDF Generation](#pdf-generation)
11. [Database Utilities](#database-utilities)
12. [Setup & Installation](#setup--installation)
13. [Development Guidelines](#development-guidelines)
14. [Testing](#testing)
15. [Deployment](#deployment)
16. [Roadmap](#roadmap)

## Overview

ClientEase is a comprehensive SaaS application designed to simplify client management, project tracking, and financial operations for freelancers and small businesses. The application provides a complete solution for managing clients, projects, and invoices in a single platform.

### Key Features
- **User Authentication & Authorization**: Secure login, registration, email verification, and password reset
- **Client Management**: CRUD operations for client information
- **Project Management**: Create, track, and manage projects with client associations
- **Invoice Management**: Generate, track, and download invoices as PDFs
- **Role-based Access Control**: Admin and user roles with different permissions
- **Email Notifications**: Automated email sending for account verification and password reset
- **Search & Pagination**: Advanced filtering and pagination for all data
- **PDF Generation**: Professional invoice generation with custom templates

## Architecture

ClientEase follows a **Flask Blueprint Architecture** with the following design patterns:

### Application Factory Pattern
- Uses Flask's application factory pattern for better testing and configuration management
- Modular blueprint structure for different features
- Centralized configuration management

### Blueprint Structure
```
app/
├── auth/          # Authentication & user management
├── client/        # Client management
├── project/       # Project management
├── invoice/       # Invoice management
├── admin/         # Admin functionality
├── main/          # Main routes & dashboard
├── utils/         # Utility functions
├── models/        # Database models
├── templates/     # HTML templates
└── static/        # CSS, JS, images
```

### Database Architecture
- **SQLAlchemy ORM** for database operations
- **Flask-Migrate** for database migrations
- **SQLite** for development (configurable for production)
- **Relationship Management** with proper foreign keys and cascading

## Technology Stack

### Backend
- **Flask 3.1.1**: Web framework
- **SQLAlchemy 2.0.41**: ORM for database operations
- **Flask-Login 0.6.3**: User session management
- **Flask-WTF 1.2.2**: Form handling and CSRF protection
- **Flask-Migrate 4.1.0**: Database migrations
- **Werkzeug 1.1.3**: Security utilities

### Database
- **SQLite**: Development database
- **Alembic**: Migration management

### Email & External Services
- **SendGrid**: Email delivery service
- **ReportLab**: PDF generation

### Frontend
- **Bootstrap 5.3.0**: CSS framework
- **Bootstrap Icons**: Icon library
- **Jinja2**: Template engine

### Development Tools
- **Python-dotenv**: Environment variable management
- **Pytest**: Testing framework (planned)

## Database Schema

### Core Models

#### User Model (`auth_models.py`)
```python
class User(UserMixin, db.Model):
    id: int (Primary Key)
    first_name: str (64 chars, indexed)
    last_name: str (64 chars, indexed)
    email: str (120 chars, unique, indexed)
    password_hash: str (256 chars)
    email_verified: bool (default: False)
    created_at: datetime (UTC)
    role_id: int (Foreign Key to Role)
    
    # Relationships
    clients: WriteOnlyMapped[list[Client]]
    projects: WriteOnlyMapped[list[Project]]
    invoices: WriteOnlyMapped[list[Invoice]]
```

#### Role Model (`auth_models.py`)
```python
class Role(db.Model):
    id: int (Primary Key)
    name: str (64 chars, unique, indexed)
    description: str (255 chars, optional)
```

#### Client Model (`client_models.py`)
```python
class Client(db.Model):
    id: int (Primary Key)
    name: str (100 chars, indexed)
    email: str (120 chars, unique, indexed)
    phone: str (20 chars, optional)
    address: str (Text, optional)
    created_at: datetime (UTC)
    user_id: int (Foreign Key to User)
    
    # Relationships
    user: User
    projects: list[Project]
    invoices: list[Invoice]
```

#### Project Model (`project_models.py`)
```python
class Project(db.Model):
    id: int (Primary Key)
    title: str (100 chars, indexed)
    description: str (Text, optional)
    start_date: datetime
    end_date: datetime (optional)
    client_id: int (Foreign Key to Client)
    user_id: int (Foreign Key to User)
    
    # Relationships
    client: Client
    user: User
    invoices: list[Invoice]
```

#### Invoice Model (`project_models.py`)
```python
class Invoice(db.Model):
    id: int (Primary Key)
    date: datetime
    amount: float
    description: str (Text, optional)
    status: InvoiceStatus (Enum: pending, paid, overdue, cancelled)
    project_id: int (Foreign Key to Project)
    user_id: int (Foreign Key to User)
    client_id: int (Foreign Key to Client)
    
    # Relationships
    project: Project
    user: User
    client: Client
```

### Relationships
- **User → Client**: One-to-Many (User can have multiple clients)
- **User → Project**: One-to-Many (User can have multiple projects)
- **User → Invoice**: One-to-Many (User can have multiple invoices)
- **Client → Project**: One-to-Many (Client can have multiple projects)
- **Client → Invoice**: One-to-Many (Client can have multiple invoices)
- **Project → Invoice**: One-to-Many (Project can have multiple invoices)

## Application Structure

### Blueprint Organization

#### Authentication Blueprint (`app/auth/`)
- **Purpose**: Handle user authentication and account management
- **Files**:
  - `auth_routes.py`: Authentication routes (login, register, logout, password reset)
  - `auth_forms.py`: WTForms for authentication forms
  - `auth_emails.py`: Email templates and sending logic
  - `__init__.py`: Blueprint registration

#### Client Blueprint (`app/client/`)
- **Purpose**: Manage client information and operations
- **Files**:
  - `client_routes.py`: CRUD operations for clients
  - `client_forms.py`: Forms for client creation and editing
  - `__init__.py`: Blueprint registration

#### Project Blueprint (`app/project/`)
- **Purpose**: Manage project lifecycle and tracking
- **Files**:
  - `prj_routes.py`: Project CRUD operations
  - `prj_forms.py`: Project forms
  - `__init__.py`: Blueprint registration

#### Invoice Blueprint (`app/invoice/`)
- **Purpose**: Handle invoice creation, management, and PDF generation
- **Files**:
  - `inv_routes.py`: Invoice operations and PDF download
  - `inv_forms.py`: Invoice forms
  - `__init__.py`: Blueprint registration

#### Admin Blueprint (`app/admin/`)
- **Purpose**: Administrative functions (currently minimal)
- **Files**:
  - `admin_routes.py`: Admin-specific routes
  - `__init__.py`: Blueprint registration

#### Main Blueprint (`app/main/`)
- **Purpose**: Main application routes and dashboard
- **Files**:
  - `main_routes.py`: Index and main pages
  - `__init__.py`: Blueprint registration

### Utility Modules (`app/utils/`)

#### Database Utilities (`db.py`)
- **`paginate_query()`**: Generic pagination for any query
- **`search_in_query()`**: Generic search functionality across multiple fields
- **`apply_filters_to_query()`**: Dynamic filter application
- **`get_client_by_name()`**: Client lookup utility

#### PDF Generation (`pdf.py`)
- **`generate_invoice()`**: Creates professional PDF invoices using ReportLab
- Features:
  - Custom styling and layout
  - Professional invoice format
  - Payment method information
  - Tax calculation support (planned)

#### Email Utilities (`email_utils.py`)
- **`send_email()`**: Asynchronous email sending using SendGrid
- **`send_async_email()`**: Background email processing
- Features:
  - Thread-safe email sending
  - HTML and text content support
  - Error handling and logging

#### Security Decorators (`decorators.py`)
- **`admin_only()`**: Restrict access to admin users only
- Role-based access control implementation

## Core Features

### 1. User Authentication System

#### Registration Process
1. User fills registration form
2. Account created with email verification required
3. Verification email sent via SendGrid
4. User clicks verification link to activate account

#### Login System
- Session-based authentication using Flask-Login
- Remember me functionality
- Secure password hashing with Werkzeug

#### Password Reset
1. User requests password reset
2. Reset token generated with expiration
3. Reset email sent with secure link
4. User sets new password via token verification

### 2. Client Management

#### Features
- **Create**: Add new clients with contact information
- **Read**: View client details with associated projects and invoices
- **Update**: Edit client information
- **Delete**: Remove clients (cascades to projects and invoices)
- **Search**: Search across name, email, phone, and address
- **Pagination**: Efficient data loading for large datasets

#### Data Validation
- Email uniqueness validation
- Required field validation
- Phone number formatting

### 3. Project Management

#### Features
- **Create**: New projects with client association
- **Read**: View project details and timeline
- **Update**: Modify project information
- **Delete**: Remove projects
- **Client Association**: Link projects to specific clients
- **Date Tracking**: Start and end date management

#### Project Lifecycle
- Project creation with client selection
- Timeline tracking with start/end dates
- Invoice generation capability
- Status tracking (planned)

### 4. Invoice Management

#### Features
- **Create**: Generate invoices for projects
- **Read**: View invoice details and status
- **Update**: Modify invoice information
- **Delete**: Remove invoices
- **PDF Generation**: Download professional PDF invoices
- **Status Tracking**: Pending, paid, overdue, cancelled

#### Invoice Workflow
1. Select project for invoice creation
2. Fill invoice details (amount, description, date)
3. Generate and download PDF
4. Track payment status

### 5. Search and Filtering

#### Search Functionality
- **Multi-field Search**: Search across multiple database fields
- **Case-insensitive**: ILIKE queries for flexible matching
- **Partial Matching**: Substring search support

#### Pagination
- **Configurable Page Size**: Default 10 items per page
- **URL Parameters**: Page and per_page query parameters
- **Error Handling**: Graceful handling of invalid page numbers

#### Filtering
- **Status Filtering**: Filter invoices by status
- **Date Filtering**: Filter by specific dates
- **Extensible**: Easy to add new filter types

## API Endpoints

### Authentication Routes
```
POST   /auth/login              # User login
POST   /auth/register           # User registration
GET    /auth/logout             # User logout
POST   /auth/forgot-password    # Password reset request
GET    /auth/reset-password/<token>  # Password reset form
POST   /auth/reset-password/<token>  # Password reset submission
GET    /auth/verify_email/<token>    # Email verification
```

### Client Routes
```
GET    /client/                 # List all clients
POST   /client/add              # Create new client
GET    /client/<client_id>      # View client details
GET    /client/<client_id>/edit # Edit client form
POST   /client/<client_id>/edit # Update client
POST   /client/<client_id>/delete # Delete client
```

### Project Routes
```
GET    /project/                # List all projects
POST   /project/create          # Create new project
GET    /project/<prj_id>        # View project details
GET    /project/update/<prj_id> # Edit project form
POST   /project/update/<prj_id> # Update project
GET    /project/delete/<prj_id> # Delete project confirmation
POST   /project/delete/<prj_id> # Delete project
```

### Invoice Routes
```
GET    /invoice/                # List all invoices
POST   /invoice/create          # Create new invoice
GET    /invoice/<id>            # View invoice details
GET    /invoice/edit/<id>       # Edit invoice form
PUT    /invoice/edit/<id>       # Update invoice
DELETE /invoice/<id>            # Delete invoice
GET    /invoice/<inv_id>/download # Download PDF invoice
```

### Main Routes
```
GET    /                        # Application dashboard
```

## Authentication & Security

### Security Features
- **Password Hashing**: Secure password storage using Werkzeug
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms
- **Session Management**: Flask-Login for secure session handling
- **Token-based Verification**: Secure email verification and password reset
- **Role-based Access**: Admin and user role separation

### Token System
- **Email Verification Tokens**: 24-hour expiration
- **Password Reset Tokens**: 24-hour expiration
- **Salt-based Security**: Different salts for different token types
- **URL-safe Serialization**: Secure token generation and verification

### Access Control
- **Login Required**: Protected routes require authentication
- **Admin-only Routes**: Restricted access for administrative functions
- **User Data Isolation**: Users can only access their own data
- **Authorization Checks**: Proper permission validation

## Email System

### Email Configuration
- **SendGrid Integration**: Professional email delivery service
- **Asynchronous Sending**: Background email processing
- **HTML Templates**: Rich email content
- **Error Handling**: Graceful failure handling

### Email Types
1. **Account Verification**: Welcome email with verification link
2. **Password Reset**: Secure password reset instructions
3. **Notification Emails**: System notifications (planned)

### Email Templates
- **Verification Email**: Account activation with secure token
- **Password Reset Email**: Reset instructions with time-limited token
- **Customizable Content**: HTML and text versions

## PDF Generation

### Invoice PDF Features
- **Professional Layout**: Clean, business-ready design
- **Custom Styling**: Branded invoice appearance
- **Complete Information**: All invoice details included
- **Payment Methods**: Payment instruction section
- **Tax Support**: Framework for tax calculations

### PDF Generation Process
1. **Data Collection**: Gather invoice and related data
2. **Template Rendering**: Apply professional styling
3. **Buffer Generation**: Create in-memory PDF
4. **File Download**: Stream PDF to user

### Technical Implementation
- **ReportLab Library**: Professional PDF generation
- **A4 Format**: Standard business document size
- **Custom Styling**: Professional color scheme and typography
- **Table Layout**: Structured invoice item presentation

## Database Utilities

### Pagination Utility
```python
def paginate_query(query, request, page=None, per_page=None, error_out=True)
```
- **Generic Pagination**: Works with any SQLAlchemy query
- **URL Parameters**: Reads page and per_page from request
- **Error Handling**: Configurable error handling for invalid pages
- **Default Values**: Sensible defaults for page size

### Search Utility
```python
def search_in_query(query, request, fields)
```
- **Multi-field Search**: Search across multiple database columns
- **Case-insensitive**: Uses ILIKE for flexible matching
- **Partial Matching**: Substring search support
- **Field Specification**: Configurable search fields

### Filter Utility
```python
def apply_filters_to_query(query, model, filters)
```
- **Dynamic Filtering**: Apply filters based on request parameters
- **Multiple Filter Types**: Status, date, and relationship filters
- **Extensible Design**: Easy to add new filter types
- **Query Optimization**: Efficient database queries

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git for version control

### Environment Variables
Create a `.env` file with the following variables:
```bash
SECURITY_PASSWORD_SALT=your_security_salt_here
EMAIL_VERIFICATION_SALT=your_email_salt_here
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your_secret_key_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
```

### Installation Steps
1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd client-ease
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

4. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Initialize Database**
   ```bash
   flask db upgrade
   ```

6. **Run Application**
   ```bash
   flask run
   ```

### Development Setup
1. **Enable Debug Mode**
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=1
   ```

2. **Database Migrations**
   ```bash
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

## Development Guidelines

### Code Style
- **PEP 8 Compliance**: Follow Python style guidelines
- **Type Hints**: Use type annotations for better code clarity
- **Docstrings**: Comprehensive documentation for functions and classes
- **Error Handling**: Proper exception handling and logging

### Database Guidelines
- **Migrations**: Always use migrations for database changes
- **Relationships**: Define proper foreign key relationships
- **Indexing**: Add indexes for frequently queried fields
- **Cascading**: Use appropriate cascade options for data integrity

### Security Guidelines
- **Input Validation**: Validate all user inputs
- **SQL Injection Prevention**: Use parameterized queries
- **XSS Prevention**: Sanitize user-generated content
- **CSRF Protection**: Include CSRF tokens in all forms

### Testing Guidelines
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test complete workflows
- **Database Tests**: Use test database for testing
- **Mock External Services**: Mock email and PDF services

## Testing

### Test Structure
```
tests/
├── conftest.py          # Test configuration and fixtures
├── unit/                # Unit tests
│   ├── test_models.py   # Model tests
│   ├── test_utils.py    # Utility function tests
│   └── test_auth.py     # Authentication tests
└── functional/          # Functional tests
    ├── test_client.py   # Client workflow tests
    ├── test_project.py  # Project workflow tests
    └── test_invoice.py  # Invoice workflow tests
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_models.py

# Run with coverage
pytest --cov=app

# Run with verbose output
pytest -v
```

### Test Configuration
- **Test Database**: In-memory SQLite database
- **Mock Services**: Mocked email and PDF services
- **Test Data**: Fixtures for consistent test data
- **Cleanup**: Automatic test data cleanup

## Deployment

### Production Considerations
- **Database**: Use PostgreSQL or MySQL for production
- **Web Server**: Deploy with Gunicorn or uWSGI
- **Reverse Proxy**: Use Nginx for static files and load balancing
- **Environment Variables**: Secure configuration management
- **SSL/TLS**: Enable HTTPS for security

### Deployment Options
1. **Heroku**: Easy deployment with Git integration
2. **AWS**: Scalable cloud deployment
3. **DigitalOcean**: VPS deployment
4. **Docker**: Containerized deployment

### Environment Configuration
```bash
# Production environment variables
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=production_secret_key
SENDGRID_API_KEY=production_api_key
```

## Roadmap

### Phase 1: Core Foundation ✅
- [x] User Authentication
- [x] User Roles and Permissions
- [x] Client Management
- [x] Basic CRUD operations

### Phase 2: Core Features ✅
- [x] Project Management
- [x] Invoice Management
- [x] Email Notifications
- [x] PDF Generation

### Phase 3: Advanced Features (Planned)
- [ ] Billing/Subscription System
- [ ] Advanced Permissions
- [ ] Data Analytics and Reporting
- [ ] Audit Logs
- [ ] Security Enhancements

### Phase 4: Scaling and Performance (Planned)
- [ ] File Uploads and Storage
- [ ] Advanced Searching and Filtering
- [ ] API Integration
- [ ] Performance Optimization

### Phase 5: Polishing (Planned)
- [ ] Comprehensive Testing
- [ ] API Documentation
- [ ] Deployment Automation
- [ ] Monitoring and Error Tracking

### Future Enhancements
- **Mobile App**: Native mobile application
- **API Development**: RESTful API for third-party integration
- **Advanced Analytics**: Business intelligence and reporting
- **Multi-tenancy**: Support for multiple organizations
- **Payment Integration**: Stripe/PayPal integration
- **Calendar Integration**: Project timeline management
- **Document Management**: File storage and organization

## Conclusion

ClientEase is a well-structured, scalable application that provides comprehensive client and project management capabilities. The modular architecture, security features, and extensible design make it suitable for both small businesses and enterprise use cases.

The application follows Flask best practices and includes proper error handling, security measures, and documentation. The roadmap provides a clear path for future development and enhancement.

For developers working on this project, the codebase is well-organized with clear separation of concerns, comprehensive documentation, and adherence to Python best practices. The modular design makes it easy to add new features and maintain existing functionality. 