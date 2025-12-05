"""
탄소 배출량 입력 및 저장 관련 State
"""

import reflex as rx
from typing import Dict, List, Any, Optional
from datetime import date
import logging
from .base import BaseState
from .auth import AuthState
from ..models import User, CarbonLog

logger = logging.getLogger(__name__)


class CarbonState(AuthState):
    """
    탄소 배출량 입력 및 저장 관련 상태 및 로직
    """
    # 저장 관련 상태
    save_message: str = ""
    is_saving: bool = False
    is_save_success: bool = False
    saved_logs_history: List[Dict[str, Any]] = []
    
    # ---------- 교통수단 선택 상태 ----------
    selected_car: bool = False
    selected_bus: bool = False
    selected_subway: bool = False
    selected_walk: bool = False
    selected_bike: bool = False
    
    # 입력 필드 표시 여부
    show_car: bool = False
    show_bus: bool = False
    show_subway: bool = False
    show_walk: bool = False
    show_bike: bool = False
    trans_input_mode: bool = False

    # ---------- 식품 선택 상태 ----------
    selected_meat: bool = False
    selected_veg: bool = False
    selected_dairy: bool = False
    selected_rice: bool = False
    selected_coffee: bool = False

    show_meat: bool = False
    show_veg: bool = False
    show_dairy: bool = False
    show_rice: bool = False
    show_coffee: bool = False
    food_input_mode: bool = False
    
    def _update_avatar_status(self, total_emission: float) -> str:
        """탄소 배출량에 따라 아바타 상태를 업데이트합니다."""
        if total_emission < 5.0:
            return "GOOD"
        elif total_emission < 10.0:
            return "NORMAL"
        elif total_emission < 15.0:
            return "BAD"
        else:
            return "SICK"
    
    # ------------------------------ 교통 관련 메서드 ------------------------------
    
    def toggle_car(self):
        self.selected_car = not self.selected_car
    
    def toggle_bus(self):
        self.selected_bus = not self.selected_bus
    
    def toggle_subway(self):
        self.selected_subway = not self.selected_subway
    
    def toggle_walk(self):
        self.selected_walk = not self.selected_walk
    
    def toggle_bike(self):
        self.selected_bike = not self.selected_bike
    
    def show_trans_input_fields(self):
        """선택된 항목들의 입력 필드를 표시"""
        self.show_car = self.selected_car
        self.show_bus = self.selected_bus
        self.show_subway = self.selected_subway
        self.show_walk = self.selected_walk
        self.show_bike = self.selected_bike
        self.trans_input_mode = True
    
    def handle_transport_submit(self, form_data: dict):
        """교통 입력값 폼 제출 -> 데이터 저장 -> 다음 페이지 이동"""
        # 기존 교통 데이터 제거
        self.all_activities = [
            act for act in self.all_activities 
            if act.get("category") != "교통"
        ]
        
        transport_data = []
        
        if self.show_car and form_data.get("car_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "자동차",
                "value": float(form_data.get("car_value", 0)),
                "unit": form_data.get("car_unit", "km"),
            })
        
        if self.show_bus and form_data.get("bus_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "버스",
                "value": float(form_data.get("bus_value", 0)),
                "unit": form_data.get("bus_unit", "km"),
            })
        
        if self.show_subway and form_data.get("subway_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "지하철",
                "value": float(form_data.get("subway_value", 0)),
                "unit": form_data.get("subway_unit", "km"),
            })
        
        if self.show_walk and form_data.get("walk_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "걷기",
                "value": float(form_data.get("walk_value", 0)),
                "unit": form_data.get("walk_unit", "km"),
            })
        
        if self.show_bike and form_data.get("bike_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "자전거",
                "value": float(form_data.get("bike_value", 0)),
                "unit": form_data.get("bike_unit", "km"),
            })
        
        self.all_activities = self.all_activities + transport_data
        
        # 입력모드 종료 + 선택 초기화
        self.trans_input_mode = False
        self.selected_car = False
        self.selected_bus = False
        self.selected_subway = False
        self.selected_walk = False
        self.selected_bike = False
        self.show_car = False
        self.show_bus = False
        self.show_subway = False
        self.show_walk = False
        self.show_bike = False
        
        return rx.redirect("/input/food")
    
    # ------------------------------ 식품 관련 메서드 ------------------------------
    
    def toggle_meat(self):
        self.selected_meat = not self.selected_meat

    def toggle_veg(self):
        self.selected_veg = not self.selected_veg

    def toggle_dairy(self):
        self.selected_dairy = not self.selected_dairy

    def toggle_rice(self):
        self.selected_rice = not self.selected_rice

    def toggle_coffee(self):
        self.selected_coffee = not self.selected_coffee

    def show_food_input_fields(self):
        """선택된 음식 항목들의 입력 필드를 표시"""
        self.show_meat = self.selected_meat
        self.show_veg = self.selected_veg
        self.show_dairy = self.selected_dairy
        self.show_rice = self.selected_rice
        self.show_coffee = self.selected_coffee
        self.food_input_mode = True

    def handle_food_submit(self, form_data: dict):
        """음식 입력값 제출 처리"""
        # 기존 음식 데이터 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != "식품"
        ]

        food_data = []

        if self.show_meat and form_data.get("meat_value"):
            # 고기류: 세부 선택(소고기/돼지고기/닭고기)을 activity_type으로 저장
            meat_sub = form_data.get("meat_sub") or "소고기"
            food_data.append({
                "category": "식품",
                "activity_type": meat_sub,
                "subcategory": "고기류",
                "value": float(form_data.get("meat_value", 0)),
                "unit": form_data.get("meat_unit", "g"),
            })

        if self.show_veg and form_data.get("veg_value"):
            # 채소류: 양파/파/마늘 등을 activity_type으로 저장
            veg_sub = form_data.get("veg_sub") or "양파"
            food_data.append({
                "category": "식품",
                "activity_type": veg_sub,
                "subcategory": "채소류",
                "value": float(form_data.get("veg_value", 0)),
                "unit": form_data.get("veg_unit", "g"),
            })

        if self.show_dairy and form_data.get("dairy_value"):
            # 유제품류: 우유/치즈 등을 activity_type으로 저장
            dairy_sub = form_data.get("dairy_sub") or "우유"
            food_data.append({
                "category": "식품",
                "activity_type": dairy_sub,
                "subcategory": "유제품류",
                "value": float(form_data.get("dairy_value", 0)),
                "unit": form_data.get("dairy_unit", "g"),
            })

        if self.show_rice and form_data.get("rice_value"):
            # 쌀밥: 하위 카테고리 없음
            food_data.append({
                "category": "식품",
                "activity_type": "쌀밥",
                "subcategory": "쌀밥",
                "value": float(form_data.get("rice_value", 0)),
                "unit": form_data.get("rice_unit", "g"),
            })

        if self.show_coffee and form_data.get("coffee_value"):
            # 커피: 아메리카노/카페라떼를 activity_type으로 저장
            coffee_sub = form_data.get("coffee_sub") or "아메리카노"
            food_data.append({
                "category": "식품",
                "activity_type": coffee_sub,
                "subcategory": "커피",
                "value": float(form_data.get("coffee_value", 0)),
                "unit": form_data.get("coffee_unit", "g"),
            })

        self.all_activities = self.all_activities + food_data

        # 입력모드 종료 + 선택 초기화
        self.food_input_mode = False
        self.selected_meat = False
        self.selected_veg = False
        self.selected_dairy = False
        self.selected_rice = False
        self.selected_coffee = False
        self.show_meat = False
        self.show_veg = False
        self.show_dairy = False
        self.show_rice = False
        self.show_coffee = False

        return rx.redirect("/input/clothing")
    
    # ------------------------------ 의류 관련 메서드 ------------------------------
    
    # 의류 입력 상태
    clothing_type: str = ""
    clothing_count: float = 0.0
    clothing_is_vintage: bool = False
    
    def handle_clothing_submit(self, form_data: dict):
        """의류 입력값 제출 처리"""
        # 기존 의류 데이터 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != "의류"
        ]

        clothing_items = []

        # 여러 종류를 한 번에 입력할 수 있도록 처리
        mapping = [
            ("상의", "top_count"),
            ("하의", "bottom_count"),
            ("신발", "shoes_count"),
            ("가방/잡화", "bag_count"),
        ]

        for label, field in mapping:
            value_str = form_data.get(field)
            if value_str:
                try:
                    value = float(value_str)
                except ValueError:
                    continue
                if value > 0:
                    clothing_items.append({
                        "category": "의류",
                        "activity_type": label,
                        "value": value,
                        "unit": "개",
                        "is_vintage": False,
                    })

        if clothing_items:
            self.all_activities = self.all_activities + clothing_items
        
        # 폼 초기화
        self.clothing_type = ""
        self.clothing_count = 0.0
        self.clothing_is_vintage = False
        
        return rx.redirect("/input/electricity")
    
    # ------------------------------ 전기 관련 메서드 ------------------------------
    
    # 전기 입력 상태
    electricity_type: str = ""
    electricity_hours: float = 0.0
    
    def handle_electricity_submit(self, form_data: dict):
        """전기 입력값 제출 처리"""
        # 기존 전기 데이터 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != "전기"
        ]

        electricity_items = []

        # 냉방기 / 난방기를 한 번에 입력
        cooling = form_data.get("cooling_hours")
        heating = form_data.get("heating_hours")

        if cooling:
            try:
                v = float(cooling)
                if v > 0:
                    electricity_items.append({
                        "category": "전기",
                        "activity_type": "냉방기",
                        "value": v,
                        "unit": "시간",
                    })
            except ValueError:
                pass

        if heating:
            try:
                v = float(heating)
                if v > 0:
                    electricity_items.append({
                        "category": "전기",
                        "activity_type": "난방기",
                        "value": v,
                        "unit": "시간",
                    })
            except ValueError:
                pass

        if electricity_items:
            self.all_activities = self.all_activities + electricity_items
        
        # 폼 초기화
        self.electricity_type = ""
        self.electricity_hours = 0.0
        
        return rx.redirect("/input/waste")
    
    # ------------------------------ 쓰레기 관련 메서드 ------------------------------
    
    # 쓰레기 입력 상태
    waste_type: str = ""
    waste_amount: float = 0.0
    waste_unit: str = "kg"
    
    def handle_waste_submit(self, form_data: dict):
        """쓰레기 입력값 제출 처리"""
        # 기존 쓰레기 데이터 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != "쓰레기"
        ]

        waste_items = []

        def add_waste(label: str, amount_key: str, unit_key: str):
            value_str = form_data.get(amount_key)
            if not value_str:
                return
            try:
                value = float(value_str)
            except ValueError:
                return
            if value <= 0:
                return
            unit = form_data.get(unit_key, "kg")
            waste_items.append({
                "category": "쓰레기",
                "activity_type": label,
                "value": value,
                "unit": unit,
            })

        add_waste("일반", "waste_general_amount", "waste_general_unit")
        add_waste("플라스틱", "waste_plastic_amount", "waste_plastic_unit")
        add_waste("종이", "waste_paper_amount", "waste_paper_unit")
        add_waste("유리", "waste_glass_amount", "waste_glass_unit")
        add_waste("캔", "waste_can_amount", "waste_can_unit")

        if waste_items:
            self.all_activities = self.all_activities + waste_items
        
        # 폼 초기화
        self.waste_type = ""
        self.waste_amount = 0.0
        self.waste_unit = "kg"
        
        return rx.redirect("/input/water")
    
    # ------------------------------ 물 관련 메서드 ------------------------------
    
    # 물 입력 상태
    water_type: str = ""
    water_amount: float = 0.0
    water_unit: str = "회"
    
    async def handle_water_submit(self, form_data: dict):
        """물 입력값 제출 처리"""
        # 기존 물 데이터 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != "물"
        ]

        water_items = []

        def add_water(label: str, count_key: str, unit_key: str):
            value_str = form_data.get(count_key)
            if not value_str:
                return
            try:
                value = float(value_str)
            except ValueError:
                return
            if value <= 0:
                return
            unit = form_data.get(unit_key, "회")
            water_items.append({
                "category": "물",
                "activity_type": label,
                "value": value,
                "unit": unit,
            })

        add_water("샤워", "water_shower_count", "water_shower_unit")
        add_water("설거지", "water_dish_count", "water_dish_unit")
        add_water("세탁", "water_laundry_count", "water_laundry_unit")

        if water_items:
            self.all_activities = self.all_activities + water_items
        
        # 폼 초기화
        self.water_type = ""
        self.water_amount = 0.0
        self.water_unit = "회"
        
        # 리포트로 이동하기 전에 자동으로 계산 수행
        await self.calculate_report()
        
        return rx.redirect("/report")
    
    # ------------------------------ 리포트 계산 메서드 ------------------------------
    
    async def calculate_report(self):
        """리포트 페이지에서 전체 탄소 배출량을 계산합니다."""
        logger.info("[리포트 계산] 시작 - 전체 활동 데이터 계산 중...")
        
        try:
            from ..service.carbon_calculator import calculate_carbon_emission
            
            total_emission = 0.0
            calculation_details = []  # 상세 계산 내역 저장
            
            logger.info(f"[리포트 계산] 총 {len(self.all_activities)}개의 활동 데이터 처리 시작")
            
            for idx, activity in enumerate(self.all_activities):
                category = activity.get("category", "")
                activity_type = activity.get("activity_type", "")
                value = activity.get("value", 0)
                unit = activity.get("unit", "")
                sub_category = activity.get("subcategory") or activity.get("is_vintage")
                
                logger.info(f"[리포트 계산] [{idx+1}/{len(self.all_activities)}] 처리 중 - 카테고리: {category}, 활동: {activity_type}, 값: {value}{unit}")
                
                # 탄소 배출량 계산
                result = calculate_carbon_emission(
                    category=category,
                    activity_type=activity_type,
                    value=value,
                    unit=unit,
                    sub_category=sub_category
                )
                
                emission = result.get("carbon_emission_kg", 0.0)
                method = result.get("calculation_method", "local")
                total_emission += emission
                
                calculation_details.append({
                    "category": category,
                    "activity_type": activity_type,
                    "value": value,
                    "unit": unit,
                    "emission": emission,
                    "method": method
                })
                
                logger.info(f"[리포트 계산] ✅ [{idx+1}/{len(self.all_activities)}] 계산 완료: {category}/{activity_type} = {emission}kgCO2e (방법: {method})")
            
            # 결과 저장
            self.total_carbon_emission = round(total_emission, 3)
            self.is_report_calculated = True
            self.calculation_details = calculation_details  # 상세 내역 저장
            
            logger.info(f"[리포트 계산] ✅ 전체 계산 완료! 총 배출량: {self.total_carbon_emission}kgCO2e")
            logger.info(f"[리포트 계산] 계산 상세 내역: {calculation_details}")
            
        except Exception as e:
            logger.error(f"[리포트 계산] ❌ 계산 오류 발생: {e}", exc_info=True)
            self.total_carbon_emission = 0.0
            self.is_report_calculated = False
    
    # ------------------------------ DB 저장 메서드 ------------------------------
    
    async def save_carbon_log_to_db(self):
        """현재 입력된 탄소 배출량을 데이터베이스에 저장"""
        if not self.is_logged_in or not self.current_user_id:
            self.save_message = "로그인이 필요합니다."
            return
        
        self.is_saving = True
        self.save_message = ""
        
        try:
            import json
            from ..service.carbon_calculator import calculate_carbon_emission
            
            # 전체 탄소 배출량 계산 (이미 계산된 값이 있으면 사용)
            if not self.is_report_calculated or self.total_carbon_emission == 0.0:
                total_emission = 0.0
                for activity in self.all_activities:
                    category = activity.get("category")
                    activity_type = activity.get("activity_type")
                    value = activity.get("value", 0)
                    unit = activity.get("unit", "")
                    sub_category = activity.get("subcategory") or activity.get("is_vintage")
                    
                    result = calculate_carbon_emission(
                        category=category,
                        activity_type=activity_type,
                        value=value,
                        unit=unit,
                        sub_category=sub_category
                    )
                    emission = result.get("carbon_emission_kg", 0.0)
                    total_emission += emission
            else:
                total_emission = self.total_carbon_emission
            
            # 간단한 통계 수집 (기존 호환성 유지)
            transport_km = 0.0
            ac_hours = 0.0
            cup_count = 0
            
            for activity in self.all_activities:
                category = activity.get("category")
                activity_type = activity.get("activity_type")
                value = activity.get("value", 0)
                unit = activity.get("unit", "")
                
                if category == "교통":
                    if unit == "km":
                        transport_km += value
                    elif unit == "분":
                        if activity_type == "자동차":
                            transport_km += value * 30 / 60
                        elif activity_type == "버스":
                            transport_km += value * 25 / 60
                        elif activity_type == "지하철":
                            transport_km += value * 30 / 60
                elif category == "전기":
                    if activity_type == "냉방기":
                        ac_hours += value
                elif category == "쓰레기":
                    if activity_type == "일회용컵":
                        cup_count += int(value)
            
            # all_activities를 JSON으로 변환
            activities_json = json.dumps(self.all_activities, ensure_ascii=False, default=str)
            
            # 오늘 날짜의 기존 로그 확인 (SQLModel Session 사용)
            from sqlmodel import Session, create_engine, select
            import os
            
            db_path = os.path.join(os.getcwd(), "reflex.db")
            db_url = f"sqlite:///{db_path}"
            engine = create_engine(db_url, echo=False)
            
            today = date.today()
            existing_log = None
            with Session(engine) as session:
                stmt = select(CarbonLog).where(
                    CarbonLog.student_id == self.current_user_id,
                    CarbonLog.log_date == today
                )
                existing_log = session.exec(stmt).first()
                
                if existing_log:
                    log = existing_log
                    log.transport_km = transport_km
                    log.ac_hours = ac_hours
                    log.cup_count = cup_count
                    log.total_emission = total_emission
                    log.activities_json = activities_json
                    session.add(log)
                else:
                    log = CarbonLog(
                        student_id=self.current_user_id,
                        log_date=today,
                        transport_km=transport_km,
                        ac_hours=ac_hours,
                        cup_count=cup_count,
                        total_emission=total_emission,
                        activities_json=activities_json
                    )
                    session.add(log)
                
                session.commit()
            
            # 사용자 아바타 상태 업데이트 및 포인트 지급
            points_earned = 0
            with Session(engine) as session:
                user_stmt = select(User).where(User.student_id == self.current_user_id)
                user = session.exec(user_stmt).first()
                
                if user:
                    user.avatar_status = self._update_avatar_status(total_emission)
                    if not existing_log:
                        points_earned = int(total_emission * 10)
                        user.current_points += points_earned
                        self.current_user_points = user.current_points
                        self.save_message = f"✅ 저장 완료! 포인트 {points_earned}점을 획득했습니다."
                    else:
                        self.save_message = "✅ 데이터가 업데이트되었습니다."
                    
                    self.is_save_success = True
                    session.add(user)
                    session.commit()
                    logger.info(f"탄소 로그 저장/업데이트 완료: {self.current_user_id}, 배출량: {total_emission}kg, 포인트: {user.current_points}")
                else:
                    self.save_message = "❌ 사용자 정보를 찾을 수 없습니다."
                    self.is_save_success = False
                    logger.error(f"탄소 로그 저장 오류: 사용자 {self.current_user_id}를 찾을 수 없음")
            
            self.is_saving = False
            
        except Exception as e:
            self.save_message = f"❌ 저장 중 오류가 발생했습니다: {str(e)}"
            self.is_save_success = False
            self.is_saving = False
            logger.error(f"탄소 로그 저장 오류: {e}", exc_info=True)
    
    async def load_saved_logs_history(self):
        """저장된 로그 이력을 불러옵니다."""
        self.saved_logs_history = await self.get_saved_logs_history(limit=10)
    
    async def load_saved_activities(self):
        """저장된 입력 데이터를 불러옵니다. 오늘 날짜의 데이터를 불러옵니다."""
        if not self.is_logged_in or not self.current_user_id:
            return
        
        try:
            target_date = date.today()
            
            logs = await CarbonLog.find(
                CarbonLog.student_id == self.current_user_id,
                CarbonLog.log_date == target_date
            )
            
            if logs:
                log = logs[0]
                activities = log.get_activities()
                if activities:
                    self.all_activities = activities
                    # 저장된 데이터가 있으면 자동으로 계산 수행
                    await self.calculate_report()
                    logger.info(f"저장된 데이터 불러오기 완료: {self.current_user_id}, 날짜: {target_date}, 활동 수: {len(activities)}")
                else:
                    logger.info(f"저장된 데이터가 없습니다: {self.current_user_id}, 날짜: {target_date}")
            else:
                logger.info(f"저장된 로그가 없습니다: {self.current_user_id}, 날짜: {target_date}")
                
        except Exception as e:
            logger.error(f"저장된 데이터 불러오기 오류: {e}", exc_info=True)
    
    async def get_saved_logs_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """저장된 로그 이력을 반환합니다."""
        if not self.is_logged_in or not self.current_user_id:
            return []
        
        try:
            logs = await CarbonLog.find(
                CarbonLog.student_id == self.current_user_id
            )
            
            # 날짜순으로 정렬 (최신순)
            logs.sort(key=lambda x: x.log_date, reverse=True)
            
            result = []
            for log in logs[:limit]:
                result.append({
                    "log_date": log.log_date,
                    "total_emission": log.total_emission,
                    "activities_count": len(log.get_activities()),
                    "created_at": log.created_at
                })
            
            return result
            
        except Exception as e:
            logger.error(f"로그 이력 조회 오류: {e}", exc_info=True)
            return []
    
    async def get_carbon_statistics(self) -> Dict[str, Any]:
        """탄소 배출량 통계 데이터 반환"""
        if not self.is_logged_in or not self.current_user_id:
            return {
                "total_logs": 0,
                "total_emission": 0.0,
                "average_daily_emission": 0.0,
                "total_activities": 0,
                "category_breakdown": []
            }
        
        try:
            from ..models import CarbonLog
            from sqlmodel import Session, create_engine, select
            import os
            
            # SQLModel Session을 직접 사용하여 조회
            db_path = os.path.join(os.getcwd(), "reflex.db")
            db_url = f"sqlite:///{db_path}"
            engine = create_engine(db_url, echo=False)
            
            logs = []
            with Session(engine) as session:
                statement = select(CarbonLog).where(CarbonLog.student_id == self.current_user_id)
                logs = list(session.exec(statement).all())
            
            if not logs:
                return {
                    "total_logs": 0,
                    "total_emission": 0.0,
                    "average_daily_emission": 0.0,
                    "total_activities": 0,
                    "category_breakdown": []
                }
            
            # 통계 계산
            total_logs = len(logs)
            total_emission = sum(log.total_emission for log in logs)
            average_daily_emission = total_emission / total_logs if total_logs > 0 else 0.0
            
            # 카테고리별 통계
            category_breakdown = {}
            total_activities = 0
            
            for log in logs:
                activities = log.get_activities()
                total_activities += len(activities)
                
                for activity in activities:
                    category = activity.get("category", "기타")
                    if category not in category_breakdown:
                        category_breakdown[category] = 0
                    category_breakdown[category] += 1
            
            # Dict를 리스트로 변환하고 비율 계산 (Reflex foreach에서 사용하기 위해)
            category_list = []
            for k, v in category_breakdown.items():
                percent = (v / total_activities * 100) if total_activities > 0 else 0
                category_list.append({
                    "name": k,
                    "count": v,
                    "percent": round(percent, 1)
                })
            
            return {
                "total_logs": total_logs,
                "total_emission": round(total_emission, 2),
                "average_daily_emission": round(average_daily_emission, 2),
                "total_activities": total_activities,
                "category_breakdown": category_list
            }
            
        except Exception as e:
            logger.error(f"탄소 통계 조회 오류: {e}", exc_info=True)
            return {
                "total_logs": 0,
                "total_emission": 0.0,
                "average_daily_emission": 0.0,
                "total_activities": 0,
                "category_breakdown": []
            }

