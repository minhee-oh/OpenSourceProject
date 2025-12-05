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
            # 환산 비율: 1 포인트 = 1 마일리지 (테스트용)
            converted_mileage = self.mileage_request_points
            
            # 포인트 차감
            user = await User.find_by_id(self.current_user_id)
            user.current_points -= self.mileage_request_points
            self.current_user_points = user.current_points
            await user.save()
            
            # 환산 신청 기록
            request = MileageRequest(
                student_id=self.current_user_id,
                request_points=self.mileage_request_points,
                converted_mileage=converted_mileage,
                status="APPROVED"  # 테스트용 자동 승인
            )
            await request.save()
            
            self.mileage_request_points = 0
            self.mileage_error_message = ""
            logger.info(f"마일리지 환산 완료: {self.current_user_id}, 포인트: {self.mileage_request_points}, 마일리지: {converted_mileage}")
            
        except Exception as e:
            self.mileage_error_message = f"마일리지 환산 실패: {str(e)}"
            logger.error(f"마일리지 환산 오류: {e}")


