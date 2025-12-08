# mypage.py - 마이페이지

import reflex as rx
from ecojourney.state import AppState
from typing import Dict, Any

def header() -> rx.Component:
    """공통 헤더"""
    return rx.box(
        rx.hstack(
            rx.button(
                "EcoJourney",
                on_click=rx.redirect("/"),
                background_color="transparent",
                color="white",
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
                        "대결",
                        on_click=rx.redirect("/battle"),
                        background_color="rgba(255, 255, 255, 0.2)",
                        color="white",
                        border="1px solid rgba(255, 255, 255, 0.3)",
                        border_radius="20px",
                        padding="8px 20px",
                        _hover={
                            "background_color": "rgba(255, 255, 255, 0.3)",
                        },
                    ),
                    rx.button(
                        "랭킹",
                        on_click=rx.redirect("/ranking"),
                        background_color="rgba(255, 255, 255, 0.2)",
                        color="white",
                        border="1px solid rgba(255, 255, 255, 0.3)",
                        border_radius="20px",
                        padding="8px 20px",
                        _hover={
                            "background_color": "rgba(255, 255, 255, 0.3)",
                        },
                    ),
                    rx.text(
                        f"{AppState.current_user_id}님",
                        color="white",
                        font_size="1em",
                        margin_right="10px",
                    ),
                    rx.button(
                        "로그아웃",
                        on_click=AppState.logout,
                        background_color="rgba(255, 255, 255, 0.2)",
                        color="white",
                        border="1px solid rgba(255, 255, 255, 0.3)",
                        border_radius="20px",
                        padding="8px 20px",
                        _hover={
                            "background_color": "rgba(255, 255, 255, 0.3)",
                        },
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.button(
                    "로그인",
                    on_click=rx.redirect("/auth"),
                    background_color="rgba(255, 255, 255, 0.2)",
                    color="white",
                    border="1px solid rgba(255, 255, 255, 0.3)",
                    border_radius="20px",
                    padding="8px 20px",
                    _hover={
                        "background_color": "rgba(255, 255, 255, 0.3)",
                    },
                ),
            ),
            justify="between",
            align="center",
            padding="1em 2em",
        ),
        width="100%",
        position="relative",
        z_index="10",
        background_color="transparent",
    )

def mypage_page() -> rx.Component:
    """마이페이지 컴포넌트"""
    # 페이지 로드 시 통계 데이터 로드
    return rx.center(
        rx.vstack(
            header(),
            
            rx.cond(
                AppState.is_logged_in,
                rx.vstack(
                    # 페이지 제목
                    rx.heading("📊 마이페이지", size="8", color="white", margin_bottom="30px"),
                    
                    # 포인트 섹션
                    rx.box(
                        rx.vstack(
                            rx.heading("💰 내 포인트", size="6", color="white", margin_bottom="10px"),
                            rx.text(
                                f"{AppState.current_user_points:,}점",
                                size="9",
                                color="yellow.300",
                                font_weight="bold",
                            ),
                            rx.text(
                                f"단과대: {AppState.current_user_college}",
                                size="3",
                                color="gray.300",
                                margin_top="10px",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        padding="30px",
                        border_radius="16px",
                        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        width="100%",
                        max_width="600px",
                        margin_bottom="30px",
                    ),
                    
                    # 포인트 획득 내역 섹션
                    rx.box(
                        rx.vstack(
                            rx.heading("📅 포인트 획득 내역", size="6", color="white", margin_bottom="20px"),
                            rx.cond(
                                AppState.points_log.length() > 0,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.points_log,
                                        lambda log: rx.hstack(
                                            rx.text(
                                                log["date"],
                                                color="white",
                                                size="4",
                                                font_weight="bold",
                                                width="150px",
                                            ),
                                            rx.text(
                                                f"+{log['points']} 포인트",
                                                color="yellow.300",
                                                size="4",
                                                font_weight="bold",
                                            ),
                                            spacing="4",
                                            justify="between",
                                            width="100%",
                                            padding="10px",
                                            border_radius="8px",
                                            background="rgba(255, 255, 255, 0.1)",
                                            margin_bottom="8px",
                                        ),
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                rx.text(
                                    "아직 획득한 포인트가 없습니다.",
                                    color="gray.400",
                                    size="3",
                                ),
                            ),
                            spacing="3",
                        ),
                        padding="30px",
                        border_radius="16px",
                        background="rgba(0, 0, 0, 0.3)",
                        width="100%",
                        max_width="600px",
                        margin_bottom="30px",
                    ),
                    
                    # 챌린지 진행률 섹션
                    rx.box(
                        rx.vstack(
                            rx.heading("🎯 참여 중인 챌린지", size="6", color="white", margin_bottom="20px"),
                            rx.cond(
                                AppState.user_challenge_progress.length() > 0,
                                rx.foreach(
                                    AppState.user_challenge_progress,
                                    lambda progress: rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.text(
                                                    progress["title"],
                                                    font_weight="bold",
                                                    color="white",
                                                    size="4",
                                                ),
                                                rx.cond(
                                                    progress["is_completed"],
                                                    rx.badge("완료", color_scheme="green"),
                                                    rx.badge("진행중", color_scheme="blue"),
                                                ),
                                                justify="between",
                                                width="100%",
                                            ),
                                            rx.text(
                                                f"{progress['current_value']} / {progress['goal_value']}",
                                                color="gray.300",
                                                size="3",
                                            ),
                                            rx.progress(
                                                value=progress["progress_percent"],
                                                width="100%",
                                                color_scheme="green",
                                                margin_top="10px",
                                            ),
                                            rx.text(
                                                f"보상: {progress['reward_points']}점",
                                                color="yellow.300",
                                                size="2",
                                                margin_top="5px",
                                            ),
                                            spacing="2",
                                        ),
                                        padding="20px",
                                        border_radius="12px",
                                        background="rgba(255, 255, 255, 0.1)",
                                        border="1px solid rgba(255, 255, 255, 0.2)",
                                        margin_bottom="15px",
                                        width="100%",
                                    ),
                                ),
                                rx.text(
                                    "참여 중인 챌린지가 없습니다.",
                                    color="gray.400",
                                    size="3",
                                ),
                            ),
                            spacing="3",
                        ),
                        padding="30px",
                        border_radius="16px",
                        background="rgba(0, 0, 0, 0.3)",
                        width="100%",
                        max_width="600px",
                        margin_bottom="30px",
                    ),
                    
                    # 탄소 배출 통계 섹션
                    rx.box(
                        rx.vstack(
                            rx.heading("📈 탄소 배출 통계", size="6", color="white", margin_bottom="20px"),
                            rx.cond(
                                AppState.carbon_total_logs > 0,
                                rx.vstack(
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("총 기록일", color="gray.300", size="2"),
                                            rx.text(
                                                f"{AppState.carbon_total_logs}일",
                                                color="white",
                                                size="5",
                                                font_weight="bold",
                                            ),
                                            align="center",
                                            spacing="1",
                                        ),
                                        rx.vstack(
                                            rx.text("총 배출량", color="gray.300", size="2"),
                                            rx.text(
                                                f"{AppState.carbon_total_emission}kg",
                                                color="white",
                                                size="5",
                                                font_weight="bold",
                                            ),
                                            align="center",
                                            spacing="1",
                                        ),
                                        rx.vstack(
                                            rx.text("일평균", color="gray.300", size="2"),
                                            rx.text(
                                                f"{AppState.carbon_average_daily_emission}kg",
                                                color="white",
                                                size="5",
                                                font_weight="bold",
                                            ),
                                            align="center",
                                            spacing="1",
                                        ),
                                        rx.vstack(
                                            rx.text("총 활동 수", color="gray.300", size="2"),
                                            rx.text(
                                                f"{AppState.carbon_total_activities}개",
                                                color="white",
                                                size="5",
                                                font_weight="bold",
                                            ),
                                            align="center",
                                            spacing="1",
                                        ),
                                        spacing="6",
                                        justify="between",
                                        width="100%",
                                    ),
                                    rx.divider(margin_y="20px"),
                                    rx.text("카테고리별 활동 수", color="gray.300", size="3", margin_bottom="10px"),
                                    rx.vstack(
                                    rx.foreach(
                                        AppState.carbon_category_breakdown,
                                        lambda item: rx.hstack(
                                            rx.text(
                                                item["name"],
                                                color="white",
                                                size="3",
                                                width="100px",
                                            ),
                                            rx.progress(
                                                value=item["percent"],
                                                width="200px",
                                                color_scheme="blue",
                                            ),
                                            rx.text(
                                                f"{item['count']}회",
                                                color="gray.300",
                                                size="2",
                                            ),
                                            spacing="3",
                                            width="100%",
                                        ),
                                    ),
                                        spacing="2",
                                        width="100%",
                                    ),
                                    spacing="3",
                                ),
                                rx.text(
                                    "아직 기록된 데이터가 없습니다.",
                                    color="gray.400",
                                    size="3",
                                ),
                            ),
                            spacing="3",
                        ),
                        padding="30px",
                        border_radius="16px",
                        background="rgba(0, 0, 0, 0.3)",
                        width="100%",
                        max_width="600px",
                        margin_bottom="30px",
                    ),
                    
                    # 새로고침 버튼
                    rx.button(
                        "🔄 통계 새로고침",
                        on_click=AppState.load_mypage_data,
                        color_scheme="blue",
                        size="3",
                        margin_bottom="20px",
                    ),
                    
                    spacing="4",
                    align="center",
                    width="100%",
                    max_width="800px",
                    padding="40px",
                ),
                rx.vstack(
                    rx.heading("로그인이 필요합니다", size="6", color="white"),
                    rx.button(
                        "로그인하기",
                        on_click=rx.redirect("/auth"),
                        color_scheme="green",
                        size="3",
                        margin_top="20px",
                    ),
                    spacing="4",
                    align="center",
                ),
            ),
            
            spacing="4",
            align="center",
            width="100%",
            min_height="100vh",
            padding="20px",
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        ),
        width="100%",
        min_height="100vh",
    )

