from pydantic import BaseModel, Field
from datetime import datetime


# ==========================
# 공통 필드 베이스
# ==========================
class UserBase(BaseModel):
    student_id: str = Field(..., description="학번 (로그인 ID)")
    college: str = Field(..., description="소속 단과대")
    current_points: int = Field(0, description="현재 보유 포인트")


# ==========================
# 회원가입 요청 바디
# ==========================
class UserCreate(BaseModel):
    student_id: str = Field(..., description="학번 (로그인 ID)")
    password: str = Field(..., min_length=6, description="평문 비밀번호 (입력용)")
    college: str = Field(..., description="소속 단과대 (예: 공과대학, 경영대학)")



# ==========================
# 로그인 요청 바디
# ==========================
class UserLogin(BaseModel):
    student_id: str = Field(..., description="학번 (로그인 ID)")
    password: str = Field(..., min_length=6, description="평문 비밀번호")
    college: str = Field(..., description="소속 단과대 (예: 공과대학, 경영대학)")


# ==========================
# 유저 정보 응답용
# ==========================
class User(UserBase):
    created_at: datetime = Field(..., description="가입일")

    class Config:
        # Pydantic v1/v2 모두 호환되게
        orm_mode = True
