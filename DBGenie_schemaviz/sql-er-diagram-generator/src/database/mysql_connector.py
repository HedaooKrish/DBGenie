import mysql.connector
from typing import List, Dict, Tuple
from mysql.connector import Error

class MySQLConnector:
    def __init__(self, host: str = "localhost", user: str = "root", password: str = ""):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def get_databases(self) -> List[str]:
        if not self.connection:
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        cursor.close()
        return databases

    def use_database(self, database_name: str) -> bool:
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"USE {database_name}")
            cursor.close()
            return True
        except Error as e:
            print(f"Error using database {database_name}: {e}")
            return False

    def get_tables(self) -> List[str]:
        if not self.connection:
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables

    def get_table_columns(self, table_name: str) -> List[Dict]:
        if not self.connection:
            return []
        
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = []
        for column in cursor.fetchall():
            columns.append({
                'name': column[0],
                'type': column[1],
                'is_nullable': column[2],
                'key': column[3],
                'default': column[4],
                'extra': column[5]
            })
        cursor.close()
        return columns

    def get_foreign_keys(self, table_name: str) -> List[Dict]:
        if not self.connection:
            return []
        
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT 
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM
                information_schema.KEY_COLUMN_USAGE
            WHERE
                TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = '{table_name}'
                AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        
        foreign_keys = []
        for fk in cursor.fetchall():
            foreign_keys.append({
                'column': fk[0],
                'referenced_table': fk[1],
                'referenced_column': fk[2]
            })
        cursor.close()
        return foreign_keys

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None 