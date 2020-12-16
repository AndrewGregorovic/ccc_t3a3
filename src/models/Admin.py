from sqlalchemy import text

from src.main import db


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    def dump_database(cls):
        """
        Class method to execute an sql query to dump the database contents

        Returns:
        The database contents retrieved by the query
        """

        sql_query = text("SELECT *")
        return db.engine.execute(sql_query)
