from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime
from typing import TYPE_CHECKING

# Import Client for type annotations only
if TYPE_CHECKING:
    from app.models import Client, User, Invoice


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
    # TODO: Add extra information such as hourly or fix price etc.
