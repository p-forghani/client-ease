import click
from flask.cli import with_appcontext
from app import db
from app.models import Role

@click.command("seed-db")
@with_appcontext
def seed_db():
    """Seed the database with initial data."""
    roles = [
        {"id": 1, "name": "Admin", "description": "Admin role"},
        {"id": 2, "name": "User", "description": "User role"},
        {"id": 3, "name": "Customer", "description": "Customer role"}]

    for role in roles:
        if not Role.query.filter_by(name=role["name"]).first():
            db.session.add(
                Role(
                    id=role["id"],
                    name=role["name"],
                    description=role["description"]
                )
            )


    db.session.commit()
    click.echo("✅ Database roles seeded successfully!")
