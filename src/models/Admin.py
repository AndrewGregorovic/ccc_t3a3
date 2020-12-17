import gzip

from sh import pg_dump

from src.main import db


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    def dump_database():
        """
        Method to dump the database contents to a file using pg_dump

        Returns:
        String with message on whether or not the dump was successful
        """

        try:
            with gzip.open("database_dump.gz", "wb") as f:
                pg_dump("-h", "localhost", "-U", "t3a3", "t3a3", _out=f)
        except Exception:
            return "An error occurred and the database was unable to be dumped"

        return "Database dumped to file 'database_dump.gz'"
