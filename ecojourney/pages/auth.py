# auth.py - 로그인 및 회원가입 페이지

import reflex as rx
from ecojourney.state import AppState

def auth_page() -> rx.Component:
    """로그인 및 회원가입 페이지"""
    return rx.box(
        rx.center(
            rx.box(
                rx.hstack(
                    # 왼쪽 영역 - 소개 섹션
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "ECOJOURNEY",
                                size="8",
                                color="#4DAB75",
                                font_weight="700",
                                letter_spacing="-0.02em",
                            ),
                            rx.text(
                                "탄소 발자국을 측정하고",
                                color="#666666",
                                font_size="1.2em",
                                font_weight="500",
                            ),
                            rx.text(
                                "지구를 지키는 여정에 함께하세요",
                                color="#666666",
                                font_size="1.2em",
                                font_weight="500",
                            ),
                            rx.box(height="20px"),
                            rx.text(
                                "🌍 일상 속 탄소 배출량 계산",
                                color="#999999",
                                font_size="1em",
                            ),
                            rx.text(
                                "📊 AI 기반 맞춤형 분석",
                                color="#999999",
                                font_size="1em",
                            ),
                            rx.text(
                                "🏆 챌린지와 배틀로 동기부여",
                                color="#999999",
                                font_size="1em",
                            ),
                            rx.text(
                                "⭐ 포인트 획득과 랭킹 시스템",
                                color="#999999",
                                font_size="1em",
                            ),
                            spacing="3",
                            align="start",
                            padding="60px",
                            justify="center",
                        ),
                        width="50%",
                        min_height="500px",
                        display="flex",
                        background="linear-gradient(135deg, rgba(77, 171, 117, 0.05) 0%, rgba(77, 171, 117, 0.15) 100%)",
                        border_radius="30px 0 0 30px",
                    ),

                    # 오른쪽 영역 - 로그인/회원가입 폼
                    rx.box(
                        rx.vstack(
                            # 로그인/회원가입 탭
                            rx.tabs.root(
                                rx.tabs.list(
                                    rx.tabs.trigger(
                                        "로그인",
                                        value="login",
                                        color="#666666",
                                        _selected={
                                            "color": "#4DAB75",
                                            "border_bottom": "2px solid #4DAB75",
                                        },
                                        font_weight="600",
                                        font_size="1.1em",
                                        padding="10px 30px",
                                    ),
                                    rx.tabs.trigger(
                                        "회원가입",
                                        value="signup",
                                        color="#666666",
                                        _selected={
                                            "color": "#4DAB75",
                                            "border_bottom": "2px solid #4DAB75",
                                        },
                                        font_weight="600",
                                        font_size="1.1em",
                                        padding="10px 30px",
                                    ),
                                    justify="center",
                                ),
                                rx.tabs.content(
                                    # 로그인 폼
                                    rx.vstack(
                                        rx.form(
                                            rx.vstack(
                                                rx.input(
                                                    placeholder="학번",
                                                    name="student_id",
                                                    value=AppState.login_student_id,
                                                    on_change=AppState.set_login_student_id,
                                                    size="3",
                                                    width="100%",
                                                    background_color="#FFFFFF",
                                                    color="#333333",
                                                    border_radius="12px",
                                                    border="1px solid #E0E0E0",
                                                    padding="8px 16px",
                                                    _focus={
                                                        "border": "2px solid #4DAB75",
                                                        "outline": "none",
                                                    },
                                                    _placeholder={
                                                        "color": "#999999",
                                                    },
                                                ),
                                                rx.input(
                                                    type="password",
                                                    placeholder="비밀번호",
                                                    name="password",
                                                    value=AppState.login_password,
                                                    on_change=AppState.set_login_password,
                                                    size="3",
                                                    width="100%",
                                                    background_color="#FFFFFF",
                                                    color="#333333",
                                                    border_radius="12px",
                                                    border="1px solid #E0E0E0",
                                                    padding="8px 16px",
                                                    _focus={
                                                        "border": "2px solid #4DAB75",
                                                        "outline": "none",
                                                    },
                                                    _placeholder={
                                                        "color": "#999999",
                                                    },
                                                ),
                                                rx.cond(
                                                    AppState.auth_error_message != "",
                                                    rx.text(
                                                        AppState.auth_error_message,
                                                        color="#f87171",
                                                        size="2",
                                                        margin_top="10px",
                                                    ),
                                                ),
                                                rx.button(
                                                    "로그인",
                                                    type="submit",
                                                    width="100%",
                                                    background_color="#4DAB75",
                                                    color="#FFFFFF",
                                                    border_radius="25px",
                                                    padding="14px 28px",
                                                    font_weight="600",
                                                    font_size="1.05em",
                                                    border="none",
                                                    cursor="pointer",
                                                    box_shadow="0 4px 20px rgba(77, 171, 117, 0.3)",
                                                    transition="all 0.25s ease",
                                                    _hover={
                                                        "background_color": "#3d9a66",
                                                        "transform": "translateY(-2px)",
                                                        "box_shadow": "0 6px 24px rgba(77, 171, 117, 0.5)",
                                                    },
                                                    margin_top="10px",
                                                ),
                                                spacing="4",
                                            ),
                                            on_submit=AppState.login,
                                            width="100%",
                                        ),
                                        spacing="4",
                                        align="center",
                                        padding="30px 0",
                                        width="100%",
                                    ),
                                    value="login",
                                ),
                                rx.tabs.content(
                                    # 회원가입 폼
                                    rx.vstack(
                                        rx.form(
                                            rx.vstack(
                                                rx.input(
                                                    placeholder="학번",
                                                    name="student_id",
                                                    value=AppState.signup_student_id,
                                                    on_change=AppState.set_signup_student_id,
                                                    size="3",
                                                    width="100%",
                                                    background_color="#FFFFFF",
                                                    color="#333333",
                                                    border_radius="12px",
                                                    border="1px solid #E0E0E0",
                                                    padding="8px 16px",
                                                    _focus={
                                                        "border": "2px solid #4DAB75",
                                                        "outline": "none",
                                                    },
                                                    _placeholder={
                                                        "color": "#999999",
                                                    },
                                                ),
                                                rx.input(
                                                    type="password",
                                                    placeholder="비밀번호",
                                                    name="password",
                                                    value=AppState.signup_password,
                                                    on_change=AppState.set_signup_password,
                                                    size="3",
                                                    width="100%",
                                                    background_color="#FFFFFF",
                                                    color="#333333",
                                                    border_radius="12px",
                                                    border="1px solid #E0E0E0",
                                                    padding="8px 16px",
                                                    _focus={
                                                        "border": "2px solid #4DAB75",
                                                        "outline": "none",
                                                    },
                                                    _placeholder={
                                                        "color": "#999999",
                                                    },
                                                ),
                                                rx.select(
                                                    [
                                                        "인문대학",
                                                        "사회과학대학",
                                                        "경영대학",
                                                        "자연과학대학",
                                                        "의과대학",
                                                        "간호대학",
                                                        "글로벌융합대학",
                                                        "미디어스쿨",
                                                        "반도체·디스플레이스쿨",
                                                        "정보과학대학",
                                                        "미래융합스쿨",
                                                        "산학협력특성화대학",
                                                        "일송자유교양대학",
                                                        "자기설계융합전공"
                                                    ],
                                                    placeholder="단과대 선택",
                                                    value=AppState.signup_college,
                                                    on_change=AppState.set_signup_college,
                                                    size="3",
                                                    width="100%",
                                                    background_color="#FFFFFF",
                                                    color="#333333",
                                                    border_radius="12px",
                                                    border="1px solid #E0E0E0",
                                                    padding="12px 16px",
                                                ),
                                                rx.cond(
                                                    AppState.auth_error_message != "",
                                                    rx.text(
                                                        AppState.auth_error_message,
                                                        color="#f87171",
                                                        size="2",
                                                        margin_top="10px",
                                                    ),
                                                ),
                                                rx.button(
                                                    "회원가입",
                                                    type="submit",
                                                    width="100%",
                                                    background_color="#4DAB75",
                                                    color="#FFFFFF",
                                                    border_radius="25px",
                                                    padding="14px 28px",
                                                    font_weight="600",
                                                    font_size="1.05em",
                                                    border="none",
                                                    cursor="pointer",
                                                    box_shadow="0 4px 20px rgba(77, 171, 117, 0.3)",
                                                    transition="all 0.25s ease",
                                                    _hover={
                                                        "background_color": "#3d9a66",
                                                        "transform": "translateY(-2px)",
                                                        "box_shadow": "0 6px 24px rgba(77, 171, 117, 0.5)",
                                                    },
                                                    margin_top="10px",
                                                ),
                                                spacing="4",
                                            ),
                                            on_submit=AppState.signup,
                                            width="100%",
                                        ),
                                        spacing="4",
                                        align="center",
                                        padding="30px 0",
                                        width="100%",
                                    ),
                                    value="signup",
                                ),
                                default_value="login",
                                width="100%",
                            ),

                            # 홈으로 돌아가기 버튼
                            rx.button(
                                "홈으로",
                                on_click=rx.redirect("/"),
                                background_color="transparent",
                                color="#4DAB75",
                                border="1px solid rgba(77, 171, 117, 0.3)",
                                border_radius="25px",
                                padding="10px 28px",
                                font_weight="600",
                                cursor="pointer",
                                transition="all 0.25s ease",
                                _hover={
                                    "background_color": "rgba(77, 171, 117, 0.05)",
                                    "border": "1px solid #4DAB75",
                                },
                                margin_top="20px",
                            ),

                            spacing="4",
                            align="center",
                            padding="60px",
                            width="100%",
                            justify="center",
                        ),
                        width="50%",
                        min_height="500px",
                        display="flex",
                        background="#FFFFFF",
                        border_radius="0 30px 30px 0",
                    ),

                    spacing="0",
                    width="100%",
                    align="stretch",
                ),
                width="100%",
                max_width="850px",
                min_height="500px",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.12)",
                border_radius="30px",
                overflow="hidden",
            ),
            width="100%",
            min_height="100vh",
            padding="40px 20px",
        ),
        width="100%",
        min_height="100vh",
        background="#F8F9FA",
    )

