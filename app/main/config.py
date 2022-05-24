class ConfigNotKnownError(Exception):
    pass


class Configuration:
    def load(self):
        # load based on env vars
        pass

    __conf = {
        "pg_server": "postgres-postgresql.challenge.svc.cluster.local.",
        "pg_port": 5432,
        "pg_password": "DiWqht9aSe",
        "pg_username": "postgres",
        "pg_dbname": "pagila",
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
