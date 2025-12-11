# ranking.py - 저번주 대결 랭킹 페이지

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
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"border": "1px solid #FFFFFF"},
                    ),
                    rx.button(
                        "랭킹",
                        on_click=rx.redirect("/ranking"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="1px solid #FFFFFF",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
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


def ranking_page() -> rx.Component:
    """저번주 대결 결과 랭킹 페이지"""
    return rx.box(
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
                            "랭킹",
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
                            "개인 포인트 랭킹과 지난주 단과대 대결 결과를 확인하세요!",
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
                            src="/ranking.png",
                            width="50%",             # 이미지 너비
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
                        padding_left="30px",
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
            
                    # 개인 포인트 랭킹 섹션
                    rx.card(
                        rx.vstack(
                            rx.heading("개인 포인트 랭킹 (Top 10)", size="6", color="#333333", margin_bottom="15px"),
                    rx.cond(
                        AppState.personal_rankings.length() > 0,
                        rx.vstack(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("순위", width="80px"),
                                        rx.table.column_header_cell("학번", width="150px"),
                                        rx.table.column_header_cell("단과대", width="200px"),
                                        rx.table.column_header_cell("포인트", width="150px"),
                                    ),
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        AppState.personal_rankings,
                                        lambda ranking: rx.table.row(
                                            rx.table.cell(
                                                rx.cond(
                                                    ranking["rank"] == 1,
                                                    rx.badge("🥇 1등", color_scheme="yellow", size="2"),
                                                    rx.cond(
                                                        ranking["rank"] == 2,
                                                        rx.badge("🥈 2등", color_scheme="gray", size="2"),
                                                        rx.cond(
                                                            ranking["rank"] == 3,
                                                            rx.badge("🥉 3등", color_scheme="orange", size="2"),
                                                            rx.text(ranking["rank"], size="3", color="white"),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            rx.table.cell(
                                                rx.text(ranking["student_id"], size="3", color="#333333"),
                                            ),
                                            rx.table.cell(
                                                rx.text(ranking["college"], size="3", color="#333333"),
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    f"{ranking['points']:,}점",
                                                    size="3",
                                                    color="#4DAB75",
                                                    weight="bold",
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                width="100%",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        rx.text(
                            "랭킹 데이터가 없습니다.",
                            size="3",
                            color="gray.600",
                        ),
                    ),
                    spacing="4",
                    padding="20px",
                    width="100%",
                        ),
                        width="100%",
                        background="white",
                        border="1px solid rgba(0, 0, 0, 0.1)",
                        box_shadow="0 4px 12px rgba(0,0,0,0.1)",
                        margin_bottom="30px",
                    ),
            
                    # 저번주 대결 결과 섹션
                    rx.heading("지난주 배틀 결과", size="6", color="#333333", margin_bottom="15px"),

                    rx.cond(
                        AppState.previous_battles.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.previous_battles,
                        lambda battle, i: rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(
                                            battle["college_a"],
                                            size="5",
                                            weight="bold",
                                            color="blue.600",
                                        ),
                                        rx.text(
                                            f"{battle['score_a']}점",
                                            size="4",
                                            color="#333333",
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    rx.vstack(
                                        rx.cond(
                                            battle["winner"] == battle["college_a"],
                                            rx.badge("WIN", color_scheme="green", size="2"),
                                            rx.cond(
                                                battle["winner"] == battle["college_b"],
                                                rx.badge("LOSE", color_scheme="red", size="2"),
                                                rx.badge("DRAW", color_scheme="gray", size="2"),
                                            ),
                                        ),
                                        rx.text("VS", size="4", weight="bold", color="#4DAB75"),
                                        align="center",
                                        spacing="2",
                                    ),
                                    rx.vstack(
                                        rx.text(
                                            battle["college_b"],
                                            size="5",
                                            weight="bold",
                                            color="red.600",
                                        ),
                                        rx.text(
                                            f"{battle['score_b']}점",
                                            size="4",
                                            color="#333333",
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    align="center",
                                    justify="between",
                                    width="100%",
                                    padding="15px",
                                ),
                                rx.divider(margin_y="10px"),
                                rx.text(
                                    f"날짜: {battle['start_date']}",
                                    size="2",
                                    color="gray.600",
                                ),
                                spacing="3",
                                padding="20px",
                            ),
                            width="100%",
                            background="white",
                            border="1px solid rgba(0, 0, 0, 0.1)",
                            box_shadow="0 4px 12px rgba(0,0,0,0.1)",
                            margin_bottom="15px",
                        ),
                    ),
                    spacing="4",
                    width="100%",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text(
                                    "지난주 배틀 결과가 없습니다.",
                                    size="4",
                                    color="gray.700",
                                ),
                                rx.text(
                                    "이번 주 배틀이 종료되면 결과가 표시됩니다.",
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
    )

