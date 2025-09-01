from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

# Import Client for type annotations only
if TYPE_CHECKING:
    from app.models import Client, User


class Project(db.Model):
    """
    Represents a project in the application.
    Attributes:
        title (str): The title of the project, with a maximum length of 100
        characters.
        description (str, optional): A detailed description of the project.
        start_date (datetime): The start date and time of the project.
        end_date (datetime, optional): The end date and time of the project.
        client_id (int): The unique identifier of the client associated with
        the project.
        user_id (int): The unique identifier of the user associated with the
        project.
    """

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
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user.id'), index=True)
    client: so.Mapped['Client'] = so.relationship(
        'Client', back_populates='projects')
    user: so.Mapped['User'] = so.relationship(
        'User', back_populates='projects')
    invoices: so.Mapped[list['Invoice']] = so.relationship(
        'Invoice', back_populates='project', cascade='all, delete-orphan')
    # FUTURE: Add extra information such as hourly or fix price etc.


class InvoiceStatus(Enum):
    pending = 'pending'
    paid = 'paid'
    overdue = 'overdue'
    cancelled = 'cancelled'


class Invoice(db.Model):
    """
    Represents an invoice in the application.

    Attributes:
        id (int): The unique identifier of the invoice.
        title (str): The title of the invoice.
        description (str, optional): A detailed description of the invoice.
        amount (float): The amount of the invoice.
        issue_date (datetime): The issue date and time of the invoice.
        due_date (datetime): The due date and time of the invoice.
        project_id (int): The unique identifier of the project associated with
        the invoice.
        client_id (int): The unique identifier of the client associated with
        the invoice.
        user_id (int): The unique identifier of the user associated with the
        invoice.
        status (InvoiceStatus): The status of the invoice (pending, paid,
        overdue, cancelled).
        project (Project): The project associated with the invoice.
        client (Client): The client associated with the invoice.
        user (User): The user associated with the invoice.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    amount: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    status: so.Mapped[InvoiceStatus] = so.mapped_column(
        sa.Enum(InvoiceStatus),
        nullable=False,
        default=InvoiceStatus.pending.value
    )

    project_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('project.id'), index=True)
    project: so.Mapped[Project] = so.relationship(
        'Project', back_populates='invoices')
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user.id'), index=True)
    user = so.relationship('User', back_populates='invoices')
    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('client.id'), index=True)
    client: so.Mapped['Client'] = so.relationship(
        'Client', back_populates='invoices')
