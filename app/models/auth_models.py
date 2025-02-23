from __future__ import annotations
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Client


class User(UserMixin, db.Model):
    '''User model for the application'''

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(
        sa.String(256), nullable=False)

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=datetime.now(tz=timezone.utc))

    # WriteOnlyMapped prevents unnecessary large queries when accessing
    # clients.
    clients: so.WriteOnlyMapped[list['Client']] = so.relationship(
        'Client', back_populates='user')

    def __repr__(self) -> str:
        return f'<User {self.name}>'

    def set_password(self, password: str) -> None:
        '''Set the password hash for the user'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        '''Check the password hash for the user'''
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id: int) -> User:
    '''Load a user from the database'''
    return db.session.get(User, int(id))
