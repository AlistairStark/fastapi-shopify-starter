from sqlalchemy.orm.scoping import ScopedSession

from app.models.database import get_session


class DBService:
    def __init__(self):
        self.session: ScopedSession = get_session()
