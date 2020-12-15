from sqlalchemy import text

from src.main import db


class Admin(db.Model):
    def dump_database(cls):
        sql_query = text("SELECT *")
        return db.engine.execute(sql_query)
