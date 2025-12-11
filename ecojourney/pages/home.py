# home.py (수정된 최종 코드)

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
        z_index="20",
        background_color="#4DAB75",
    )


def footer() -> rx.Component:
    return rx.box(
        rx.center(
            # 💡 영상 위에서 잘 보이도록 텍스트 색상 조정
            rx.text("© 2025 EcoJourney. All rights reserved.", color="white", font_size="0.9em"),
            padding="1em",
        ),
        width="100%",
        position="fixed",
        bottom="0",
        z_index="100",
        background_color="transparent",
    )

# --- 홈 페이지 본문 ---
def home_page() -> rx.Component:
    """홈 페이지 컴포넌트"""
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
            # 1) 배경 (가장 아래 레이어)
            # ---------------------------------------------
            rx.box(
                width="100%",
                height="55vh",
                background="#4DAB75",
                position="absolute",
                top="0",
                left="0",
                z_index="0",
            ),

            # ---------------------------------------------
            # 2) 이미지 (중간 레이어)
            # ---------------------------------------------
            rx.box(
                rx.image(
                    src="/earth.png",
                    width="50%",
                    height="auto",
                    object_fit="contain",
                    style={
                        "opacity": 0,
                        "transform": "translateY(20px)",
                        "animation": "fadeInUp 0.8s ease forwards",
                        "animation-delay": "0.2s",
                    },
                ),
                width="100%",
                height="100vh",
                position="absolute",
                top="15",
                left="0",
                z_index="10",
                display="flex",
                align_items="center",
                justify_content="center",
            ),

            # ---------------------------------------------
            # 3) 텍스트 (이미지보다 위 레이어)
            # ---------------------------------------------
            rx.box(
                rx.vstack(
                    rx.heading(
                        "ECOJOURNEY",
                        size="9",
                        color="#FFFFFF",
                        margin_bottom="18px",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 0.8s ease forwards",
                            "animation-delay": "0.1s",
                        },
                    ),
                    rx.text(
                        "줄일수록 보이는 나의 변화.",
                        color="#FFFFFF",
                        size="5",
                        font_weight="bold",
                        text_align="center",
                        width="100%",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 1s ease forwards",
                            "animation-delay": "0.25s",
                        },
                    ),
                    rx.text(
                        "다함께 지속 가능한 에코 라이프를 만들어요.",
                        color="#FFFFFF",
                        size="5",
                        font_weight="bold",
                        text_align="center",
                        width="100%",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 1s ease forwards",
                            "animation-delay": "0.35s",
                        },
                    ),
                    spacing="2",
                    align="center",
                    justify="center",
                ),
                width="100%",
                height="100vh",
                position="absolute",
                top="10",
                left="0",
                z_index="15",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
        ),
    )


    #     rx.box(
    #         rx.vstack(
    #             rx.heading("EcoJourney", size="9", color="white", font_weight="bold", margin_right="100px"),
    #             rx.text(
    #                 "EcoJourney는 일상 속 행동을 기반으로\n"
    #                 "당신의 탄소 발자국을 시각적으로 보여주는 서비스입니다.\n"
    #                 "지금 바로 오늘의 흔적을 확인해보세요.",
    #                 white_space="pre-line",
    #                 size="5",
    #                 color="white",
    #                 text_align="left",
    #                 margin_bottom="30px",
    #                 margin_left="100px"
    #             ),
    #             rx.button(
    #                 "EcoJourney 자세히 보기",
    #                 on_click=rx.redirect("/intro"),
    #                 color="white",
    #                 background_color="rgba(0, 0, 0, 0.22)",      # 연한 회색 배경
    #                 border_radius="40px",            # pill 형태
    #                 padding="27px 40px",             # 사진과 비슷한 두께
    #                 border="4px solid rgba(255, 255, 255, 0.2)",      # 테두리 색
    #                 font_size="1.1em",
    #                 font_weight="semibold",
    #                 margin_left="100px",
    #                 _hover={
    #                     "background_color": "rgba(0, 0, 0, 0.4)",    # hover 시 약간 진하게
    #                 },
    #             ),
                
    #             align_items="center",
    #             spacing="5",
    #             z_index="1",
    #         ),
    #         width="100%",
    #         height="100vh",
    #         padding_top="80px",
    #         padding_bottom="80px",
    #         z_index="1",
    #         display="flex",
    #         justify_content="flex-end",
    #         align_items="center",
    #         padding_right="4%",
    #     ),
        
    #     footer(),
        
    #     width="100%",
    #     min_height="100vh",
    #     background_color="transparent", 
    #     # 메인 콘텐츠가 배경 위에서 올바르게 위치하도록 position: relative 추가
    #     position="relative" 
    # )