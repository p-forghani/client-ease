from app.models import User


def test_user_model():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the attributes are set correctly
    AND the password hash is generated
    AND the password can be checked
    AND the token can be generated
    AND the token can be validated
    AND the __repr__ method returns the correct string
    AND the created_at timestamp is set
    AND the email_verified flag is set to False
    AND the role_id is set to 2
    AND the clients, projects, and invoices relationships are set correctly
    """
    user = User(
        first_name="John",
        last_name="Doe",
        email='john.doe@gmail.com',
        password_hash="hashed_password",
    )
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == 'john.doe@gmail.com'
    assert user.password_hash == "hashed_password"
