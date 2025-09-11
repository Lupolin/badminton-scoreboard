# app/config.py
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

def _build_mysql_url():
    host=os.getenv("RDS_HOST",""); user=os.getenv("RDS_USER","")
    pwd=os.getenv("RDS_PASSWORD",""); db=os.getenv("RDS_DATABASE",""); port=os.getenv("RDS_PORT","3306")
    if not (host and user and pwd and db): return ""
    return f"mysql+pymysql://{user}:{quote_plus(pwd)}@{host}:{port}/{db}?charset=utf8mb4"

def load_config():
    default_players = os.getenv(
        "DEFAULT_PLAYERS",
        "Judy, Jesha, Lucas, Doris, Iris, Luna, Mars, Solomon"
    )
    return {
        "FLASK_SECRET": os.getenv("SECRET_KEY","dev-secret"),
        "MYSQL_URL": _build_mysql_url(),
        "APP_TIMEZONE": os.getenv("APP_TIMEZONE","Asia/Taipei"),
        "DEFAULT_PLAYERS": [s.strip() for s in default_players.split(",") if s.strip()],
    }
