import reflex as rx
from ..states import AppState

def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.button(
                "ECOJOURNEY",
                on_click=rx.redirect("/"),
                background_color="transparent",
                color="#FFFFFF",
                font_size="1.5em",
                font_weight="bold",
                padding="0",
                border="none",
                border_radius="8px",
                cursor="pointer",
            ),
            rx.cond(
                AppState.is_logged_in,
                rx.hstack(
                    rx.button(
                        "챌린지",
                        on_click=rx.redirect("/info"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={
                            "border": "1px solid #FFFFFF",
                        },
                    ),
                    rx.button(
                        "배틀",
                        on_click=rx.redirect("/battle"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={
                            "border": "1px solid #FFFFFF",
                        },
                    ),
                    rx.button(
                        "랭킹",
                        on_click=rx.redirect("/ranking"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={
                            "border": "1px solid #FFFFFF",
                        },
                    ),
                    rx.button(
                        "마이페이지",
                        on_click=rx.redirect("/mypage"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={
                            "border": "1px solid #FFFFFF",
                        },
                    ),
                    rx.text(
                        f"{AppState.current_user_id}님",
                        color="#FFFFFF",
                        font_size="1em",
                        margin_right="10px",
                    ),
                    rx.button(
                        "로그아웃",
                        on_click=AppState.logout,
                        background_color="#FFFFFF",
                        color="#4DAB75",
                        border="1px solid #4DAB75",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={
                            "background_color": "rgba(255, 255, 255, 0.9)",
                        },
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.button(
                    "로그인",
                    on_click=rx.redirect("/auth"),
                    background_color="#FFFFFF",
                    color="#4DAB75",
                    border="1px solid #4DAB75",
                    border_radius="25px",
                    padding="8px 20px",
                    font_weight="500",
                    _hover={
                        "background_color": "rgba(255, 255, 255, 0.9)",
                    },
                ),
            ),
            justify="between",
            align="center",
            padding="1.5em 3em",
        ),
        width="100%",
        position="relative",
        z_index="10",
        background_color="#4DAB75",
        border_bottom="1px solid rgba(255, 255, 255, 0.1)",
    )

def report_page() -> rx.Component:
    """
    최종 탄소 발자국 리포트 페이지 컴포넌트입니다.
    4분할 레이아웃: 막대그래프, 파이차트, 포인트 내역, AI 솔루션
    """
    return rx.box(
        rx.vstack(
            # 헤더
            header(),

            # 메인 컨텐츠 - 4분할 그리드
            rx.cond(
                AppState.is_report_calculated,
                rx.box(
                    rx.heading(
                        "Your Carbon Footprint Report",
                        size="9",
                        width="100%",
                        text_align="center",
                        color="#333333",
                        font_weight="700",
                        letter_spacing="-0.02em",
                        padding_bottom="25px",
                        padding_top="30px",
                    ),
                    rx.grid(
                        # 왼쪽 상단: 막대 그래프 (평균 비교)
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "평균 대비 배출량",
                                    font_weight="700",
                                    size="5",
                                    color="#333333",
                                ),

                                # 막대 그래프 + 비교 문구를 가로로 배치
                                rx.hstack(
                                    # 왼쪽: 막대 그래프
                                    rx.hstack(
                                        # 한국인 평균 막대
                                        rx.vstack(
                                            rx.box(
                                                rx.tooltip(
                                                    rx.box(
                                                        width="50px",
                                                        height=f"{AppState.average_bar_height}px",
                                                        background="linear-gradient(180deg, #93c5fd 0%, #60a5fa 100%)",
                                                        border_radius="8px 8px 0 0",
                                                        transition="height 0.5s ease",
                                                        _hover={"opacity": "0.8"},
                                                    ),
                                                    content=f"평균 배출량: {AppState.total_average_comparison.get('average', 0):.2f} kgCO₂e",
                                                ),
                                                display="flex",
                                                align_items="flex-end",
                                                height="120px",
                                            ),
                                            rx.text("평균 배출량", size="1", color="#666666", margin_top="6px"),
                                            rx.text(
                                                f"{AppState.total_average_comparison.get('average', 0):.1f}kg",
                                                size="2",
                                                font_weight="bold",
                                                color="#93c5fd",
                                            ),
                                            align="center",
                                            spacing="1",
                                        ),

                                        # 내 배출량 막대
                                        rx.vstack(
                                            rx.box(
                                                rx.tooltip(
                                                    rx.box(
                                                        width="50px",
                                                        height=f"{AppState.user_bar_height}px",
                                                        background=rx.cond(
                                                            AppState.total_average_comparison.get('is_better', False),
                                                            "linear-gradient(180deg, #6ee7b7 0%, #34d399 100%)",
                                                            "linear-gradient(180deg, #fca5a5 0%, #f87171 100%)",
                                                        ),
                                                        border_radius="8px 8px 0 0",
                                                        transition="height 0.5s ease",
                                                        _hover={"opacity": "0.8"},
                                                    ),
                                                    content=f"내 배출량: {AppState.total_average_comparison.get('user', 0):.2f} kgCO₂e",
                                                ),
                                                display="flex",
                                                align_items="flex-end",
                                                height="120px",
                                            ),
                                            rx.text("내 배출량", size="1", color="#666666", margin_top="6px"),
                                            rx.text(
                                                f"{AppState.total_average_comparison.get('user', 0):.1f}kg",
                                                size="2",
                                                font_weight="bold",
                                                color=rx.cond(
                                                    AppState.total_average_comparison.get('is_better', False),
                                                    "#6ee7b7",
                                                    "#fca5a5",
                                                ),
                                            ),
                                            align="center",
                                            spacing="1",
                                        ),

                                        spacing="4",
                                        align="end",
                                    ),

                                    # 오른쪽: 비교 결과 문구
                                    rx.box(
                                        rx.vstack(
                                            rx.text(
                                                rx.cond(
                                                    AppState.total_average_comparison.get('is_better', False),
                                                    "✅ 평균보다",
                                                    "⚠️ 평균보다",
                                                ),
                                                size="2",
                                                color="#666666",
                                                font_weight="500",
                                            ),
                                            rx.text(
                                                f"{AppState.total_average_comparison.get('abs_difference', 0):.1f}kg",
                                                size="5",
                                                font_weight="bold",
                                                color=rx.cond(
                                                    AppState.total_average_comparison.get('is_better', False),
                                                    "#6ee7b7",
                                                    "#fca5a5",
                                                ),
                                            ),
                                            rx.text(
                                                rx.cond(
                                                    AppState.total_average_comparison.get('is_better', False),
                                                    "적게 배출했어요! 🎉",
                                                    "더 배출했어요 😅",
                                                ),
                                                size="2",
                                                color="#999999",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        padding="16px 20px",
                                        background=rx.cond(
                                            AppState.total_average_comparison.get('is_better', False),
                                            "rgba(110, 231, 183, 0.15)",
                                            "rgba(252, 165, 165, 0.15)",
                                        ),
                                        border_radius="16px",
                                        border="2px solid",
                                        border_color=rx.cond(
                                            AppState.total_average_comparison.get('is_better', False),
                                            "rgba(110, 231, 183, 0.3)",
                                            "rgba(252, 165, 165, 0.3)",
                                        ),
                                    ),

                                    spacing="6",
                                    align="center",
                                    justify="center",
                                    width="100%",
                                    padding_top="20px",
                                ),

                                spacing="3",
                                align="center",
                                width="100%",
                            ),
                            padding="24px",
                            background="#FFFFFF",
                            border_radius="20px",
                            box_shadow="0 4px 20px rgba(0, 0, 0, 0.1)",
                            border="1px solid #E0E0E0",
                            height="100%",
                        ),

                        # 오른쪽 상단: 파이 차트 (카테고리별)
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "카테고리별 배출량",
                                    font_weight="700",
                                    size="5",
                                    color="#333333",
                                ),

                                rx.cond(
                                    AppState.category_emission_list.length() > 0,
                                    rx.hstack(
                                        # 파이 차트 SVG
                                        rx.box(
                                            rx.cond(
                                                AppState.donut_chart_svg != "",
                                                rx.html(AppState.donut_chart_svg),
                                                rx.text("차트 생성 중...", color="#999999", size="2"),
                                            ),
                                            width="140px",
                                            height="140px",
                                            display="flex",
                                            align_items="center",
                                            justify_content="center",
                                        ),

                                        # 범례
                                        rx.vstack(
                                            rx.foreach(
                                                AppState.category_emission_list,
                                                lambda item: rx.tooltip(
                                                    rx.hstack(
                                                        rx.box(
                                                            width="12px",
                                                            height="12px",
                                                            border_radius="3px",
                                                            background=item["color"],
                                                        ),
                                                        rx.text(
                                                            item["category"],
                                                            size="2",
                                                            color="#333333",
                                                        ),
                                                        rx.text(
                                                            f"{item['percentage']:.0f}%",
                                                            size="2",
                                                            color="#666666",
                                                            font_weight="600",
                                                        ),
                                                        spacing="2",
                                                        align="center",
                                                        padding="4px 8px",
                                                        border_radius="6px",
                                                        _hover={"background": "rgba(77, 171, 117, 0.1)"},
                                                        cursor="pointer",
                                                    ),
                                                    content=f"{item['category']}: {item['emission']:.2f}kgCO₂e ({item['percentage']:.1f}%)",
                                                ),
                                            ),
                                            spacing="1",
                                            align="start",
                                        ),

                                        spacing="4",
                                        align="center",
                                        justify="center",
                                        width="100%",
                                        padding_top="20px",
                                    ),
                                    rx.text("데이터 없음", color="#999999", size="3"),
                                ),

                                spacing="3",
                                align="center",
                                width="100%",
                                height="100%",
                            ),
                            padding="24px",
                            background="#FFFFFF",
                            border_radius="20px",
                            box_shadow="0 4px 20px rgba(0, 0, 0, 0.1)",
                            border="1px solid #E0E0E0",
                            height="100%",
                        ),

                        # 왼쪽 하단: 포인트 획득 내역
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "포인트 획득 내역",
                                    font_weight="700",
                                    size="5",
                                    color="#333333",
                                ),

                                rx.box(
                                    rx.vstack(
                                        # 총 포인트
                                        rx.hstack(
                                            rx.text("총 획득 포인트", size="2", color="#666666"),
                                            rx.spacer(),
                                            rx.text(
                                                f"{AppState.total_points_earned}점",
                                                size="5",
                                                font_weight="bold",
                                                color="#fbbf24",
                                            ),
                                            width="100%",
                                            padding="12px",
                                            background="rgba(251, 191, 36, 0.15)",
                                            border_radius="12px",
                                            border="1px solid rgba(251, 191, 36, 0.3)",
                                        ),

                                        # 포인트 상세 내역
                                        rx.cond(
                                            AppState.total_saved_emission > 0,
                                            rx.hstack(
                                                rx.box(
                                                    rx.text("🚴", size="4"),
                                                    padding="8px",
                                                    background="rgba(110, 231, 183, 0.2)",
                                                    border_radius="8px",
                                                ),
                                                rx.vstack(
                                                    rx.text("자전거/걷기 절약", size="2", font_weight="600", color="#333333"),
                                                    rx.text(f"{AppState.total_saved_emission:.2f}kg 절약", size="1", color="#6ee7b7"),
                                                    spacing="0",
                                                    align="start",
                                                ),
                                                rx.spacer(),
                                                rx.text(f"+{AppState.saved_money}원", size="2", font_weight="bold", color="#6ee7b7"),
                                                width="100%",
                                                padding="10px",
                                                background="rgba(110, 231, 183, 0.1)",
                                                border_radius="10px",
                                                border="1px solid rgba(110, 231, 183, 0.2)",
                                                align="center",
                                            ),
                                        ),

                                        rx.cond(
                                            AppState.points_breakdown.get('빈티지', 0) > 0,
                                            rx.hstack(
                                                rx.box(
                                                    rx.text("👕", size="4"),
                                                    padding="8px",
                                                    background="rgba(196, 181, 253, 0.2)",
                                                    border_radius="8px",
                                                ),
                                                rx.vstack(
                                                    rx.text("빈티지 제품", size="2", font_weight="600", color="#333333"),
                                                    rx.text("환경 보호 실천", size="1", color="#c4b5fd"),
                                                    spacing="0",
                                                    align="start",
                                                ),
                                                rx.spacer(),
                                                rx.text(f"+{AppState.points_breakdown.get('빈티지', 0)}점", size="2", font_weight="bold", color="#c4b5fd"),
                                                width="100%",
                                                padding="10px",
                                                background="rgba(196, 181, 253, 0.1)",
                                                border_radius="10px",
                                                border="1px solid rgba(196, 181, 253, 0.2)",
                                                align="center",
                                            ),
                                        ),

                                        rx.cond(
                                            AppState.total_average_comparison.get('is_better', False),
                                            rx.hstack(
                                                rx.box(
                                                    rx.text("📉", size="4"),
                                                    padding="8px",
                                                    background="rgba(147, 197, 253, 0.2)",
                                                    border_radius="8px",
                                                ),
                                                rx.vstack(
                                                    rx.text("평균 이하 배출", size="2", font_weight="600", color="#333333"),
                                                    rx.text("우수한 탄소 관리", size="1", color="#93c5fd"),
                                                    spacing="0",
                                                    align="start",
                                                ),
                                                rx.spacer(),
                                                rx.text(f"+{AppState.points_breakdown.get('평균 대비', 0)}점", size="2", font_weight="bold", color="#93c5fd"),
                                                width="100%",
                                                padding="10px",
                                                background="rgba(147, 197, 253, 0.1)",
                                                border_radius="10px",
                                                border="1px solid rgba(147, 197, 253, 0.2)",
                                                align="center",
                                            ),
                                        ),

                                        spacing="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    overflow_y="auto",
                                    max_height="200px",
                                ),

                                spacing="3",
                                align="start",
                                width="100%",
                                height="100%",
                            ),
                            padding="24px",
                            background="#FFFFFF",
                            border_radius="20px",
                            box_shadow="0 4px 20px rgba(0, 0, 0, 0.1)",
                            border="1px solid #E0E0E0",
                            height="100%",
                        ),

                        # 오른쪽 하단: AI 솔루션
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "AI 솔루션",
                                    font_weight="700",
                                    size="5",
                                    color="#333333",
                                ),

                                rx.cond(
                                    AppState.is_loading_ai,
                                    rx.vstack(
                                        rx.spinner(size="3", color="#4DAB75"),
                                        rx.text("AI가 분석 중입니다...", color="#333333", size="2"),
                                        spacing="3",
                                        align="center",
                                        justify="center",
                                        padding="40px",
                                        width="100%",
                                    ),
                                    rx.cond(
                                        AppState.ai_analysis_result != "",
                                        rx.box(
                                            rx.vstack(
                                                # 분석 결과 카드
                                                rx.box(
                                                    rx.vstack(
                                                        rx.hstack(
                                                            rx.text("📝", size="3"),
                                                            rx.text("분석 결과", size="2", font_weight="600", color="#333333"),
                                                            rx.spacer(),
                                                            rx.button(
                                                                rx.cond(
                                                                    AppState.show_analysis_detail,
                                                                    "접기",
                                                                    "펼치기",
                                                                ),
                                                                on_click=AppState.toggle_analysis_detail,
                                                                size="1",
                                                                variant="ghost",
                                                                color="#4DAB75",
                                                            ),
                                                            width="100%",
                                                            align="center",
                                                        ),
                                                        rx.cond(
                                                            AppState.show_analysis_detail,
                                                            rx.text(
                                                                AppState.ai_analysis_result,
                                                                size="2",
                                                                color="#333333",
                                                                line_height="1.6",
                                                                white_space="pre-wrap",
                                                            ),
                                                            rx.text(
                                                                "클릭하여 상세 분석 결과를 확인하세요",
                                                                size="1",
                                                                color="#999999",
                                                            ),
                                                        ),
                                                        spacing="2",
                                                        width="100%",
                                                    ),
                                                    padding="12px",
                                                    background="rgba(147, 197, 253, 0.1)",
                                                    border_radius="12px",
                                                    border="1px solid rgba(147, 197, 253, 0.2)",
                                                    width="100%",
                                                    cursor="pointer",
                                                    on_click=AppState.toggle_analysis_detail,
                                                ),

                                                # 탄소 저감 제안 카드
                                                rx.cond(
                                                    AppState.ai_suggestions.length() > 0,
                                                    rx.box(
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("💡", size="3"),
                                                                rx.text("탄소 저감 제안", size="2", font_weight="600", color="#333333"),
                                                                rx.spacer(),
                                                                rx.button(
                                                                    rx.cond(
                                                                        AppState.show_suggestions_detail,
                                                                        "접기",
                                                                        "펼치기",
                                                                    ),
                                                                    on_click=AppState.toggle_suggestions_detail,
                                                                    size="1",
                                                                    variant="ghost",
                                                                    color="#4DAB75",
                                                                ),
                                                                width="100%",
                                                                align="center",
                                                            ),
                                                            rx.cond(
                                                                AppState.show_suggestions_detail,
                                                                rx.vstack(
                                                                    rx.foreach(
                                                                        AppState.ai_suggestions,
                                                                        lambda suggestion: rx.hstack(
                                                                            rx.text("•", color="#4DAB75", font_weight="bold"),
                                                                            rx.text(suggestion, size="2", color="#333333"),
                                                                            spacing="2",
                                                                            width="100%",
                                                                        ),
                                                                    ),
                                                                    spacing="1",
                                                                    width="100%",
                                                                ),
                                                                rx.text(
                                                                    f"{AppState.ai_suggestions.length()}개의 제안이 있습니다",
                                                                    size="1",
                                                                    color="#999999",
                                                                ),
                                                            ),
                                                            spacing="2",
                                                            width="100%",
                                                        ),
                                                        padding="12px",
                                                        background="rgba(110, 231, 183, 0.1)",
                                                        border_radius="12px",
                                                        border="1px solid rgba(110, 231, 183, 0.2)",
                                                        width="100%",
                                                        cursor="pointer",
                                                        on_click=AppState.toggle_suggestions_detail,
                                                    ),
                                                ),

                                                spacing="2",
                                                width="100%",
                                            ),
                                            width="100%",
                                            overflow_y="auto",
                                            max_height="220px",
                                        ),
                                        rx.vstack(
                                            rx.spinner(size="3", color="#4DAB75"),
                                            rx.text("AI 분석 준비 중...", size="2", color="#999999"),
                                            spacing="3",
                                            align="center",
                                            justify="center",
                                            padding="40px",
                                            width="100%",
                                        ),
                                    ),
                                ),

                                spacing="3",
                                align="start",
                                width="100%",
                                height="100%",
                            ),
                            padding="24px",
                            background="#FFFFFF",
                            border_radius="20px",
                            box_shadow="0 4px 20px rgba(0, 0, 0, 0.1)",
                            border="1px solid #E0E0E0",
                            height="100%",
                        ),

                        columns="2",
                        rows="2",
                        gap="16px",
                        width="100%",
                        height="calc(100vh - 180px)",
                    ),
                    padding="20px 40px",
                    width="100%",
                ),
                # 계산 중 로딩 상태
                rx.box(
                    rx.vstack(
                        rx.spinner(size="3", color="#4DAB75"),
                        rx.text("리포트를 생성하고 있습니다...", size="4", color="#333333", font_weight="600"),
                        rx.text("잠시만 기다려주세요", size="2", color="#666666"),
                        spacing="3",
                        align="center",
                        justify="center",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    height="calc(100vh - 100px)",
                    width="100%",
                )
            ),

            # 하단 버튼
            rx.hstack(
                rx.cond(
                    AppState.is_logged_in,
                    rx.cond(
                        AppState.is_saving,
                        rx.button(
                            "저장 중...",
                            is_disabled=True,
                            size="2",
                            background_color="rgba(217, 239, 222, 0.3)",
                            color="rgba(217, 239, 222, 0.5)",
                        ),
                        rx.button(
                            "저장하기",
                            on_click=AppState.save_carbon_log_to_db,
                            size="2",
                            is_disabled=~AppState.is_report_calculated,
                            background_color="#4DAB75",
                            color="#FFFFFF",
                            border_radius="25px",
                            padding="10px 28px",
                            font_weight="600",
                            cursor="pointer",
                            _hover={
                                "background_color": "#3d9a66",
                            },
                        ),
                    ),
                ),
                rx.button(
                    "처음으로",
                    on_click=rx.redirect("/intro"),
                    size="2",
                    background_color="transparent",
                    color="#4DAB75",
                    border="1px solid rgba(77, 171, 117, 0.3)",
                    border_radius="25px",
                    padding="10px 28px",
                    font_weight="600",
                    cursor="pointer",
                    _hover={
                        "background_color": "rgba(77, 171, 117, 0.05)",
                        "border": "1px solid #4DAB75",
                    },
                ),
                rx.cond(
                    AppState.save_message != "",
                    rx.text(
                        AppState.save_message,
                        size="2",
                        color=rx.cond(AppState.is_save_success, "#6ee7b7", "#fca5a5"),
                        font_weight="500",
                    ),
                ),
                spacing="3",
                padding="20px 40px",
                justify="center",
                width="100%",
                background_color="#FFFFFF",
                border_top="1px solid #E0E0E0",
            ),

            spacing="0",
            width="100%",
            min_height="100vh",
        ),
        background="#F8F9FA",
        width="100%",
        min_height="100vh",
        on_mount=AppState.on_report_page_load,  # 페이지 로드 시 자동 실행
    )
