from services import unit_of_work
from sqlalchemy import text

def get_bookmarks(uow: unit_of_work):
    with uow:
        rows = uow.session.execute(
            text("""
            SELECT * from bookmarks
            """)
        ).fetchall()
    return [dict(row._asdict()) for row in rows]

def get_bookmarks_sorted(sort_column: str, uow: unit_of_work):
    with uow:
        rows = uow.session.execute(
            text(f"""
            SELECT * from bookmarks ORDER BY {sort_column}
            """)
        ).fetchall()
    return [dict(row._asdict()) for row in rows]

def get_bookmark_by_id(id: str, uow: unit_of_work):
    with uow:
        row = uow.session.execute(
            text(f"""
            SELECT * from bookmarks WHERE id = {id}
            """)
        ).fetchone()
    return row._asdict()