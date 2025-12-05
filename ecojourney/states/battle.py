"""
대항전 시스템 관련 State
"""

import reflex as rx
from typing import Optional, Dict, Any
from datetime import date
import logging
from .carbon import CarbonState
from ..models import Battle, BattleParticipant, User

logger = logging.getLogger(__name__)


class BattleState(CarbonState):
    """
    대항전 시스템 관련 상태 및 로직
    """
    current_battle: Optional[Dict[str, Any]] = None
    battle_bet_amount: int = 0
    battle_error_message: str = ""
    
    async def load_current_battle(self):
        """현재 활성화된 대항전 정보 로드"""
        if not self.is_logged_in:
            return
        
        try:
            today = date.today()
            battles = await Battle.find(
                Battle.status == "ACTIVE",
                Battle.start_date <= today,
                Battle.end_date >= today
            )
            
            if battles:
                battle = battles[0]
                if battle.college_a == self.current_user_college or battle.college_b == self.current_user_college:
                    self.current_battle = {
                        "id": battle.id,
                        "college_a": battle.college_a,
                        "college_b": battle.college_b,
                        "score_a": battle.score_a,
                        "score_b": battle.score_b,
                        "start_date": battle.start_date,
                        "end_date": battle.end_date
                    }
                else:
                    self.current_battle = None
            else:
                self.current_battle = None
                
        except Exception as e:
            logger.error(f"대항전 로드 오류: {e}")
            self.current_battle = None
    
    async def join_battle(self):
        """대항전 참가 및 베팅"""
        if not self.is_logged_in or not self.current_battle:
            self.battle_error_message = "대항전 정보를 불러올 수 없습니다."
            return
        
        if self.battle_bet_amount <= 0:
            self.battle_error_message = "베팅 포인트를 입력해주세요."
            return
        
        if self.battle_bet_amount > self.current_user_points:
            self.battle_error_message = "보유 포인트가 부족합니다."
            return
        
        try:
            battle_id = self.current_battle["id"]
            
            # 이미 참가했는지 확인
            existing_participants = await BattleParticipant.find(
                BattleParticipant.battle_id == battle_id,
                BattleParticipant.student_id == self.current_user_id
            )
            
            if existing_participants:
                self.battle_error_message = "이미 참가한 대항전입니다."
                return
            
            # 포인트 차감
            user = await User.find_by_id(self.current_user_id)
            user.current_points -= self.battle_bet_amount
            self.current_user_points = user.current_points
            await user.save()
            
            # 참가자 등록
            participant = BattleParticipant(
                battle_id=battle_id,
                student_id=self.current_user_id,
                bet_amount=self.battle_bet_amount,
                reward_amount=0
            )
            await participant.save()
            
            # 대항전 점수 업데이트
            battle = await Battle.find_by_id(battle_id)
            if battle:
                if battle.college_a == self.current_user_college:
                    battle.score_a += self.battle_bet_amount
                elif battle.college_b == self.current_user_college:
                    battle.score_b += self.battle_bet_amount
                await battle.save()
            
            self.battle_bet_amount = 0
            self.battle_error_message = ""
            logger.info(f"대항전 참가 완료: {self.current_user_id}, 베팅: {self.battle_bet_amount}")
            
        except Exception as e:
            self.battle_error_message = f"대항전 참가 실패: {str(e)}"
            logger.error(f"대항전 참가 오류: {e}")


