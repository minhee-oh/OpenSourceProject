"""
사용자 인증 관련 State
"""

import reflex as rx
from typing import Optional
from datetime import datetime
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

    # 쿠키를 사용한 세션 저장 (Reflex 내장 기능)
    _session_user_id: str = rx.Cookie("")

    def _save_session_to_storage(self):
        """로그인 세션을 브라우저 localStorage 및 쿠키에 저장"""
        # 쿠키에 user_id 저장 (Reflex 방식)
        self._session_user_id = self.current_user_id or ""

        # localStorage에도 저장 (호환성을 위해)
        yield rx.call_script(
            f"""
            localStorage.setItem('eco_user_id', '{self.current_user_id}');
            localStorage.setItem('eco_user_college', '{self.current_user_college}');
            localStorage.setItem('eco_user_points', '{self.current_user_points}');
            localStorage.setItem('eco_is_logged_in', 'true');
            """
        )

    def _clear_session_storage(self):
        """localStorage 및 쿠키에서 세션 정보 삭제"""
        # 쿠키 삭제
        self._session_user_id = ""

        # localStorage 삭제
        yield rx.call_script(
            """
            localStorage.removeItem('eco_user_id');
            localStorage.removeItem('eco_user_college');
            localStorage.removeItem('eco_user_points');
            localStorage.removeItem('eco_is_logged_in');
            """
        )

    def check_and_restore_session(self):
        """
        페이지 로드 시 쿠키에서 세션을 확인하고 복원
        """
        # 이미 로그인되어 있으면 복원할 필요 없음
        if self.is_logged_in:
            return

        # 쿠키에서 user_id 확인
        user_id = self._session_user_id

        if not user_id or user_id == "":
            return

        try:
            # auth_service를 사용하여 사용자 존재 여부 확인
            from ..ai.services.auth_service import get_user

            user = get_user(user_id)
            if not user:
                # 사용자가 존재하지 않으면 세션 삭제
                yield from self._clear_session_storage()
                return

            # 세션 복원
            self.current_user_id = user.student_id
            self.current_user_college = user.college
            self.current_user_points = user.current_points
            self.is_logged_in = True

        except Exception as e:
            logger.error(f"세션 복원 오류: {e}", exc_info=True)
            yield from self._clear_session_storage()
    
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
    
    def _hash_password(self, password: str) -> str:
        """비밀번호를 해시화합니다."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def signup(self):
        """회원가입 처리 (auth_service 사용 - FastAPI와 통합)"""
        self.auth_error_message = ""

        if not self.signup_student_id or not self.signup_password or not self.signup_college:
            self.auth_error_message = "모든 필드를 입력해주세요."
            return

        try:
            # auth_service를 사용하여 회원가입 (FastAPI와 동일한 로직 사용)
            from ..ai.services.auth_service import create_user, get_user
            from ..schemas.user import UserCreate
            from pydantic import ValidationError
            import sqlite3

            # 먼저 중복 체크 (DB 조회)
            existing_user = get_user(self.signup_student_id)
            if existing_user:
                self.auth_error_message = "이미 존재하는 학번입니다."
                logger.warning(f"회원가입 실패 - 중복 학번: {self.signup_student_id}")
                return

            # UserCreate 스키마로 변환 (Pydantic 검증)
            try:
                user_data = UserCreate(
                    student_id=self.signup_student_id,
                    password=self.signup_password,
                    college=self.signup_college
                )
            except ValidationError as ve:
                # Pydantic 검증 오류를 사용자 친화적인 메시지로 변환
                for error in ve.errors():
                    if error['loc'] == ('password',) and 'string_too_short' in str(error['type']):
                        self.auth_error_message = "비밀번호는 최소 6자 이상이어야 합니다."
                        return
                # 기타 검증 오류
                self.auth_error_message = "입력 정보가 올바르지 않습니다."
                logger.warning(f"회원가입 실패 - 검증 오류: {ve}")
                return

            # 사용자 생성 (auth_service 사용)
            try:
                create_user(user_data)
            except sqlite3.IntegrityError:
                self.auth_error_message = "이미 존재하는 학번입니다."
                logger.warning(f"회원가입 실패 - IntegrityError: {self.signup_student_id}")
                return
            except Exception as create_error:
                logger.error(f"사용자 생성 오류: {create_error}", exc_info=True)
                self.auth_error_message = f"회원가입 실패: {str(create_error)}"
                return

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

            # 세션 저장
            yield from self._save_session_to_storage()

            return rx.redirect("/")

        except Exception as e:
            self.auth_error_message = f"회원가입 실패: {str(e)}"
            logger.error(f"회원가입 오류: {e}", exc_info=True)
    
    def login(self):
        """로그인 처리 (auth_service 사용 - FastAPI와 통합)"""
        self.auth_error_message = ""

        if not self.login_student_id or not self.login_password:
            self.auth_error_message = "학번과 비밀번호를 입력해주세요."
            return

        try:
            # auth_service를 사용하여 로그인 검증 (FastAPI와 동일한 로직)
            from ..ai.services.auth_service import verify_user, get_user

            # 비밀번호 검증
            is_valid = verify_user(self.login_student_id, self.login_password)
            if not is_valid:
                self.auth_error_message = "학번 또는 비밀번호가 올바르지 않습니다."
                logger.warning(f"로그인 실패 - 잘못된 인증 정보: {self.login_student_id}")
                return

            # 사용자 정보 조회
            user = get_user(self.login_student_id)
            if not user:
                self.auth_error_message = "존재하지 않는 사용자입니다."
                logger.error(f"로그인 실패 - 사용자 없음: {self.login_student_id}")
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

            # 세션 저장
            yield from self._save_session_to_storage()

            return rx.redirect("/")

        except Exception as e:
            self.auth_error_message = f"로그인 실패: {str(e)}"
            logger.error(f"로그인 오류: {e}", exc_info=True)
    
    def logout(self):
        """로그아웃 처리"""
        logger.info(f"[로그아웃] 사용자: {self.current_user_id}")

        self.current_user_id = None
        self.current_user_college = None
        self.current_user_points = 0
        self.is_logged_in = False
        self.all_activities = []

        # 세션 스토리지 삭제
        yield from self._clear_session_storage()

        return rx.redirect("/")



