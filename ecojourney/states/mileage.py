"""
마일리지 환산 관련 State
"""

import reflex as rx
from typing import List, Dict, Any
import logging
from .battle import BattleState
from ..models import MileageRequest, User

logger = logging.getLogger(__name__)


class MileageState(BattleState):
    """
    마일리지 환산 관련 상태 및 로직
    """
    mileage_request_points: int = 0
    mileage_error_message: str = ""

    def set_mileage_points(self, value: str):
        """입력된 포인트 값을 정수로 변환하여 설정"""
        try:
            self.mileage_request_points = int(value) if value else 0
        except ValueError:
            self.mileage_request_points = 0

    async def request_mileage_conversion(self):
        """마일리지 환산 신청"""
        if not self.is_logged_in:
            self.mileage_error_message = "로그인이 필요합니다."
            return

        if self.mileage_request_points <= 0:
            self.mileage_error_message = "환산할 포인트를 입력해주세요."
            return

        if self.mileage_request_points > self.current_user_points:
            self.mileage_error_message = "보유 포인트가 부족합니다."
            return

        try:
            from sqlmodel import Session, create_engine, select
            import os

            db_path = os.path.join(os.getcwd(), "reflex.db")
            db_url = f"sqlite:///{db_path}"
            engine = create_engine(db_url, echo=False)

            # 환산 비율: 1 포인트 = 1 마일리지 (테스트용)
            converted_mileage = self.mileage_request_points
            points_to_deduct = self.mileage_request_points

            with Session(engine) as session:
                # 포인트 차감
                user = session.exec(
                    select(User).where(User.student_id == self.current_user_id)
                ).first()

                if not user:
                    self.mileage_error_message = "사용자를 찾을 수 없습니다."
                    return

                user.current_points -= points_to_deduct
                self.current_user_points = user.current_points
                session.add(user)

                # 환산 신청 기록
                request = MileageRequest(
                    student_id=self.current_user_id,
                    request_points=points_to_deduct,
                    converted_mileage=converted_mileage,
                    status="APPROVED"  # 테스트용 자동 승인
                )
                session.add(request)
                session.commit()

            logger.info(f"마일리지 환산 완료: {self.current_user_id}, 포인트: {points_to_deduct}, 마일리지: {converted_mileage}")
            self.mileage_request_points = 0
            self.mileage_error_message = f"✅ {converted_mileage} 마일리지로 환산 완료!"

        except Exception as e:
            self.mileage_error_message = f"마일리지 환산 실패: {str(e)}"
            logger.error(f"마일리지 환산 오류: {e}", exc_info=True)



