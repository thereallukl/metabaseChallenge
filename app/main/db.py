import psycopg2
from psycopg2 import pool
from app.main.config import Configuration


class DBConnection:
    pool = None

    @classmethod
    def init_pool(cls):
        config = Configuration()
        cls.pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                      user=config.pg_username,
                                                      password=config.pg_password,
                                                      host=config.pg_server,
                                                      database=config.pg_dbname,
                                                      port=config.pg_port)

    @classmethod
    def get_connection(cls):
        if not cls.pool:
            cls.init_pool()
        try:
            conn = cls.pool.getconn()
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to get connection to PG", error)

    @classmethod
    def release_connection(cls, conn):
        if not cls.pool:
            return
        try:
            cls.pool.putconn(conn)
        except Exception as error:
            print("Failed to release connection", error)
