import os
import sqlite3
import logging

logging.basicConfig(level = logging.INFO,format='%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s')
logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self,db_path:str):
        try:
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
                logger.info(f"Created directory: {db_dir}")

            self.connection = sqlite3.connect(db_path)
            self.connection.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.connection.cursor()

            logger.info(f"connect to database: {db_path}")
        except sqlite3.Error as e:
            logger.exception(f"Failed to connect to database: {db_path}")


    def _execute_query(self,query:str)->None:
        try:
            self.cursor.execute(query)
            self.connection.commit()

            logger.debug(f"Executed query: {query}")

        except sqlite3.Error as e:
            logger.exception(f"SQl Error: {e} | Query: {query}")

    def delete_table(self,table_name:str) -> None:
        self._execute_query(f"DROP TABLE IF EXISTS {table_name}")

    
    def make_table(self,table_name:str, schema:str) -> None:
        self._execute_query(f"CREATE TABLE IF NOT EXISTS {table_name} {schema}")

    def list_tables(self) -> list:
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            self.cursor.execute(query)

            tables = [row[0] for row in self.cursor.fetchall()]

            logger.info(f"Tables Found: {tables}")

            return tables
        
        except sqlite3.Error as e:
            logger.exception(f"Could not retrieve tables: {e}")

            return []
        

    def describe_table(self,table_name:str):
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            cols = self.cursor.fetchall()

            if not cols:
                logger.warning(f"Table {table_name} not found or has no columns")
                return
            
            print(f"\n--- Structure of '{table_name}' ---")
            print(f"{'ID':<3} {'Name':<20} {'Type':<10} {'NotNUll':<8} {'PK':<3}")
            print("-" * 50)

            for col in cols:
                print(f"{col[0]:<3} {col[1]:<20} {col[2]:<10} {col[3]:<8} {col[5]:<3}")

            print("-" * 50 + "\n")
        except sqlite3.Error as e:
            logger.exception(f"Could not describe table: {table_name}")


    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        logger.info("Context Manager: Connection closed.")
