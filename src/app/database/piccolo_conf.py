import os
from dotenv import load_dotenv
from piccolo.engine.sqlite import SQLiteEngine

load_dotenv()

DB_PATH = os.getenv("DB_PATH")

if DB_PATH is None:
    raise ValueError("DB_PATH not set!")

DB = SQLiteEngine(path=DB_PATH)
