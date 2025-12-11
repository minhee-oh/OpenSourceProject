# battle.py - 단과대별 대결 페이지

import reflex as rx
from ecojourney.state import AppState


def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            # 로고 버튼
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

            # 로그인 상태에 따른 메뉴
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
                        _hover={"border": "1px solid #FFFFFF"},
                    ),
                    rx.button(
                        "배틀",
                        on_click=rx.redirect("/battle"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="1px solid #FFFFFF",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
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
                        _hover={"border": "1px solid #FFFFFF"},
                    ),
                    rx.button(
                        "리포트",
                        on_click=rx.redirect("/intro"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"border": "1px solid #FFFFFF"},
                    ),
                    rx.text(
                        f"{AppState.current_user_id}님",
                        color="#FFFFFF",
                        font_size="1em",
                        margin_right="10px",
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
                        _hover={"border": "1px solid #FFFFFF"},
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
                        _hover={"background_color": "rgba(255, 255, 255, 0.9)"},
                    ),
                    spacing="3",
                    align="center",
                ),

                # 로그인 안 된 상태 → 로그인 버튼
                rx.button(
                    "로그인",
                    on_click=rx.redirect("/auth"),
                    background_color="#FFFFFF",
                    color="#4DAB75",
                    border="1px solid #4DAB75",
                    border_radius="25px",
                    padding="8px 20px",
                    font_weight="500",
                    _hover={"background_color": "rgba(255, 255, 255, 0.9)"},
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


def battle_page() -> rx.Component:
    """단과대별 대결 페이지"""
    return rx.cond(
        AppState.is_logged_in,
        rx.box(
            header(),

        # fade-in 애니메이션을 위한 CSS 삽입
        rx.html("""
        <style>
        @keyframes fadeInUp {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        </style>
        """),

         # 배경 레이어 구성
        rx.box(
            # ---------------------------------------------
            # 1) 상단 2/3 배경 + 텍스트 + fade-in animation
            # ---------------------------------------------
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            "배틀",
                            size="9",
                            color="#333333",
                            margin_bottom="18px",
                            style={
                                "opacity": 0,
                                "transform": "translateY(20px)",
                                "animation": "fadeInUp 0.8s ease forwards",
                                "animation-delay": "0.1s",
                            },
                        ),
                        rx.text(
                            "단과대별 배틀에 참여하여 포인트를 베팅하고 승리의 영광을 차지하세요!",
                            color="gray.200",
                            size="5",
                            font_weight="bold",
                            text_align="left",
                            width="100%",
                            style={
                                "opacity": 0,
                                "transform": "translateY(20px)",
                                "animation": "fadeInUp 1s ease forwards",
                                "animation-delay": "0.25s",
                            },
                        ),
                        spacing="2",
                        align="start",        # 가로: 왼쪽 정렬
                        justify="center",     # 세로: 중앙 정렬
                        height="100%",
                        padding_top="50px",
                        padding_left="100px",
                    ),

                    # -----------------------
                    # 오른쪽: 이미지 영역
                    # -----------------------
                    rx.box(
                        rx.image(
                            src="/battle.png",
                            width="100%",             # 이미지 너비
                            height="auto",
                            object_fit="contain",
                            style={
                                "opacity": 0,
                                "transform": "translateY(20px)",
                                "animation": "fadeInUp 0.8s ease forwards",
                                "animation-delay": "0.2s",
                            },
                        ),
                        width="50%",                 # 전체의 절반을 이미지 영역으로 사용
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        padding_left="50px",
                        padding_top="70px",
                    ),
                    width="100%",
                    height="100%",
                    align="center",
                    justify="between",
                ),
                width="100%",
                height="80vh",
                background="linear-gradient(135deg, rgba(77, 171, 117, 0.1) 0%, rgba(77, 171, 117, 0.15) 100%)",
                position="absolute",
                top="0",
                left="0",
                z_index="0",
            ),

            # 실제 콘텐츠
            rx.box(
                rx.vstack(
            
                    # 현재 대결 정보
                    rx.cond(
                        AppState.current_battle != None,
                        rx.vstack(
                            rx.card(
                                rx.vstack(
                                    rx.heading("현재 대결", size="6", margin_bottom="15px", color="#333333"),
                            rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        AppState.current_battle["college_a"],
                                        size="5",
                                        weight="bold",
                                        color="blue.600",
                                    ),
                                    rx.text(
                                        f"총 포인트: {AppState.current_battle['score_a']}",
                                        size="4",
                                        color="#333333",
                                    ),
                                    rx.text(
                                        f"참가 인원: {AppState.current_battle['participants_a']}명",
                                        size="3",
                                        color="gray.600",
                                    ),
                                    align="center",
                                    spacing="2",
                                ),
                                rx.text("VS", size="6", weight="bold", color="#4DAB75", margin_x="30px"),
                                rx.vstack(
                                    rx.text(
                                        AppState.current_battle["college_b"],
                                        size="5",
                                        weight="bold",
                                        color="red.600",
                                    ),
                                    rx.text(
                                        f"총 포인트: {AppState.current_battle['score_b']}",
                                        size="4",
                                        color="#333333",
                                    ),
                                    rx.text(
                                        f"참가 인원: {AppState.current_battle['participants_b']}명",
                                        size="3",
                                        color="gray.600",
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
                                        color="gray.600",
                                    ),
                                    spacing="4",
                                    padding="20px",
                                ),
                                width="100%",
                                background="white",
                                border="1px solid rgba(0, 0, 0, 0.1)",
                                box_shadow="0 4px 12px rgba(0,0,0,0.1)",
                            ),
                    
                            # 참가 폼
                            rx.card(
                                rx.vstack(
                                    rx.heading("대결 참가", size="5", margin_bottom="15px", color="#333333"),
                                    rx.text(
                                        "참가비(베팅 포인트)를 내고 참여하세요!",
                                        size="3",
                                        color="gray.700",
                                        margin_bottom="5px",
                                    ),
                                    rx.text(
                                        "참여한 인원들의 총 포인트로 승부가 결정됩니다.",
                                        size="2",
                                        color="gray.600",
                                        margin_bottom="5px",
                                    ),
                                    rx.text(
                                        "이긴 팀은 진 팀의 참가비를 모두 가져갑니다!",
                                        size="2",
                                        color="#4DAB75",
                                        font_weight="bold",
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
                                            color="red.600",
                                            size="2",
                                            margin_top="10px",
                                        ),
                                    ),
                                    spacing="4",
                                    padding="20px",
                                ),
                                width="100%",
                                background="white",
                                border="1px solid rgba(0, 0, 0, 0.1)",
                                box_shadow="0 4px 12px rgba(0,0,0,0.1)",
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
                                    color="gray.700",
                                ),
                                rx.text(
                                    "매주 월요일 새로운 대결이 시작됩니다!",
                                    size="3",
                                    color="gray.600",
                                    margin_top="10px",
                                ),
                                align="center",
                                padding="40px",
                            ),
                            width="100%",
                            background="white",
                            border="1px solid rgba(0, 0, 0, 0.1)",
                            box_shadow="0 4px 12px rgba(0,0,0,0.1)",
                        ),
                    ),

                    # 내 포인트 정보
                    rx.card(
                        rx.hstack(
                            rx.text("내 포인트: ", size="4", color="#333333"),
                            rx.text(
                                AppState.current_user_points,
                                size="5",
                                weight="bold",
                                color="#4DAB75",
                            ),
                            align="center",
                            spacing="2",
                        ),
                        width="100%",
                        background="white",
                        border="1px solid rgba(0, 0, 0, 0.1)",
                        box_shadow="0 4px 12px rgba(0,0,0,0.1)",
                        margin_top="20px",
                        padding="15px",
                    ),

                    spacing="6",
                    align="center",
                    padding="40px 20px",
                    width="100%",
                    max_width="1200px",
                ),

                width="100%",
                z_index="2",
                display="flex",
                justify_content="center",
                margin_top="70vh",
            ),
        ),
        ),
        rx.box(
            on_mount=rx.redirect("/auth"),
        ),
    )

