from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseService:
    def __init__(self, db_url=None):
        """
        Initializes the DatabaseService with a specified or default database URL.

        Supported database URLs:
        - SQLite: sqlite:///path/to/your/database.db
        - MySQL: mysql://username:password@hostname/database_name
        - PostgreSQL: postgresql://username:password@hostname/database_name
        - Oracle: oracle://username:password@hostname:port/database_name
        - SQL Server: mssql+pyodbc://username:password@hostname/database_name
        """

        # Define the connection URL
        if db_url:
            self.db_url = db_url
        else:
            self.db_url = "postgresql://postgres:123456@localhost:5432/iot_db"

        # Create the SQLAlchemy engine
        self.engine = create_engine(self.db_url)

        # Create a sessionmaker that will be used to create sessions
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
