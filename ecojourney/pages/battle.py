# battle.py - 단과대별 대결 페이지

import reflex as rx
from ecojourney.state import AppState


def battle_page() -> rx.Component:
    """단과대별 대결 페이지"""
    return rx.container(
        rx.vstack(
            rx.heading("🏆 단과대 대결", size="8", color="white", margin_bottom="20px"),
            
            # 현재 대결 정보
            rx.cond(
                AppState.current_battle != None,
                rx.vstack(
                    rx.card(
                        rx.vstack(
                            rx.heading("현재 대결", size="6", margin_bottom="15px"),
                            rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        AppState.current_battle["college_a"],
                                        size="5",
                                        weight="bold",
                                        color="blue.300",
                                    ),
                                    rx.text(
                                        f"총 포인트: {AppState.current_battle['score_a']}",
                                        size="4",
                                        color="white",
                                    ),
                                    rx.text(
                                        f"참가 인원: {AppState.current_battle['participants_a']}명",
                                        size="3",
                                        color="gray.300",
                                    ),
                                    align="center",
                                    spacing="2",
                                ),
                                rx.text("VS", size="6", weight="bold", color="yellow.400", margin_x="30px"),
                                rx.vstack(
                                    rx.text(
                                        AppState.current_battle["college_b"],
                                        size="5",
                                        weight="bold",
                                        color="red.300",
                                    ),
                                    rx.text(
                                        f"총 포인트: {AppState.current_battle['score_b']}",
                                        size="4",
                                        color="white",
                                    ),
                                    rx.text(
                                        f"참가 인원: {AppState.current_battle['participants_b']}명",
                                        size="3",
                                        color="gray.300",
                                    ),
                                    align="center",
                                    spacing="2",
                                ),
                                align="center",
                                justify="center",
                                width="100%",
                                margin_y="20px",
                            ),
                            rx.divider(margin_y="15px"),
                            rx.text(
                                f"기간: {AppState.current_battle['start_date']} ~ {AppState.current_battle['end_date']}",
                                size="3",
                                color="gray.300",
                            ),
                            spacing="4",
                            padding="20px",
                        ),
                        width="100%",
                        background="rgba(255, 255, 255, 0.1)",
                        border="1px solid rgba(255, 255, 255, 0.2)",
                    ),
                    
                    # 참가 폼
                    rx.card(
                        rx.vstack(
                            rx.heading("대결 참가", size="5", margin_bottom="15px"),
                            rx.text(
                                "참가비(베팅 포인트)를 내고 참여하세요!",
                                size="3",
                                color="gray.300",
                                margin_bottom="5px",
                            ),
                            rx.text(
                                "참여한 인원들의 총 포인트로 승부가 결정됩니다.",
                                size="2",
                                color="gray.400",
                                margin_bottom="5px",
                            ),
                            rx.text(
                                "이긴 팀은 진 팀의 참가비를 모두 가져갑니다!",
                                size="2",
                                color="yellow.300",
                                margin_bottom="15px",
                            ),
                            rx.hstack(
                                rx.input(
                                    type="number",
                                    placeholder="베팅 포인트",
                                    value=AppState.battle_bet_amount,
                                    on_change=AppState.set_battle_bet_amount,
                                    size="3",
                                    width="200px",
                                ),
                                rx.button(
                                    "참가하기",
                                    on_click=AppState.join_battle,
                                    color_scheme="green",
                                    size="3",
                                ),
                                align="center",
                                spacing="4",
                            ),
                            rx.cond(
                                AppState.battle_error_message != "",
                                rx.text(
                                    AppState.battle_error_message,
                                    color="red.400",
                                    size="2",
                                    margin_top="10px",
                                ),
                            ),
                            spacing="4",
                            padding="20px",
                        ),
                        width="100%",
                        background="rgba(255, 255, 255, 0.1)",
                        border="1px solid rgba(255, 255, 255, 0.2)",
                        margin_top="20px",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.card(
                    rx.vstack(
                        rx.text(
                            "현재 진행 중인 대결이 없습니다.",
                            size="4",
                            color="gray.300",
                        ),
                        rx.text(
                            "매주 월요일 새로운 대결이 시작됩니다!",
                            size="3",
                            color="gray.400",
                            margin_top="10px",
                        ),
                        align="center",
                        padding="40px",
                    ),
                    width="100%",
                    background="rgba(255, 255, 255, 0.1)",
                    border="1px solid rgba(255, 255, 255, 0.2)",
                ),
            ),
            
            # 내 포인트 정보
            rx.card(
                rx.hstack(
                    rx.text("내 포인트: ", size="4", color="white"),
                    rx.text(
                        AppState.current_user_points,
                        size="5",
                        weight="bold",
                        color="yellow.400",
                    ),
                    align="center",
                    spacing="2",
                ),
                width="100%",
                background="rgba(255, 255, 255, 0.1)",
                border="1px solid rgba(255, 255, 255, 0.2)",
                margin_top="20px",
                padding="15px",
            ),
            
            # 홈으로 버튼
            rx.button(
                "홈으로",
                on_click=rx.redirect("/"),
                variant="ghost",
                color="white",
                margin_top="20px",
            ),
            
            spacing="6",
            align="center",
            padding="40px",
            width="100%",
        ),
        width="100%",
        min_height="100vh",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        padding="20px",
    )

