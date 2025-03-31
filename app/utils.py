from app.models import Client
from sqlalchemy.orm import Session
from flask_sqlalchemy import BaseQuery
from flask import Request


def get_client_by_name(client_name: str, session: Session):
    return session.query(Client).filter(Client.name == client_name).first()


def paginate_query(
    query: BaseQuery,
    request: Request,
    page: int | None = None,
    per_page: int | None = None,
    error_out: bool = True
) -> BaseQuery:
    """
    Paginates a SQLAlchemy query object based on request arguments or provided
    parameters.

    Args:
        query (BaseQuery): The SQLAlchemy query object to paginate.
        request (Request): The HTTP request object containing query parameters.
        page (int | None, optional): The page number to retrieve. Defaults to
            the "page" query parameter in the request or 1 if not provided.
        per_page (int | None, optional): The number of items per page. Defaults
            to the "per_page" query parameter in the request or 10 if not
            provided.
        error_out (bool, optional): Whether to raise an error if the page is
            out of range. Defaults to True.

    Returns:
        BaseQuery: The paginated query object.
    """
    page = page or request.args.get("page", default=1, type=int)
    per_page = per_page or request.args.get("per_page", default=10, type=int)
    return query.paginate(page=page, per_page=per_page, error_out=error_out)
