import os


class ConfigNotKnownError(Exception):
    pass


class Configuration:

    @classmethod
    def load(cls):
        # load based on env vars
        for key in cls.__conf.keys():
            if os.environ.get(key):
                cls.__conf[key] = os.environ[key]

    __conf = {
        "pg_server": "postgres-postgresql.challenge.svc.cluster.local.",
        "pg_port": 5432,
        "pg_password": "password",
        "pg_username": "postgres",
        "pg_dbname": "postgres",
        "minio_username": "admin",
        "minio_password": "password",
        "minio_server": "http://minio.challenge.svc.cluster.local:9000",
        "minio_bucket": "backups"
    }

    def __getattr__(self, item):
        if self.__conf.get(item):
            return self.__conf[item]
        else:
            raise ConfigNotKnownError
