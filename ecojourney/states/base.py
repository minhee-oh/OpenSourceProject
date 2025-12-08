"""
기본 UI 상태 및 공통 기능
"""

import reflex as rx
from typing import Dict, List, Any

# CATEGORY_CONFIG: 모든 카테고리 데이터를 담는 핵심 딕셔너리
CATEGORY_CONFIG = {
    "교통": {
        "path": "transportation",
        "description": "오늘의 교통 수단 이용량(거리 또는 시간)을 입력해주세요.",
        "activities": ["자동차", "지하철", "버스", "걷기", "자전거"],
        "units": ["km", "분"],
        "inputs_key": "transport_inputs"
    },
    "식품": {
        "path": "food",
        "description": "오늘 섭취한 주요 식품 카테고리를 입력해주세요.",
        "activities": ["육류", "채소/과일", "가공식품", "유제품"],
        "units": ["g", "회"],
        "inputs_key": "food_inputs"
    },
    "의류": {
        "path": "clothing",
        "description": "오늘 쇼핑한 의류 및 잡화의 종류와 개수를 입력해주세요.",
        "activities": ["상의", "하의", "신발", "가방/잡화"],
        "units": ["개"],
        "inputs_key": "clothing_inputs"
    }
}

CATEGORY_ORDER = list(CATEGORY_CONFIG.keys())

# 탄소 배출량 데이터를 저장할 딕셔너리 구조 정의
CarbonActivity = Dict[str, Any]

TRANSPORT_LIST = ["자동차", "버스", "지하철", "걷기", "자전거"]
FOOD_LIST = ["육류", "야채류", "유제품류", "기타"]


class BaseState(rx.State):
    """
    기본 UI 상태 및 공통 기능
    """
    current_category: str = "교통"
    all_activities: List[CarbonActivity] = []
    
    # 결과 리포트 데이터
    total_carbon_emission: float = 0.0
    is_report_calculated: bool = False
    calculation_details: List[Dict[str, Any]] = []  # 상세 계산 내역
    
    # 절약량 관련 데이터
    total_saved_emission: float = 0.0  # 총 절약한 탄소 배출량 (kgCO2e)
    saved_money: float = 0.0  # 절약한 금액 (원)
    savings_details: List[Dict[str, Any]] = []  # 절약 상세 내역
    
    # 포인트 관련 데이터
    points_breakdown: Dict[str, int] = {}  # 포인트 상세 내역 (절약량, 빈티지, 평균 대비)
    total_points_earned: int = 0  # 총 획득 포인트
