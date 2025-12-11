# info.py - 정보 글 & OX 퀴즈 페이지

import reflex as rx
from ecojourney.state import AppState

# --------------------------
# 아티클 데이터
# --------------------------
ARTICLES = [
    {
        "title": "탄소중립이란?",
        "summary": "탄소 배출을 0으로 만드는 개념.",
        "full_text": "탄소 중립은 인간 활동으로 인해 발생하는 이산화탄소의 배출량을 상쇄하여 순 배출량을 0에 가깝게 만드는 것입니다.\n\n탄소 흡수원 확대와 배출 감소가 핵심입니다.",
        "image": "/static/images/article1.jpg",
        "on_read": AppState.complete_daily_info,
    },
    {
        "title": "재생에너지의 필요성",
        "summary": "태양광·풍력은 지속 가능한 에너지입니다.",
        "full_text": "재생에너지는 화석연료를 대체할 수 있는 에너지로 환경적·경제적으로 중요한 역할을 합니다.\n\n미래에는 전력의 대부분이 재생에너지로 충당될 것입니다.",
        "image": "/static/images/article2.jpg",
        "on_read": AppState.complete_daily_info,
    },
]


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
                        border="1px solid #FFFFFF",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
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


# --------------------------
# 모달 컴포넌트
# --------------------------
def article_modal(article: dict):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.box(
                rx.vstack(
                    rx.heading(article["title"], size="6", color="#333333"),
                    rx.text(article["summary"], size="3", color="gray.200"),
                    spacing="2",
                ),
                width="250px",
                height="300px",
                border_radius="20px",
                padding="20px",
                cursor="pointer",
                background=f"url('{article['image']}')",
                background_size="cover",
                background_position="center",
                box_shadow="0 6px 16px rgba(0,0,0,0.25)",
                position="relative",
                class_name="article-card",
            )
        ),

        rx.dialog.content(
            rx.vstack(
                # 이미지
                rx.box(
                    background=f"url('{article['image']}')",
                    background_size="cover",
                    background_position="center",
                    width="100%",
                    height="200px",
                    border_radius="12px",
                ),

                # 제목 & 본문
                rx.heading(article["title"], size="6", margin_top="15px"),
                rx.text(article["full_text"], size="4", color="gray.700"),

                rx.dialog.close(
                    rx.button(
                        rx.cond(
                            AppState.article_read_today,
                            "오늘 이미 읽었습니다",
                            "읽음 처리"
                        ),
                        on_click=[article["on_read"]],
                        color_scheme=rx.cond(
                            AppState.article_read_today,
                            "gray",
                            "green"
                        ),
                        disabled=AppState.article_read_today,
                        width="100%",
                        margin_top="20px",
                    ),
                ),

                spacing="4",
            ),
            padding="25px",
            border_radius="16px",
            max_width="600px",
            background="white",
        )
    )


# --------------------------
# OX 퀴즈 카드
# --------------------------
def quiz_card():
    return rx.cond(
        AppState.quiz_answered,
        # 이미 답변한 경우 - 결과 표시
        rx.box(
            rx.vstack(
                rx.heading(
                    rx.cond(
                        AppState.quiz_is_correct,
                        "🎉 정답입니다! 🎉",
                        "😢 틀렸습니다 😢"
                    ),
                    size="7",
                    color="white",
                    margin_bottom="15px",
                ),
                rx.text(
                    rx.cond(
                        AppState.quiz_is_correct,
                        "OX 퀴즈를 완료했습니다! 포인트가 적립되었습니다. 내일 다시 도전해주세요!",
                        "아쉽게도 틀렸습니다. 내일 다시 도전해주세요!"
                    ),
                    color="white",
                    size="5",
                    text_align="center",
                ),
                spacing="3",
                align="center",
            ),
            background=rx.cond(
                AppState.quiz_is_correct,
                "linear-gradient(135deg, #4DAB75 0%, #3d9463 100%)",
                "linear-gradient(135deg, #E74C3C 0%, #c0392b 100%)"
            ),
            padding="40px",
            border_radius="12px",
            width="100%",
            max_width="850px",
            height="120px",
            display="flex",
            align_items="center",
            justify_content="center",
            box_shadow="0 6px 16px rgba(0,0,0,0.25)",
        ),

        # 아직 답변하지 않은 경우 - 퀴즈 표시
        rx.hstack(
            # 문제 박스
            rx.box(
                rx.text(
                    "지구 온난화를 막기 위해서는 일회용품 사용을 줄여야 한다.",
                    color="#333333",
                    size="5",
                    font_weight="500",
                ),
                background="#F1F3F4",
                padding="40px",
                border_radius="12px",
                flex="1",
                height="120px",
                display="flex",
                align_items="center",
            ),

            # O 버튼 (정답)
            rx.button(
                "O",
                on_click=lambda: AppState.answer_quiz(True),
                background_color="#4DAB75",
                color="white",
                size="4",
                width="120px",
                height="120px",
                border_radius="12px",
                font_weight="bold",
                font_size="2.5em",
                box_shadow="0 6px 16px rgba(0,0,0,0.25)",
                transition="all 0.3s ease",
                _hover={
                    "background_color": "#3d9463",
                    "transform": "translateY(-8px)",
                    "box_shadow": "0 12px 24px rgba(0,0,0,0.35)"
                },
            ),

            # X 버튼 (오답)
            rx.button(
                "X",
                on_click=lambda: AppState.answer_quiz(False),
                background_color="#E74C3C",
                color="white",
                size="4",
                width="120px",
                height="120px",
                border_radius="12px",
                font_weight="bold",
                font_size="2.5em",
                box_shadow="0 6px 16px rgba(0,0,0,0.25)",
                transition="all 0.3s ease",
                _hover={
                    "background_color": "#c0392b",
                    "transform": "translateY(-8px)",
                    "box_shadow": "0 12px 24px rgba(0,0,0,0.35)"
                },
            ),

            spacing="4",
            width="100%",
            max_width="850px",
            align="stretch",
        ),
    )


def info_page() -> rx.Component:
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

        @keyframes slideUpFade {
            0% {
                opacity: 0;
                transform: translateY(40px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .article-card {
            opacity: 0;
            animation: slideUpFade 0.6s ease forwards;
        }

        .article-card:nth-child(1) {
            animation-delay: 0.1s;
        }

        .article-card:nth-child(2) {
            animation-delay: 0.2s;
        }

        .article-card:nth-child(3) {
            animation-delay: 0.3s;
        }

        .article-card:nth-child(4) {
            animation-delay: 0.4s;
        }

        .article-card:nth-child(5) {
            animation-delay: 0.5s;
        }

        .article-card:nth-child(6) {
            animation-delay: 0.6s;
        }

        .article-card:nth-child(7) {
            animation-delay: 0.7s;
        }

        .article-card:nth-child(8) {
            animation-delay: 0.8s;
        }

        .article-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
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
                            "챌린지",
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
                            "아티클을 읽거나 OX 퀴즈를 풀어 일일 챌린지를 완료하고 포인트를 쌓아보세요!",
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
                            src="/challenge.png",    # assets/challenge.png
                            width="70%",             # 이미지 너비
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
                        padding_top="30px",
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

            # ----------------------------------------------------
            # ② 실제 콘텐츠
            # ----------------------------------------------------
            rx.box(
                rx.vstack(
                    # 아티클 제목 (가운데 정렬)
                    rx.box(
                        rx.heading(
                            "아티클",
                            size="8",
                            color="#333333",
                            style={
                                "opacity": 0,
                                "transform": "translateY(20px)",
                                "animation": "fadeInUp 0.8s ease forwards",
                                "animation-delay": "0.1s",
                            },
                        ),
                        width="100%",
                        text_align="center",
                        margin_top="15px",
                        margin_bottom="30px",
                    ),

                    # 아티클 카드 그리드 (한 줄에 4개, 가운데 정렬)
                    rx.box(
                        rx.grid(
                            *[article_modal(article) for article in ARTICLES],
                            columns="repeat(4, 1fr)",
                            spacing="3",
                            width="100%",
                            max_width="1200px",
                        ),
                        width="100%",
                        display="flex",
                        justify_content="center",
                    ),

                    rx.divider(margin_top="40px"),

                    rx.box(
                        rx.heading("OX 퀴즈", size="8", color="#333333"),
                        width="100%",
                        text_align="center",
                        margin_bottom="30px",
                    ),
                    quiz_card(),

                    rx.cond(
                        AppState.challenge_message != "",
                        rx.callout(
                            AppState.challenge_message,
                            icon="info",
                            color_scheme="green",
                            width="100%",
                        ),
                    ),
                    spacing="6",
                    width="100%",
                    max_width="1200px",
                    align="center",
                ),

                width="100%",
                z_index="2",
                padding="40px 20px",
                display="flex",
                justify_content="center",

                # ⭐ 콘텐츠를 상단 66vh 바로 아래로 내리는 핵심 코드
                margin_top="66vh",
            ),

        ),

        # 페이지 로드 시 퀴즈 상태 로드
        on_mount=AppState.load_quiz_state,
    )
