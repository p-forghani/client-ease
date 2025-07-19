# ClientEase
ClientEase simplifies managing clients, projects, and finances.

## Prerequisites

Set the following environment variables before starting the application:

- `SECURITY_PASSWORD_SALT`
- `EMAIL_VERIFICATION_SALT`
- `DATABASE_URL`
- `SECRET_KEY`
- `SENDGRID_API_KEY`

## Getting Started

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Apply database migrations:
    ```
    flask db upgrade
    ```
3. Start the application:
    ```
    flask run
    ```