import os
from dotenv import load_dotenv

load_dotenv()

mongo_user = os.getenv("mongo_user")
mongo_password = os.getenv("mongo_password")
mongo_closter = os.getenv("mongo_closter")
mongo_db = os.getenv("mongo_db")
mongo_colection = os.getenv("mongo_colection")

mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_closter}/{mongo_db}"