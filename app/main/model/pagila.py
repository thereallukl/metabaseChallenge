from typing import Dict

import psycopg2.extras

from app.main.db import DBConnection


class TableListDto:
    tables: Dict

    def __init__(self):
        self.tables = []


class TableList:

    def get(self):
        tl_dto = TableListDto()
        self._get_table_list(tl_dto)
        return tl_dto

    def _get_table_list(self, tl_dto):
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        select table_name, pg_relation_size('"'||table_schema||'"."'||table_name||'"')
        from information_schema.tables
        where table_schema = 'public'
        order by pg_relation_size desc;
        """
        )
        results = cursor.fetchall()
        cursor.close()
        DBConnection.release_connection(connection)
        for r in results:
            tl_dto.tables.append(r[0])


class WholeTableBackupDto:
    records: Dict
    columns: Dict

    def __init__(self):
        self.records = []
        self.columns = []


class WholeTableBackup:

    def get(self, table_name):
        wtb_dto = WholeTableBackupDto()
        self._get_schema(table_name, wtb_dto)
        self._get_whole_table(table_name, wtb_dto)
        return wtb_dto

    def _get_schema(self, table_name, wtb_dto):
        connection = DBConnection.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # get schema
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema ='public' AND table_name = '" + table_name + "'")
        columns_iter = cursor.fetchall()
        cursor.close()
        DBConnection.release_connection(connection)
        for c in columns_iter:
            wtb_dto.columns.append(c)

    # evaluate using cursor.copy()
    def _get_whole_table(self, table_name, wtb_dto):
        connection = DBConnection.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM " + table_name)
        records_iter = cursor.fetchall()
        cursor.close()
        DBConnection.release_connection(connection)
        for r in records_iter:
            wtb_dto.records.append([str(x) for x in r])
