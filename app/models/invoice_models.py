from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db

if TYPE_CHECKING:
    from app.models import Client, Project, User


class InvoiceStatus(Enum):
    PENDING = 'pending'
    PAID = 'paid'
    OVERDUE = 'overdue'
    CANCELLED = 'cancelled'


class Invoice(db.Model):
    """Invoice model for the app"""

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    invoice_number: so.Mapped[str] = so.mapped_column(
        sa.String(50), unique=True, nullable=False)
    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('client.id'), nullable=False)
    project_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('project.id'), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user.id'), nullable=False)
    issue_date: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, nullable=False, default=datetime.now(timezone.utc))
    due_date: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, nullable=False)
    total_amount: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    # TODO: Add the partially paid status
    status: so.Mapped[InvoiceStatus] = so.mapped_column(
        sa.Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.PENDING)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, nullable=False, default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc))

    client: so.Mapped['Client'] = so.relationship(
        'Client', back_populates='invoices')
    project: so.Mapped['Project'] = so.relationship(
        'Project', back_populates='invoices')
    user: so.Mapped['User'] = so.relationship(
        'User', back_populates='invoices')
