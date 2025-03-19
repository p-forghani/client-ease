from app.models import Client
from sqlalchemy.orm import Session


def get_client_by_name(client_name: str, session: Session):
    return session.query(Client).filter(Client.name == client_name).first()
