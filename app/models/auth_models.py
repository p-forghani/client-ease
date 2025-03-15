from __future__ import annotations
from datetime import datetime, timezone
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models import Client


class User(UserMixin, db.Model):
    '''User model for the application'''
    __name__ = 'user'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(
        sa.String(256), nullable=False)
    email_verified: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, default=False)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=datetime.now(tz=timezone.utc))

    role_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('role.id', name='fk_user_role'), index=True, default=2)

    # WriteOnlyMapped prevents unnecessary large queries when accessing
    # clients.
    clients: so.WriteOnlyMapped[list['Client']] = so.relationship(
        'Client', back_populates='user')

    def __repr__(self) -> str:
        return f'<{self.first_name} {self.last_name}>'

    def set_password(self, password: str) -> None:
        '''Set the password hash for the user'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        '''Check the password hash for the user'''
        return check_password_hash(self.password_hash, password)

    def generate_token(self, token_type) -> str:
        """
        Generate a token for the user based on the token type.

        Args:
            token_type (str): The type of token to generate. Acceptable values:
                'reset_password': For generating a password reset token.
                'verify_email': For generating an email verification
                token.
                (add any other token types here as needed).

        Returns:
            str: The generated token.
        """

        # Validate token_type value
        if token_type not in current_app.config["SALTS"]:
            raise ValueError(
                f"Invalid token type: {token_type}. "
                f"Expected one of {list(current_app.config['SALTS'].keys())}"
            )
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(
            self.email, salt=current_app.config["SALTS"][token_type])

    @staticmethod
    def verify_token(token: str, token_type) -> User:
        """
        Verify a token and return the associated User.
        Args:
            token (str): The token to verify.
            token_type (str): The type of the token. Acceptable values are
                'verify_email', 'reset_password', etc.
        Returns:
            User: The user associated with the token if verification is
                successful, otherwise None.
        Raises:
            Exception: If there is an error during token verification.
        """

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token, salt=current_app.config['SALTS'][token_type],
                max_age=86400)
        except Exception as e:
            current_app.logger.exception(
                f'Error verifying {token_type} token: {e}')
            return None
        return db.session.scalar(
            sa.select(User).where(User.email == email))


@login.user_loader
def load_user(id: int) -> User:
    '''Load a user from the database'''
    return db.session.get(User, int(id))


class Role(db.Model):
    '''Role model for the application'''
    __name__ = 'role'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True
    )
    description: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(255), nullable=True
    )
