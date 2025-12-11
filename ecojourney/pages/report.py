# report.py

import reflex as rx
from ..states import AppState
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
            
            # 2. 총 배출량 및 절약량
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "총 배출량 (kg CO2e):", 
                        font_weight="bold",
                        size="4"
                    ),
                    rx.text(
                        AppState.total_carbon_emission, 
                        size="8", 
                        color="blue.700"
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.cond(
                    AppState.total_saved_emission > 0,
                    rx.vstack(
                        rx.text(
                            "절약한 탄소 (kg CO2e):", 
                            font_weight="bold",
                            size="4"
                        ),
                        rx.text(
                            AppState.total_saved_emission, 
                            size="8", 
                            color="green.700"
                        ),
                        rx.text(
                            f"절약 금액: {AppState.saved_money}원",
                            size="3",
                            color="green.600"
                        ),
                        spacing="1",
                        align="center",
                    ),
                    rx.fragment(),
                ),
                spacing="8",
                justify="center",
                width="100%",
            ),
            
            # 3. 상세 내역 (데이터 개수 확인)
            rx.text(
                f"총 활동 기록 수: {AppState.all_activities.length()}",
                color="gray.600"
            ),
            
            rx.divider(margin_y="20px"),
            
            # 4. 상세 계산 내역 표시 및 도넛 차트
            rx.cond(
                AppState.is_report_calculated & (AppState.calculation_details.length() > 0),
                rx.hstack(
                    # 상세 계산 내역
                    rx.box(
                        rx.vstack(
                            rx.heading("📋 상세 계산 내역", size="5", margin_bottom="10px"),
                            rx.foreach(
                                AppState.calculation_details,
                                lambda detail: rx.vstack(
                                    # 카테고리 및 활동 유형
                                    rx.hstack(
                                        rx.text(detail["category"], font_weight="bold", size="3"),
                                        rx.text(" - ", font_weight="bold", size="3"),
                                        rx.text(
                                            detail["activity_type"], 
                                            font_weight="bold", 
                                            size="3",
                                            overflow="hidden",
                                            text_overflow="ellipsis",
                                            white_space="nowrap",
                                            max_width="100%",
                                        ),
                                        rx.cond(
                                            detail.get("sub_category", "") != "",
                                            rx.hstack(
                                                rx.text(" (", size="2", color="gray.500"),
                                                rx.text(
                                                    detail["sub_category"],
                                                    size="2",
                                                    color="gray.500",
                                                    font_weight="bold",
                                                ),
                                                rx.text(")", size="2", color="gray.500"),
                                                spacing="0",
                                            ),
                                            rx.fragment(),
                                        ),
                                        spacing="0",
                                        width="100%",
                                        align="start",
                                        flex_wrap="wrap",
                                    ),
                                    # 값 및 배출량
                                    rx.hstack(
                                        rx.text(detail["value"], color="gray.600", size="3"),
                                        rx.text(detail["unit"], color="gray.600", size="3"),
                                        rx.text(" = ", color="gray.600", size="3"),
                                        rx.text(detail["emission"], color="blue.700", font_weight="bold", size="3"),
                                        rx.text("kgCO2e", color="blue.700", font_weight="bold", size="3"),
                                        spacing="1",
                                        width="100%",
                                        flex_wrap="wrap",
                                    ),
                                    # 계산 방법
                                    rx.hstack(
                                        rx.text("(", color="green.600", size="2"),
                                        rx.text(
                                            detail["method"], 
                                            color="green.600", 
                                            size="2",
                                            overflow="hidden",
                                            text_overflow="ellipsis",
                                            white_space="nowrap",
                                            max_width="100%",
                                        ),
                                        rx.text(")", color="green.600", size="2"),
                                        spacing="0",
                                        width="100%",
                                    ),
                                    spacing="1",
                                    margin_bottom="10px",
                                    padding="10px",
                                    border="1px solid",
                                    border_color="gray.200",
                                    border_radius="6px",
                                    width="100%",
                                    align="start",
                                )
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        padding="20px",
                        border="1px solid",
                        border_color="gray.300",
                        border_radius="8px",
                        width="50%",
                        margin_right="10px",
                        overflow="hidden",
                    ),
                    
                    # 도넛 차트 (카테고리별 비율)
                    rx.cond(
                        AppState.category_emission_breakdown.length() > 0,
                        rx.box(
                            rx.vstack(
                                rx.heading("🍩 카테고리별 배출 비율", size="5", margin_bottom="15px"),
                                rx.cond(
                                    AppState.total_carbon_emission > 0,
                                    rx.vstack(
                                        # 도넛 차트 SVG
                                        rx.cond(
                                            AppState.donut_chart_svg != "",
                                            rx.box(
                                                rx.html(AppState.donut_chart_svg),
                                                width="200px",
                                                height="200px",
                                                display="flex",
                                                align_items="center",
                                                justify_content="center",
                                                margin_bottom="15px",
                                            ),
                                            rx.box(
                                                rx.text("차트 생성 중...", color="gray.400", size="3"),
                                                width="200px",
                                                height="200px",
                                                display="flex",
                                                align_items="center",
                                                justify_content="center",
                                                margin_bottom="15px",
                                            ),
                                        ),
                                        # 범례 및 상세 정보
                                        rx.vstack(
                                            rx.foreach(
                                                AppState.category_emission_list,
                                                lambda item: rx.hstack(
                                                    rx.box(
                                                        width="20px",
                                                        height="20px",
                                                        border_radius="4px",
                                                        background=item["color"],
                                                    ),
                                                    rx.vstack(
                                                        rx.hstack(
                                                            rx.text(
                                                                item["category"],
                                                                font_weight="bold",
                                                                size="3",
                                                                color="gray.800",
                                                            ),
                                                            rx.text(
                                                                f"{item['percentage']:.1f}%",
                                                                size="2",
                                                                color="gray.600",
                                                            ),
                                                            justify="between",
                                                            width="100%",
                                                        ),
                                                        rx.text(
                                                            f"{item['emission']:.2f}kg",
                                                            size="2",
                                                            color="gray.600",
                                                        ),
                                                        spacing="1",
                                                        width="100%",
                                                    ),
                                                    spacing="3",
                                                    width="100%",
                                                    margin_bottom="10px",
                                                ),
                                            ),
                                            spacing="2",
                                            align="start",
                                            width="100%",
                                        ),
                                        spacing="2",
                                        align="center",
                                    ),
                                    rx.text("데이터 없음", color="gray.400", size="3"),
                                ),
                                spacing="2",
                            ),
                            padding="20px",
                            border="1px solid",
                            border_color="gray.300",
                            border_radius="12px",
                            width="50%",
                            margin_left="10px",
                        ),
                        rx.fragment(),
                    ),
                    spacing="4",
                    width="100%",
                    align="start",
                    margin_bottom="20px",
                ),
            ),
            
            rx.divider(margin_y="20px"),
            
            # 절약량 및 포인트 획득 내역
            rx.cond(
                AppState.is_report_calculated,
                rx.box(
                    rx.vstack(
                        rx.heading("🌱 탄소 절약 및 포인트 획득 내역", size="6", margin_bottom="15px"),
                        
                        # 자전거/걷기 절약량
                        rx.cond(
                            AppState.total_saved_emission > 0,
                            rx.vstack(
                                rx.text(
                                    f"자전거/걷기를 사용하여 총 {AppState.total_saved_emission}kg의 탄소를 절약했습니다!",
                                    size="4",
                                    color="green.700",
                                    margin_bottom="10px",
                                ),
                                rx.foreach(
                                    AppState.savings_details,
                                    lambda item: rx.hstack(
                                        rx.text(
                                            f"• {item['activity_type']} {item['distance_km']}km",
                                            size="3",
                                            color="gray.700",
                                        ),
                                        rx.text(
                                            f"→ {item['saved_emission']}kg 절약 ({item['saved_money']}원)",
                                            size="3",
                                            color="green.600",
                                            font_weight="bold",
                                        ),
                                        spacing="2",
                                        width="100%",
                                    ),
                                ),
                                spacing="2",
                                margin_bottom="15px",
                            ),
                            rx.fragment(),
                        ),
                        
                        # 빈티지 제품 정보
                        rx.cond(
                            AppState.points_breakdown.get('빈티지', 0) > 0,
                            rx.vstack(
                                rx.text(
                                    f"빈티지 제품 사용: {AppState.points_breakdown.get('빈티지', 0)}점",
                                    size="3",
                                    color="purple.600",
                                    font_weight="bold",
                                    margin_bottom="5px",
                                ),
                                rx.foreach(
                                    AppState.all_activities,
                                    lambda act: rx.cond(
                                        (act.get("category", "") == "의류") & (act.get("sub_category", "") == "빈티지"),
                                        rx.hstack(
                                            rx.text(
                                                "• ",
                                                size="3",
                                                color="gray.700",
                                            ),
                                            rx.text(
                                                act.get('activity_type', ''),
                                                size="3",
                                                color="gray.700",
                                            ),
                                            rx.text(
                                                " 빈티지 ",
                                                size="3",
                                                color="gray.700",
                                            ),
                                            rx.text(
                                                act.get('value', 0),
                                                size="3",
                                                color="gray.700",
                                            ),
                                            rx.text(
                                                "개 (10점/개)",
                                                size="3",
                                                color="purple.600",
                                            ),
                                            spacing="1",
                                            width="100%",
                                            flex_wrap="wrap",
                                        ),
                                        rx.fragment(),
                                    ),
                                ),
                                spacing="2",
                                margin_bottom="15px",
                            ),
                            rx.fragment(),
                        ),
                        
                        # 평균 대비 낮은 배출량 포인트
                        rx.cond(
                            AppState.points_breakdown.get('평균 대비', 0) > 0,
                            rx.text(
                                f"평균 대비 낮은 배출량: {AppState.points_breakdown.get('평균 대비', 0)}점",
                                size="3",
                                color="blue.600",
                                font_weight="bold",
                                margin_bottom="15px",
                            ),
                            rx.fragment(),
                        ),
                        
                        # 총 지급 포인트
                        rx.cond(
                            AppState.total_points_earned > 0,
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "💰 총 지급 포인트",
                                        size="4",
                                        color="yellow.700",
                                        font_weight="bold",
                                        margin_bottom="5px",
                                    ),
                                    rx.text(
                                        f"{AppState.total_points_earned}점",
                                        size="7",
                                        color="yellow.600",
                                        font_weight="bold",
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                padding="15px",
                                border="2px solid",
                                border_color="yellow.400",
                                border_radius="12px",
                                background="yellow.50",
                                width="100%",
                                margin_top="10px",
                            ),
                            rx.fragment(),
                        ),
                        
                        spacing="2",
                    ),
                    padding="20px",
                    border="1px solid",
                    border_color="green.300",
                    border_radius="12px",
                    background="green.50",
                    margin_bottom="20px",
                    width="100%",
                ),
                rx.fragment(),
            ),
            
            rx.divider(margin_y="20px"),
            
            # 총 평균 비교만 표시
            rx.cond(
                AppState.is_report_calculated & AppState.total_average_comparison.contains('user'),
                rx.vstack(
                    rx.heading("📊 총 배출량 평균 비교", size="6", margin_bottom="20px"),
                    
                    # 총 평균 vs 내 배출량 비교
                    rx.box(
                        rx.vstack(
                            rx.heading("📈 평균 vs 내 배출량", size="5", margin_bottom="15px"),
                            rx.text("(단위: kgCO₂e)", size="2", color="gray.600", margin_bottom="10px"),
                            
                            # 비교 정보
                            rx.vstack(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("한국인 평균", size="3", color="gray.700", font_weight="bold"),
                                        rx.text(
                                            AppState.total_average_comparison.get('average_str', "0.00 kgCO₂e"),
                                            size="5",
                                            color="blue.700",
                                            font_weight="bold",
                                        ),
                                        spacing="1",
                                        align="center",
                                    ),
                                    rx.text("vs", size="4", color="gray.500", margin_x="20px"),
                                    rx.vstack(
                                        rx.text("내 배출량", size="3", color="gray.700", font_weight="bold"),
                                        rx.text(
                                            AppState.total_average_comparison.get('user_str', "0.00 kgCO₂e"),
                                            size="5",
                                            color=rx.cond(
                                                AppState.total_average_comparison.get('is_better', False),
                                                "green.700",
                                                "red.700"
                                            ),
                                            font_weight="bold",
                                        ),
                                        spacing="1",
                                        align="center",
                                    ),
                                    spacing="4",
                                    justify="center",
                                    align="center",
                                    width="100%",
                                ),
                                
                                rx.divider(margin_y="15px"),
                                
                                # 차이 표시
                                rx.vstack(
                                    rx.text(
                                        rx.cond(
                                            AppState.total_average_comparison.get('is_better', False),
                                            "✅ 평균보다 낮습니다!",
                                            "⚠️ 평균보다 높습니다."
                                        ),
                                        size="4",
                                        color=rx.cond(
                                            AppState.total_average_comparison.get('is_better', False),
                                            "green.700",
                                            "red.700"
                                        ),
                                        font_weight="bold",
                                    ),
                                    rx.text(
                                        AppState.total_average_comparison.get('abs_difference_str', "차이: 0.00 kgCO₂e"),
                                        size="3",
                                        color="gray.600",
                                    ),
                                    rx.text(
                                        AppState.total_average_comparison.get('percentage_str', "(0.0%)"),
                                        size="3",
                                        color="gray.600",
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                
                                spacing="3",
                                align="center",
                                width="100%",
                            ),
                            
                            spacing="3",
                            align="center",
                            width="100%",
                        ),
                        padding="20px",
                        border="1px solid",
                        border_color="gray.300",
                        border_radius="12px",
                        width="100%",
                        max_width="500px",
                        margin="0 auto",
                    ),
                    
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                rx.fragment(),
            ),
            
            rx.divider(margin_y="20px"),
            
            # AI 분석 결과 및 대안 추천
            rx.cond(
                AppState.is_report_calculated,
                rx.vstack(
                    rx.heading("🤖 AI 분석 및 대안 추천", size="6", margin_bottom="20px"),
                    
                    rx.cond(
                        AppState.is_loading_ai,
                        rx.vstack(
                            rx.text("AI 분석 중...", color="blue.600", size="4"),
                            rx.progress(is_indeterminate=True, width="100%", max_width="400px"),
                            spacing="3",
                            align="center",
                        ),
                        rx.cond(
                            AppState.ai_analysis_result != "",
                            rx.vstack(
                                # AI 분석 결과
                                rx.box(
                                    rx.vstack(
                                        rx.heading("📝 분석 결과", size="5", margin_bottom="10px"),
                                        rx.text(
                                            AppState.ai_analysis_result,
                                            size="3",
                                            line_height="1.8",
                                            white_space="pre-wrap",
                                        ),
                                        spacing="2",
                                    ),
                                    padding="20px",
                                    border="1px solid",
                                    border_color="blue.300",
                                    border_radius="12px",
                                    background="blue.50",
                                    margin_bottom="20px",
                                    width="100%",
                                    max_width="800px",
                                ),
                                
                                # 구체적 제안
                                rx.box(
                                    rx.vstack(
                                        rx.heading("💡 탄소 저감 제안", size="5", margin_bottom="10px"),
                                        rx.foreach(
                                            AppState.ai_suggestions,
                                            lambda suggestion: rx.hstack(
                                                rx.text("• ", color="green.600", font_weight="bold"),
                                                rx.text(
                                                    suggestion,
                                                    size="3",
                                                    line_height="1.8",
                                                ),
                                                spacing="2",
                                                width="100%",
                                                margin_bottom="8px",
                                            ),
                                        ),
                                        spacing="2",
                                    ),
                                    padding="20px",
                                    border="1px solid",
                                    border_color="green.300",
                                    border_radius="12px",
                                    background="green.50",
                                    margin_bottom="20px",
                                    width="100%",
                                    max_width="800px",
                                ),
                                
                                spacing="3",
                                align="center",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("AI 분석을 시작하려면 아래 버튼을 클릭하세요.", color="gray.600", size="3"),
                                rx.button(
                                    "🤖 AI 분석 시작하기",
                                    on_click=AppState.generate_ai_analysis,
                                    color_scheme="purple",
                                    size="3",
                                    margin_top="10px",
                                ),
                                spacing="2",
                                align="center",
                            ),
                        ),
                    ),
                    
                    spacing="3",
                    align="center",
                    width="100%",
                ),
            ),
            
            rx.divider(margin_y="20px"),
            
            # 저장 버튼 및 메시지 (로그인한 경우에만 표시)
            rx.cond(
                AppState.is_logged_in,
                rx.vstack(
                    rx.cond(
                        AppState.is_saving,
                        rx.vstack(
                            rx.text("💾 저장 중...", color="blue.600", size="4"),
                            rx.progress(is_indeterminate=True, width="100%", max_width="300px"),
                            spacing="2",
                        ),
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