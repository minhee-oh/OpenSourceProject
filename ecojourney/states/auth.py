"""
사용자 인증 관련 State
"""

import reflex as rx
from typing import Optional
import sqlite3
import logging
import json
from pydantic import ValidationError
from .base import BaseState
from ..ai.services import auth_service
from ..schemas.user import UserCreate

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
    
    # Setter 메서드들 (명시적 정의)
    def set_login_student_id(self, value: str):
        self.login_student_id = value
    
    def set_login_password(self, value: str):
        self.login_password = value
    
    def set_signup_student_id(self, value: str):
        self.signup_student_id = value
    
    def set_signup_password(self, value: str):
        self.signup_password = value
    
    def set_signup_college(self, value: str):
        self.signup_college = value
    
    async def signup(self):
        """회원가입 처리"""
        self.auth_error_message = ""
        
        if not self.signup_student_id or not self.signup_password or not self.signup_college:
            self.auth_error_message = "모든 필드를 입력해주세요."
            return
        
        try:
            # 백엔드 Auth 서비스(bcrypt) 사용
            try:
                user_payload = UserCreate(
                    student_id=self.signup_student_id.strip(),
                    password=self.signup_password,
                    college=self.signup_college.strip(),
                )
            except ValidationError as ve:
                # 비밀번호 길이 등 입력 검증 메시지 노출
                self.auth_error_message = "비밀번호는 최소 6자 이상 입력해주세요."
                logger.warning(f"회원가입 검증 오류: {ve}")
                return
            try:
                auth_service.create_user(user_payload)
            except sqlite3.IntegrityError:
                self.auth_error_message = "이미 존재하는 학번입니다."
                return
            
            # 가입 후 사용자 정보 조회
            user_info = auth_service.get_user(user_payload.student_id)
            if not user_info:
                self.auth_error_message = "회원정보를 불러오지 못했습니다."
                return
            
            # 로그인 상태로 전환
            self.current_user_id = user_info.student_id
            self.current_user_college = user_info.college
            self.current_user_points = user_info.current_points
            self.is_logged_in = True
            
            # 클라이언트 로컬 스토리지에 로그인 정보 저장 (지원되는 경우)
            if hasattr(rx, "set_local_storage"):
                await rx.set_local_storage(
                    "auth_user",
                    {
                        "student_id": self.current_user_id,
                        "college": self.current_user_college,
                        "current_points": self.current_user_points,
                    },
                )
            
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
            # 입력값 정규화
            login_id = self.login_student_id.strip()
            login_pw = self.login_password
            
            # 백엔드 검증 (bcrypt)
            ok = auth_service.verify_user(login_id, login_pw)
            if not ok:
                self.auth_error_message = "학번 또는 비밀번호가 올바르지 않습니다."
                return
            
            # 사용자 정보 조회
            user = auth_service.get_user(login_id)
            if not user:
                self.auth_error_message = "존재하지 않는 학번입니다."
                return
            
            # 로그인 성공
            self.current_user_id = user.student_id
            self.current_user_college = user.college
            self.current_user_points = user.current_points
            self.is_logged_in = True
            
            # 클라이언트 로컬 스토리지에 로그인 정보 저장 (지원되는 경우)
            if hasattr(rx, "set_local_storage"):
                await rx.set_local_storage(
                    "auth_user",
                    {
                        "student_id": self.current_user_id,
                        "college": self.current_user_college,
                        "current_points": self.current_user_points,
                    },
                )
            
            # 폼 초기화
            self.login_student_id = ""
            self.login_password = ""
            
            # 저장된 오늘 날짜의 데이터 자동 불러오기 (CarbonState에 있으므로 조건부 호출)
            # load_saved_activities는 CarbonState에 정의되어 있음
            if hasattr(self, 'load_saved_activities'):
                try:
                    await self.load_saved_activities()
                except Exception as load_error:
                    logger.warning(f"저장된 데이터 불러오기 실패 (무시): {load_error}")
            
            logger.info(f"로그인 성공: {self.current_user_id}")
            return rx.redirect("/")
            
        except Exception as e:
            self.auth_error_message = f"로그인 실패: {str(e)}"
            logger.error(f"로그인 오류: {e}")
    
    async def logout(self):
        """로그아웃 처리"""
        if hasattr(rx, "remove_local_storage"):
            await rx.remove_local_storage("auth_user")
        self.current_user_id = None
        self.current_user_college = None
        self.current_user_points = 0
        self.is_logged_in = False
        self.all_activities = []
        return rx.redirect("/")

    async def hydrate_auth(self):
        """클라이언트 로컬 스토리지에서 로그인 정보 복원"""
        try:
            if not hasattr(rx, "get_local_storage"):
                return
            data = await rx.get_local_storage("auth_user")
            if not data:
                return
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except Exception:
                    data = None
            if isinstance(data, dict):
                self.current_user_id = data.get("student_id")
                self.current_user_college = data.get("college")
                self.current_user_points = data.get("current_points") or 0
                self.is_logged_in = bool(self.current_user_id)
        except Exception as e:
            logger.warning(f"로그인 정보 복원 실패: {e}")



