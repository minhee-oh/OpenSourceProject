import sqlite3
from fastapi import APIRouter, HTTPException, status

from ecojourney.schemas.user import UserCreate, UserLogin, User
from ecojourney.ai.services.auth_service import (
    create_user,
    verify_user,
    get_user,  # 👈 이렇게 그냥 get_user로 가져오자
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    """
    회원가입 엔드포인트
    """
    try:
        create_user(user)
    except sqlite3.IntegrityError:
        # PK(student_id) 중복
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 학번입니다.",
        )
    return {"message": "회원가입이 완료되었습니다.", "student_id": user.student_id}


@router.post("/login")
def login(body: UserLogin):
    ok = verify_user(body.student_id, body.password, body.college)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="학번, 비밀번호 또는 단과대 정보가 올바르지 않습니다.",
        )

    return {"message": "로그인 성공", "student_id": body.student_id, "college": body.college}



@router.get("/users/{student_id}", response_model=User)
def get_user_info(student_id: str):
    """
    유저 정보 조회 (디버깅/관리자용)
    """
    user = get_user(student_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자입니다.",
        )
    return user
