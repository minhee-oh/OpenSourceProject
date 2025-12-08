from pathlib import Path
import sqlite3

# backend/ 폴더 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# DB 파일 이름 (원하는 대로 바꿔도 됨)
DB_PATH = BASE_DIR / "eco_journey.db"


def get_connection():
    """SQLite 연결을 만들어서 반환"""
    conn = sqlite3.connect(DB_PATH)
    # row["student_id"] 이런 식으로 쓰려고
    conn.row_factory = sqlite3.Row
    return conn
