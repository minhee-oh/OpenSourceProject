import reflex as rx
from ecojourney.state import AppState

def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.button(
                "EcoJourney",
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

def intro_page():
    return rx.box(
        background_video(),
        header(),

        rx.center(
            rx.vstack(
                rx.heading("EcoJourney는 이렇게 사용해요", size="8", color="white", margin_bottom="15px"),
                
                # rx.text(
                #     "EcoJourney는 일상 속 행동을 기반으로\n"
                #     "여섯 가지 카테고리를 순서대로 기록해요.",
                #     white_space="pre-line",
                #     color="white",
                #     max_width="600px",
                #     text_align="center",
                #     margin_y="10px"
                # ),

                rx.divider(background_color="white"),

                rx.vstack(
                    rx.list(
                        rx.list_item("1. 당신의 하루를 기록하세요.", color="white", font_weight="bold", text_align="center", padding_top="5px"),
                        rx.list_item("일상 속 6가지 카테고리(교통, 식품, 의류, 쓰레기, 전기, 물)마다 해당되는 활동을 선택합니다.", color="white", text_align="center", padding_bottom="15px"),
                        rx.list_item("2. 측정 기준을 정합니다", color="white", font_weight="bold", text_align="center", padding_top="5px"),
                        rx.list_item("선택한 활동에 대한 측정 단위(예: km 또는 시간)를 고르고 값을 입력합니다.", color="white", text_align="center", padding_bottom="15px"),
                        rx.list_item("3. 결과를 확인하세요.",color="white", font_weight="bold", text_align="center", padding_top="5px"),
                        rx.list_item("모든 카테고리의 기록이 완료되면, 당신의 라이프스타일에 대한 개인화된 탄소 발자국 리포트를 즉시 볼 수 있습니다.", color="white", text_align="center", padding_bottom="15px"),
                        spacing="3",
                    ),
                    align="start",
                    width="100%",
                    padding_x="40px"
                ),

                rx.divider(background_color="white"),

                rx.text(
                    "지금 바로 당신의 첫 걸음을 확인해보세요.",
                    color="white",
                    max_width="600px",
                    text_align="center",
                    margin_y="10px"
                ),

                rx.button(
                    "Start your Journey",
                    on_click=rx.redirect("/input/transportation"),
                    color="white",
                    background_color="rgba(0, 0, 0, 0.22)",
                    border_radius="40px",
                    padding="25px 40px",
                    border="4px solid rgba(255, 255, 255, 0.2)",
                    font_size="1.1em",
                    font_weight="semibold",
                    _hover={
                        "background_color": "rgba(0, 0, 0, 0.4)",
                    },
                ),

                spacing="5",
                align="center",
            ),
            height="100vh",    # ← 정중앙 배치의 핵심
            z_index="1",
        ),

        footer(),

        width="100%",
        min_height="100vh",
        background_color="transparent",
        position="relative",
    )
