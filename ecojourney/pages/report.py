# report.py

import reflex as rx
from ecojourney.state import AppState
from typing import Dict, Any

def report_page() -> rx.Component:
    """
    최종 탄소 발자국 리포트 페이지 컴포넌트입니다.
    페이지 로드 시 자동으로 탄소 배출량을 계산합니다.
    """
    # 페이지 로드 시 자동으로 계산 수행 (조건부 렌더링으로 트리거)
    # 리포트 페이지가 렌더링될 때 계산이 안 되어 있으면 자동으로 계산
    return rx.center(
        rx.vstack(
            rx.heading("🌍 탄소 발자국 측정 결과", size="7", margin_bottom="20px"),
            
            # 계산 버튼 (수동 재계산용)
            rx.cond(
                ~AppState.is_report_calculated,
                rx.button(
                    "📊 탄소 배출량 계산하기",
                    on_click=AppState.calculate_report,
                    color_scheme="blue",
                    size="3",
                    margin_bottom="20px"
                ),
            ),
            
            # 1. 계산 상태 확인
            rx.cond(
                AppState.is_report_calculated,
                rx.vstack(
                    rx.text("✅ 최종 계산이 완료되었습니다.", color="green.700", size="5"),
                    rx.text(
                        f"총 {AppState.all_activities.length()}개의 활동이 계산되었습니다.",
                        color="gray.600",
                        size="3"
                    ),
                    spacing="2"
                ),
                rx.text("⏳ 계산이 완료되지 않았습니다. 위 버튼을 클릭하여 계산하세요.", color="orange.700", size="5"),
            ),
            
            rx.divider(margin_y="20px"),
            
            # 2. 총 배출량 (더미 값 또는 실제 State 값 참조)
            rx.text(
                "총 배출량 (kg CO2e):", 
                font_weight="bold"
            ),
            rx.text(
                AppState.total_carbon_emission, 
                size="8", 
                color="blue.700"
            ),
            
            # 3. 상세 내역 (데이터 개수 확인)
            rx.text(
                f"총 활동 기록 수: {AppState.all_activities.length()}",
                color="gray.600"
            ),
            
            rx.divider(margin_y="20px"),
            
            # 4. 상세 계산 내역 표시
            rx.cond(
                AppState.is_report_calculated & (AppState.calculation_details.length() > 0),
                rx.vstack(
                    rx.heading("📋 상세 계산 내역", size="5", margin_bottom="10px"),
                    rx.foreach(
                        AppState.calculation_details,
                        lambda detail: rx.hstack(
                            rx.hstack(
                                rx.text(detail["category"], font_weight="bold"),
                                rx.text(" - ", font_weight="bold"),
                                rx.text(detail["activity_type"], font_weight="bold"),
                                rx.text(": ", font_weight="bold"),
                                spacing="0",
                                width="200px"
                            ),
                            rx.hstack(
                                rx.text(detail["value"], color="gray.600"),
                                rx.text(detail["unit"], color="gray.600"),
                                rx.text(" = ", color="gray.600"),
                                spacing="0"
                            ),
                            rx.hstack(
                                rx.text(detail["emission"], color="blue.700", font_weight="bold"),
                                rx.text("kgCO2e", color="blue.700", font_weight="bold"),
                                spacing="0"
                            ),
                            rx.hstack(
                                rx.text("(", color="green.600", size="2"),
                                rx.text(detail["method"], color="green.600", size="2"),
                                rx.text(")", color="green.600", size="2"),
                                spacing="0"
                            ),
                            spacing="2",
                            margin_bottom="5px"
                        )
                    ),
                    spacing="2",
                    padding="20px",
                    border="1px solid",
                    border_color="gray.300",
                    border_radius="8px",
                    margin_bottom="20px"
                ),
            ),
            
            rx.divider(margin_y="20px"),
            
            # 저장 버튼 및 메시지 (로그인한 경우에만 표시)
            rx.cond(
                AppState.is_logged_in,
                rx.vstack(
                    rx.cond(
                        AppState.is_saving,
                        rx.text("💾 저장 중...", color="blue.600", size="4"),
                        rx.button(
                            "💾 데이터 저장하기",
                            on_click=AppState.save_carbon_log_to_db,
                            color_scheme="green",
                            size="3",
                            is_disabled=~AppState.is_report_calculated,
                            margin_bottom="10px"
                        )
                    ),
                    rx.cond(
                        AppState.save_message != "",
                        rx.text(
                            AppState.save_message,
                            color=rx.cond(
                                AppState.is_save_success,
                                "green.700",
                                "red.700"
                            ),
                            size="4",
                            margin_bottom="10px"
                        ),
                    ),
                    spacing="2",
                    margin_bottom="20px"
                ),
            ),
            
            rx.divider(margin_y="20px"),
            
            # 저장된 데이터 확인 섹션
            rx.cond(
                AppState.is_logged_in,
                rx.vstack(
                    rx.heading("📚 저장된 기록 확인", size="5", margin_bottom="10px"),
                    rx.button(
                        "🔄 저장된 기록 불러오기",
                        on_click=AppState.load_saved_activities,
                        color_scheme="blue",
                        size="2",
                        variant="outline",
                        margin_bottom="10px"
                    ),
                    rx.text(
                        "오늘 날짜의 저장된 데이터를 불러옵니다.",
                        color="gray.600",
                        size="2",
                        margin_bottom="10px"
                    ),
                    spacing="2",
                    padding="15px",
                    border="1px solid",
                    border_color="gray.300",
                    border_radius="8px",
                    margin_bottom="20px"
                ),
            ),

            # 4. 재시작 버튼
            rx.button(
                "다시 시작하기",
                # 홈 또는 인트로 페이지로 돌아갑니다.
                on_click=rx.redirect("/intro"), 
                color_scheme="gray",
                size="2"
            ),
            
            spacing="5",
            align="center",
            padding="50px"
        ),
        width="100%",
        min_height="100vh"
    )