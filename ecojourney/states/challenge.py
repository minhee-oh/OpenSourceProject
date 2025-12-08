"""
챌린지 시스템 관련 State
"""

import reflex as rx
from typing import List, Dict, Any
from datetime import datetime
import logging
from .battle import BattleState
from ..models import Challenge, ChallengeProgress, User

logger = logging.getLogger(__name__)


class ChallengeState(BattleState):
    """
    챌린지 시스템 관련 상태 및 로직
    """
    active_challenges: List[Dict[str, Any]] = []
    user_challenge_progress: List[Dict[str, Any]] = []
    
    # 탄소 통계 개별 변수 (Reflex에서 Dict 접근 제한 때문에 분리)
    carbon_total_logs: int = 0
    carbon_total_emission: float = 0.0
    carbon_average_daily_emission: float = 0.0
    carbon_total_activities: int = 0
    carbon_category_breakdown: List[Dict[str, Any]] = []
    
    async def load_active_challenges(self):
        """활성화된 챌린지 목록 로드"""
        try:
            from sqlmodel import Session, create_engine, select
            import os
            
            # SQLModel Session을 직접 사용하여 조회
            db_path = os.path.join(os.getcwd(), "reflex.db")
            db_url = f"sqlite:///{db_path}"
            engine = create_engine(db_url, echo=False)
            
            challenges = []
            with Session(engine) as session:
                statement = select(Challenge).where(Challenge.is_active == True)
                challenges = list(session.exec(statement).all())
            
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
            logger.error(f"챌린지 로드 오류: {e}", exc_info=True)
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
                users = await User.find(User.student_id == self.current_user_id)
                if users:
                    user = users[0]
                    user.current_points += challenge.reward_points
                self.current_user_points = user.current_points
                await user.save()
                
                logger.info(f"챌린지 완료: {self.current_user_id}, 챌린지: {challenge.title}, 보상: {challenge.reward_points}")
            
            await progress.save()
            
        except Exception as e:
            logger.error(f"챌린지 진행도 업데이트 오류: {e}")
    
    async def load_user_challenge_progress(self):
        """사용자의 챌린지 진행도 로드"""
        if not self.is_logged_in or not self.current_user_id:
            self.user_challenge_progress = []
            return
        
        try:
            # 활성화된 챌린지 로드
            await self.load_active_challenges()
            
            # 사용자의 진행도 조회 (SQLModel Session 직접 사용)
            from sqlmodel import Session, create_engine, select
            import os
            
            db_path = os.path.join(os.getcwd(), "reflex.db")
            db_url = f"sqlite:///{db_path}"
            engine = create_engine(db_url, echo=False)
            
            all_progress = []
            with Session(engine) as session:
                statement = select(ChallengeProgress).where(
                    ChallengeProgress.student_id == self.current_user_id
                )
                all_progress = list(session.exec(statement).all())
            
            # 챌린지 정보와 진행도 결합
            progress_dict = {p.challenge_id: p for p in all_progress}
            
            result = []
            for challenge in self.active_challenges:
                challenge_id = challenge["id"]
                progress = progress_dict.get(challenge_id)
                
                if progress:
                    progress_percent = (progress.current_value / challenge["goal_value"]) * 100 if challenge["goal_value"] > 0 else 0
                    result.append({
                        "challenge_id": challenge_id,
                        "title": challenge["title"],
                        "type": challenge["type"],
                        "goal_value": challenge["goal_value"],
                        "current_value": progress.current_value,
                        "progress_percent": min(progress_percent, 100),
                        "is_completed": progress.is_completed,
                        "reward_points": challenge["reward_points"]
                    })
                else:
                    # 진행도가 없으면 0으로 시작
                    result.append({
                        "challenge_id": challenge_id,
                        "title": challenge["title"],
                        "type": challenge["type"],
                        "goal_value": challenge["goal_value"],
                        "current_value": 0,
                        "progress_percent": 0,
                        "is_completed": False,
                        "reward_points": challenge["reward_points"]
                    })
            
            self.user_challenge_progress = result
            
        except Exception as e:
            logger.error(f"사용자 챌린지 진행도 로드 오류: {e}")
            self.user_challenge_progress = []
    
    # 포인트 로그 관련 변수
    points_log: List[Dict[str, Any]] = []
    
    async def load_points_log(self):
        """포인트 획득 내역 로드 (날짜별)"""
        if not self.is_logged_in or not self.current_user_id:
            self.points_log = []
            return
        
        try:
            from ..models import CarbonLog
            from sqlmodel import Session, create_engine, select
            import os
            
            db_path = os.path.join(os.getcwd(), "reflex.db")
            db_url = f"sqlite:///{db_path}"
            engine = create_engine(db_url, echo=False)
            
            with Session(engine) as session:
                # 포인트가 0보다 큰 로그만 조회 (포인트가 있는 기록만 표시)
                stmt = select(CarbonLog).where(
                    CarbonLog.student_id == self.current_user_id,
                    CarbonLog.points_earned > 0
                ).order_by(CarbonLog.log_date.desc())
                
                logger.info(f"[포인트 로그] 조회 조건: student_id={self.current_user_id}, points_earned > 0")
                print(f"[포인트 로그] 조회 조건: student_id={self.current_user_id}, points_earned > 0")
                
                logs = session.exec(stmt).all()
                print(f"[포인트 로그] 조회 결과: {len(logs)}개")
                
                result = []
                for log in logs:
                    result.append({
                        "date": log.log_date.strftime("%Y-%m-%d") if log.log_date else "",
                        "points": log.points_earned
                    })
                    print(f"[포인트 로그] 날짜: {log.log_date}, 포인트: {log.points_earned}점")
                
                self.points_log = result
                logger.info(f"포인트 로그 로드 완료: {len(result)}개")
                print(f"[포인트 로그] 최종 결과: {len(result)}개")
                
        except Exception as e:
            logger.error(f"포인트 로그 로드 오류: {e}", exc_info=True)
            self.points_log = []
    
    async def load_mypage_data(self):
        """마이페이지 모든 데이터 로드"""
        if not self.is_logged_in or not self.current_user_id:
            return
        
        try:
            # 사용자 포인트 정보 새로고침
            from ..models import User
            from sqlmodel import Session, create_engine, select
            import os
            
            db_path = os.path.join(os.getcwd(), "reflex.db")
            db_url = f"sqlite:///{db_path}"
            engine = create_engine(db_url, echo=False)
            
            with Session(engine) as session:
                user_stmt = select(User).where(User.student_id == self.current_user_id)
                user = session.exec(user_stmt).first()
                if user:
                    self.current_user_points = user.current_points
                    logger.info(f"[마이페이지] 사용자 포인트 새로고침: {self.current_user_points}점")
        except Exception as e:
            logger.error(f"사용자 포인트 새로고침 오류: {e}", exc_info=True)
        
        try:
            # 챌린지 진행도 로드
            await self.load_user_challenge_progress()
        except Exception as e:
            logger.error(f"챌린지 진행도 로드 오류: {e}", exc_info=True)
        
        try:
            # 탄소 통계 로드 및 개별 변수에 할당
            stats = await self.get_carbon_statistics()
            self.carbon_total_logs = stats.get("total_logs", 0)
            self.carbon_total_emission = stats.get("total_emission", 0.0)
            self.carbon_average_daily_emission = stats.get("average_daily_emission", 0.0)
            self.carbon_total_activities = stats.get("total_activities", 0)
            self.carbon_category_breakdown = stats.get("category_breakdown", [])
        except Exception as e:
            logger.error(f"탄소 통계 로드 오류: {e}", exc_info=True)
            # 기본값 설정
            self.carbon_total_logs = 0
            self.carbon_total_emission = 0.0
            self.carbon_average_daily_emission = 0.0
            self.carbon_total_activities = 0
            self.carbon_category_breakdown = []
        
        try:
            # 포인트 로그 로드
            await self.load_points_log()
        except Exception as e:
            logger.error(f"포인트 로그 로드 오류: {e}", exc_info=True)
            self.points_log = []
        
        logger.info(f"마이페이지 데이터 로드 완료: {self.current_user_id}, 포인트: {self.current_user_points}점")



