"""
챌린지 시스템 관련 State
"""

import reflex as rx
from typing import List, Dict, Any
from datetime import datetime
import logging
from .mileage import MileageState
from ..models import Challenge, ChallengeProgress, User

logger = logging.getLogger(__name__)


class ChallengeState(MileageState):
    """
    챌린지 시스템 관련 상태 및 로직
    """
    active_challenges: List[Dict[str, Any]] = []
    user_challenge_progress: List[Dict[str, Any]] = []
    
    async def load_active_challenges(self):
        """활성화된 챌린지 목록 로드"""
        try:
            challenges = await Challenge.find(Challenge.is_active == True)
            self.active_challenges = [
                {
                    "id": ch.id,
                    "title": ch.title,
                    "type": ch.type,
                    "goal_value": ch.goal_value,
                    "reward_points": ch.reward_points
                }
                for ch in challenges
            ]
        except Exception as e:
            logger.error(f"챌린지 로드 오류: {e}")
            self.active_challenges = []
    
    async def update_challenge_progress(self, challenge_id: int, increment: int = 1):
        """챌린지 진행도 업데이트"""
        if not self.is_logged_in:
            return
        
        try:
            # 진행도 조회 또는 생성
            progress_list = await ChallengeProgress.find(
                ChallengeProgress.challenge_id == challenge_id,
                ChallengeProgress.student_id == self.current_user_id
            )
            
            if progress_list:
                progress = progress_list[0]
            else:
                progress = ChallengeProgress(
                    challenge_id=challenge_id,
                    student_id=self.current_user_id,
                    current_value=0,
                    is_completed=False
                )
            
            # 이미 완료된 챌린지는 업데이트하지 않음
            if progress.is_completed:
                return
            
            # 진행도 업데이트
            progress.current_value += increment
            progress.last_updated = datetime.now()
            
            # 챌린지 목표 달성 확인
            challenge = await Challenge.find_by_id(challenge_id)
            if challenge and progress.current_value >= challenge.goal_value:
                progress.is_completed = True
                progress.completed_at = datetime.now()
                
                # 보상 지급
                user = await User.find_by_id(self.current_user_id)
                user.current_points += challenge.reward_points
                self.current_user_points = user.current_points
                await user.save()
                
                logger.info(f"챌린지 완료: {self.current_user_id}, 챌린지: {challenge.title}, 보상: {challenge.reward_points}")
            
            await progress.save()
            
        except Exception as e:
            logger.error(f"챌린지 진행도 업데이트 오류: {e}")


