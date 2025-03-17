# Import future annotations for forward references
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db

# Import User only for type checking to avoid circular imports
if TYPE_CHECKING:
    from app.models import User, Project, Invoice


class Client(db.Model):
    '''Client model for the application'''

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=True)
    address: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=datetime.now(tz=timezone.utc))

    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user.id'), index=True)
    user: so.Mapped['User'] = so.relationship(back_populates='clients')

    projects: so.WriteOnlyMapped[list['Project']] = so.relationship(
        'Project', back_populates='client', cascade='all, delete-orphan')
    invoices: so.WriteOnlyMapped[list['Invoice']] = so.relationship(
        'Invoice', back_populates='client', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Client: {self.name}>'
