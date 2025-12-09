# home.py (수정된 최종 코드)

import reflex as rx
from ecojourney.state import AppState

# --- 공통 컴포넌트 ---
def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.button(
                "ECOJOURNEY",
                on_click=rx.redirect("/"),
                background_color="transparent",   # 버튼 배경 제거
                color="white",
                font_size="1.5em",
                font_weight="bold",
                padding="0",                     # 버튼 기본 padding 제거
                border="none",
                border_radius="8px",
                cursor="pointer",
            ),
            rx.cond(
                AppState.is_logged_in,
                rx.hstack(
                    rx.button(
                        "정보글",
                        on_click=rx.redirect("/info"),
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
                    rx.button(
                        "마이페이지",
                        on_click=rx.redirect("/mypage"),
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

def background_video() -> rx.Component:
    """순수 HTML5 <video> 태그를 사용하여 자동 재생을 강제하고 레이어를 안정화합니다."""
    return rx.box(
        # 💡 rx.html을 사용하여 필수 속성을 가진 순수 HTML 태그를 삽입
        rx.html(
            # src 경로가 정확한지 확인하면서, 필수 속성(autoplay, loop, muted, playsinline)을 강제합니다.
            """
            <video autoplay loop muted playsinline 
                src="/eco_background.mp4" 
                style='
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    z-index: -2; 
                    filter: brightness(0.6);'
            />
            """
        ),
        # 바깥 box는 배경 레이어의 위치 기준점 역할을 합니다.
        width="100%",
        height="100%",
        z_index="-2",
    )

# --- 홈 페이지 본문 ---
def home_page() -> rx.Component:
    """홈 페이지 컴포넌트"""
    return rx.box(
        background_video(),
        header(),
        
        rx.box(
            rx.vstack(
                rx.heading("EcoJourney", size="9", color="white", font_weight="bold", margin_right="100px"),
                rx.text(
                    "EcoJourney는 일상 속 행동을 기반으로\n"
                    "당신의 탄소 발자국을 시각적으로 보여주는 서비스입니다.\n"
                    "지금 바로 오늘의 흔적을 확인해보세요.",
                    white_space="pre-line",
                    size="5",
                    color="white",
                    text_align="left",
                    margin_bottom="30px",
                    margin_left="100px"
                ),
                rx.button(
                    "EcoJourney 자세히 보기",
                    on_click=rx.redirect("/intro"),
                    color="white",
                    background_color="rgba(0, 0, 0, 0.22)",      # 연한 회색 배경
                    border_radius="40px",            # pill 형태
                    padding="27px 40px",             # 사진과 비슷한 두께
                    border="4px solid rgba(255, 255, 255, 0.2)",      # 테두리 색
                    font_size="1.1em",
                    font_weight="semibold",
                    margin_left="100px",
                    _hover={
                        "background_color": "rgba(0, 0, 0, 0.4)",    # hover 시 약간 진하게
                    },
                ),
                
                align_items="center",
                spacing="5",
                z_index="1",
            ),
            width="100%",
            height="100vh",
            padding_top="80px",
            padding_bottom="80px",
            z_index="1",
            display="flex",
            justify_content="flex-end",
            align_items="center",
            padding_right="4%",
        ),
        
        footer(),
        
        width="100%",
        min_height="100vh",
        background_color="transparent", 
        # 메인 콘텐츠가 배경 위에서 올바르게 위치하도록 position: relative 추가
        position="relative" 
    )