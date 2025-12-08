from typing import Optional
import sqlite3
import bcrypt

from ecojourney.db import get_connection
from ecojourney.schemas.user import UserCreate, User


# ==========================
# 내부용: student_id로 row 가져오기
# ==========================
def _get_user_row(student_id: str) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE student_id = ?",
        (student_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row


# ==========================
# 회원가입
# ==========================
def create_user(user: UserCreate) -> None:
    """
    - 평문 비밀번호 → bcrypt 해시
    - users 테이블에 INSERT
    """
    conn = get_connection()
    cur = conn.cursor()

    # 비밀번호 해시 생성
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    hashed_str = hashed.decode("utf-8")

    try:
        cur.execute(
            """
            INSERT INTO users (student_id, password_hash, college)
            VALUES (?, ?, ?)
            """,
            (user.student_id, hashed_str, user.college),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        # PK(student_id) 중복 같은 에러는 위로 올려서 처리하게 둠
        raise e
    finally:
        conn.close()


# ==========================
# 로그인 검증
# ==========================
def verify_user(student_id: str, password: str, college: str) -> bool:
    """
    - student_id로 DB에서 사용자 찾고
    - 단과대(college)도 일치하는지 확인
    - bcrypt로 비밀번호 일치 여부까지 확인
    """
    row = _get_user_row(student_id)
    if row is None:
        return False

    # 1) 단과대 먼저 체크
    if row["college"] != college:
        return False

    # 2) 비밀번호 해시 체크
    stored_hash = row["password_hash"]
    if stored_hash is None:
        return False

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash.encode("utf-8"),
    )



# ==========================
# 유저 정보 조회 (응답용 User 모델)
# ==========================
def get_user(student_id: str) -> Optional[User]:
    row = _get_user_row(student_id)
    if row is None:
        return None

    # Pydantic이 created_at을 datetime으로 파싱해 줄 거라 그냥 넘겨도 됨
    return User(
        student_id=row["student_id"],
        college=row["college"],
        current_points=row["current_points"],
        created_at=row["created_at"],
    )
