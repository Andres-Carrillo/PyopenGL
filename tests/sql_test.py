import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.manager import DBManager
with DBManager("data/monsters.db") as db:
    

    all_tables = db.list_tables()

    for table in all_tables:
        db.describe_table(table)
