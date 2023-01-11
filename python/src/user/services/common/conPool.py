import os
from mysql.connector import pooling



dbconfig = {
    "user": os.environ.get("MYSQL_HOST"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DB"),
    "host": os.environ.get("MYSQL_HOST")
}

dbconfig = {
    "user": "kieran",
    "password": "root",
    "database": "XT",
    "host": "localhost"
}

class WritePool:

    def __init__(self):

        self.cnx = pooling.MySQLConnectionPool(
            pool_name="writePool",
            pool_size=5,
            pool_reset_session=True,
            **dbconfig
        )

    def getConn(self):

        return self.cnx.get_connection()

    def commit(self, conn):

        if conn.is_connected():
            conn.commit()

    def rollback(self, conn):

        if conn.is_connected():
            conn.rollback()

    def closeConn(self, conn):

        if conn.is_connected():
            conn.close()
    