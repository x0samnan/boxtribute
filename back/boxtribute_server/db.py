from peewee import MySQLDatabase
from playhouse.flask_utils import FlaskDB

db = FlaskDB()


def create_db_interface(**mysql_kwargs):
    """Create MySQL database interface using given connection parameters. `mysql_kwargs`
    are forwarded to `pymysql.connect`.
    """
    return MySQLDatabase(**mysql_kwargs)
