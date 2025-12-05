"""
사용자 인증 관련 State
"""

import reflex as rx
from typing import Optional
import hashlib
import logging
from .base import BaseState
from ..models import User

logger = logging.getLogger(__name__)


class AuthState(BaseState):
    """
    사용자 인증 관련 상태 및 로직
    """
    # 사용자 인증 관련 상태
    current_user_id: Optional[str] = None
    current_user_college: Optional[str] = None
    current_user_points: int = 0
    is_logged_in: bool = False
    
    # 로그인/회원가입 폼 상태
    login_student_id: str = ""
    login_password: str = ""
    signup_student_id: str = ""
    signup_password: str = ""
    signup_college: str = ""
    auth_error_message: str = ""
    
    def _hash_password(self, password: str) -> str:
        """비밀번호를 해시화합니다."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    async def signup(self):
        """회원가입 처리"""
        self.auth_error_message = ""
        
        if not self.signup_student_id or not self.signup_password or not self.signup_college:
            self.auth_error_message = "모든 필드를 입력해주세요."
            return
        
        try:
            # 기존 사용자 확인
            existing_user = await User.find_by_id(self.signup_student_id)
            if existing_user:
                self.auth_error_message = "이미 존재하는 학번입니다."
                return
            
            # 새 사용자 생성
            hashed_password = self._hash_password(self.signup_password)
            new_user = User(
                student_id=self.signup_student_id,
                password=hashed_password,
                college=self.signup_college,
                current_points=0,
                avatar_status="NORMAL"
            )
            await new_user.save()
            
            # 로그인 상태로 전환
            self.current_user_id = self.signup_student_id
            self.current_user_college = self.signup_college
            self.current_user_points = 0
            self.is_logged_in = True
            
            # 폼 초기화
            self.signup_student_id = ""
            self.signup_password = ""
            self.signup_college = ""
            
            logger.info(f"회원가입 성공: {self.current_user_id}")
            return rx.redirect("/")
            
        except Exception as e:
            self.auth_error_message = f"회원가입 실패: {str(e)}"
            logger.error(f"회원가입 오류: {e}")
    
    async def login(self):
        """로그인 처리"""
        self.auth_error_message = ""
        
        if not self.login_student_id or not self.login_password:
            self.auth_error_message = "학번과 비밀번호를 입력해주세요."
            return
        
        try:
            # 사용자 조회
            user = await User.find_by_id(self.login_student_id)
            if not user:
                self.auth_error_message = "존재하지 않는 학번입니다."
                return
            
            # 비밀번호 확인
            hashed_password = self._hash_password(self.login_password)
            if user.password != hashed_password:
                self.auth_error_message = "비밀번호가 일치하지 않습니다."
                return
            
            # 로그인 성공
            self.current_user_id = user.student_id
            self.current_user_college = user.college
            self.current_user_points = user.current_points
            self.is_logged_in = True
            
            # 폼 초기화
            self.login_student_id = ""
            self.login_password = ""
            
            logger.info(f"로그인 성공: {self.current_user_id}")
            return rx.redirect("/")
            
        except Exception as e:
            self.auth_error_message = f"로그인 실패: {str(e)}"
            logger.error(f"로그인 오류: {e}")
    
    async def logout(self):
        """로그아웃 처리"""
        self.current_user_id = None
        self.current_user_college = None
        self.current_user_points = 0
        self.is_logged_in = False
        self.all_activities = []
        return rx.redirect("/")


