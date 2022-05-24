from app.main.model.pagila import TableList, WholeTableBackup
from app.main.service.minio import MinioService


class PagilaService:

    def get_tables(self):
        tables = TableList().get()
        return tables

    def backup_whole_table(self, table_name):
        minio_service = MinioService()
        wtb = WholeTableBackup()
        backup = wtb.get(table_name)
        backup_script = self._generate_sql_script(table_name, backup.columns, backup.records)
        minio_service.put_backup(backup_script, table_name + ".sql")
        return

    def _generate_sql_script(self, table_name, columns, records):
        # generate schema
        script = "CREATE TABLE IF NOT EXISTS " + table_name + " (\n"
        for column in columns:
            script += "  " + column[0] + " " + column[1] + ",\n"
        script += ");\n"
        script += "COPY public." + table_name + " (" + columns[0][0]
        for column in columns[1:]:
            script += ", " + column[0]
        script += ") FROM stdin;\n"
        for record in records:
            script += "\t".join(record) + "\n"
        script += "\\.\n"
        return script