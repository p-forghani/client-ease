from app.models import Client
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query
from flask import Request
from sqlalchemy import or_


def get_client_by_name(client_name: str, session: Session):
    return session.query(Client).filter(Client.name == client_name).first()


def paginate_query(
    query,
    request: Request,
    page: int | None = None,
    per_page: int | None = None,
    error_out: bool = True
):
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


def search_in_query(
    query: Query,
    request: Request,
    fields: tuple[str] | list[str] | set[str],
) -> Query:
    """
    Filters a SQLAlchemy query object based on a search parameter in the
    request.

    Args:
        query (Query): The SQLAlchemy query object to filter.
        request (Request): The HTTP request object containing query parameters.
        fields (Iterable): An iterable of SQLAlchemy column objects to filter
        on (e.g., Client.name, Client.email).

    Returns:
        Query: The filtered query object.
    """
    search_query = request.args.get('search')
    if search_query:
        filters = [field.ilike(f'%{search_query}%') for field in fields]
        if filters:
            query = query.filter(or_(*filters))
    return query


def apply_filters_to_query(query, model, filters):
    """
    Dynamically applies filters to a SQLAlchemy query.

    Args:
        query (Query): The base SQLAlchemy query.
        model (Model): The SQLAlchemy model being queried.
        filters (dict): A dictionary of filters to apply.

    Returns:
        Query: The filtered query.
    """
    if 'status' in filters and filters['status']:
        query = query.filter(model.status == filters['status'])
    if 'date' in filters and filters['date']:
        query = query.filter(model.date == filters['date'])
    if 'project_id' in filters and filters['project_id']:
        query = query.filter(model.project_id == filters['project_id'])
    return query
