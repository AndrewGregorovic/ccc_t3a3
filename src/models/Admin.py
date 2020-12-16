from sqlalchemy import text

from src.main import db


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    def dump_database(cls):
        sql_query = text("SELECT *")
        return db.engine.execute(sql_query)
