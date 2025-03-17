from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime
from typing import TYPE_CHECKING

# Import Client for type annotations only
if TYPE_CHECKING:
    from app.models import Client, User, Invoice


class Project(db.Model):
    """Project model for the app"""

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(
        sa.String(100), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    start_date: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, nullable=False)
    end_date: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, nullable=True)
    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('client.id'), index=True)
    client: so.Mapped['Client'] = so.relationship(
        'Client', back_populates='projects')
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user.id'), index=True)
    user: so.Mapped['User'] = so.relationship(
        'User', back_populates='projects')
    invoices: so.Mapped[list['Invoice']] = so.relationship(
        'Invoice', back_populates='project', cascade='all, delete-orphan')
    # TODO: Add extra information such as hourly or fix price etc.
