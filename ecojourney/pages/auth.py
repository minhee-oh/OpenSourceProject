# auth.py - 로그인 및 회원가입 페이지

import reflex as rx
from ecojourney.state import AppState

def auth_page() -> rx.Component:
    """로그인 및 회원가입 페이지"""
    return rx.center(
        rx.vstack(
            rx.heading("EcoJourney", size="8", color="white", margin_bottom="30px"),
            
            # 로그인/회원가입 탭
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("로그인", value="login"),
                    rx.tabs.trigger("회원가입", value="signup"),
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
                                ),
                                rx.input(
                                    type="password",
                                    placeholder="비밀번호",
                                    name="password",
                                    value=AppState.login_password,
                                    on_change=AppState.set_login_password,
                                    size="3",
                                    width="100%",
                                ),
                                rx.cond(
                                    AppState.auth_error_message != "",
                                    rx.text(
                                        AppState.auth_error_message,
                                        color="red.400",
                                        size="2",
                                        margin_top="10px",
                                    ),
                                ),
                                rx.button(
                                    "로그인",
                                    type="submit",
                                    color_scheme="green",
                                    size="3",
                                    width="100%",
                                    margin_top="10px",
                                ),
                                spacing="4",
                            ),
                            on_submit=AppState.login,
                            width="100%",
                            max_width="400px",
                        ),
                        spacing="4",
                        align="center",
                        padding="20px",
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
                                ),
                                rx.input(
                                    type="password",
                                    placeholder="비밀번호",
                                    name="password",
                                    value=AppState.signup_password,
                                    on_change=AppState.set_signup_password,
                                    size="3",
                                    width="100%",
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
                                ),
                                rx.cond(
                                    AppState.auth_error_message != "",
                                    rx.text(
                                        AppState.auth_error_message,
                                        color="red.400",
                                        size="2",
                                        margin_top="10px",
                                    ),
                                ),
                                rx.button(
                                    "회원가입",
                                    type="submit",
                                    color_scheme="blue",
                                    size="3",
                                    width="100%",
                                    margin_top="10px",
                                ),
                                spacing="4",
                            ),
                            on_submit=AppState.signup,
                            width="100%",
                            max_width="400px",
                        ),
                        spacing="4",
                        align="center",
                        padding="20px",
                    ),
                    value="signup",
                ),
                default_value="login",
                width="100%",
                max_width="500px",
            ),
            
            # 홈으로 돌아가기 버튼
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
        ),
        width="100%",
        min_height="100vh",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    )

