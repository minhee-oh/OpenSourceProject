# ranking.py - 저번주 대결 랭킹 페이지

import reflex as rx
from ecojourney.state import AppState


def ranking_page() -> rx.Component:
    """저번주 대결 결과 랭킹 페이지"""
    return rx.container(
        rx.vstack(
            rx.heading("📊 랭킹", size="8", color="white", margin_bottom="20px"),
            
            # 개인 포인트 랭킹 섹션
            rx.card(
                rx.vstack(
                    rx.heading("🏆 개인 포인트 랭킹 (Top 10)", size="6", color="white", margin_bottom="15px"),
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
                                                rx.text(ranking["student_id"], size="3", color="white"),
                                            ),
                                            rx.table.cell(
                                                rx.text(ranking["college"], size="3", color="white"),
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    f"{ranking['points']:,}점",
                                                    size="3",
                                                    color="yellow.300",
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
                            color="gray.400",
                        ),
                    ),
                    spacing="4",
                    padding="20px",
                    width="100%",
                ),
                width="100%",
                background="rgba(255, 255, 255, 0.1)",
                border="1px solid rgba(255, 255, 255, 0.2)",
                margin_bottom="30px",
            ),
            
            # 저번주 대결 결과 섹션
            rx.heading("📊 저번주 대결 결과", size="6", color="white", margin_bottom="15px"),
            
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
                                            color="blue.300",
                                        ),
                                        rx.text(
                                            f"{battle['score_a']}점",
                                            size="4",
                                            color="white",
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
                                        rx.text("VS", size="4", weight="bold", color="yellow.400"),
                                        align="center",
                                        spacing="2",
                                    ),
                                    rx.vstack(
                                        rx.text(
                                            battle["college_b"],
                                            size="5",
                                            weight="bold",
                                            color="red.300",
                                        ),
                                        rx.text(
                                            f"{battle['score_b']}점",
                                            size="4",
                                            color="white",
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
                                    color="gray.400",
                                ),
                                spacing="3",
                                padding="20px",
                            ),
                            width="100%",
                            background="rgba(255, 255, 255, 0.1)",
                            border="1px solid rgba(255, 255, 255, 0.2)",
                            margin_bottom="15px",
                        ),
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.card(
                    rx.vstack(
                        rx.text(
                            "저번주 대결 결과가 없습니다.",
                            size="4",
                            color="gray.300",
                        ),
                        rx.text(
                            "이번 주 대결이 종료되면 결과가 표시됩니다.",
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

