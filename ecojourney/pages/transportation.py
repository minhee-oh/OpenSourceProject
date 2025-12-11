import reflex as rx
from ..state import AppState

UNITS = ["km", "분"]

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
                        border="1px solid #FFFFFF",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
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
                        _hover={
                            "border": "1px solid #FFFFFF",
                        },
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


# =======================================================
# 공통 버튼 UI
# =======================================================

def transport_button(label: str, is_selected, on_click):
    disabled = AppState.trans_input_mode

    base = rx.hstack(
        rx.text(label),
        spacing="2",
    )

    selected_bg = rx.cond(disabled, "rgba(77, 171, 117, 0.4)", "#4DAB75")
    default_bg  = rx.cond(disabled, "rgba(77, 171, 117, 0.05)", "rgba(77, 171, 117, 0.1)")

    text_color = rx.cond(is_selected, "#FFFFFF", "#4DAB75")
    cursor_style = rx.cond(disabled, "not-allowed", "pointer")

    return rx.button(
        base,
        on_click=rx.cond(disabled, None, on_click),
        disabled=disabled,
        background_color=rx.cond(is_selected, selected_bg, default_bg),
        color=text_color,
        border_radius="30px",
        padding=rx.cond(is_selected, "18px 36px", "16px 32px"),
        border=rx.cond(is_selected, "2px solid #4DAB75", "1px solid rgba(77, 171, 117, 0.3)"),
        font_size="1em",
        font_weight="600",
        cursor=cursor_style,
        transition="all 0.25s ease",
        box_shadow=rx.cond(is_selected, "0 4px 20px rgba(77, 171, 117, 0.3)", "none"),
        _hover=rx.cond(
            disabled,
            {},
            {
                "transform": "translateY(-2px)",
                "background_color": rx.cond(is_selected, "#4DAB75", "rgba(77, 171, 117, 0.2)"),
                "box_shadow": "0 6px 24px rgba(77, 171, 117, 0.4)",
            }
        ),
    )

# =======================================================
# 입력 필드 UI
# =======================================================

def transport_input_field(label: str, value_name: str, unit_name: str):
    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="600",
                min_width="90px",
                color="#333333",
                font_size="1em",
            ),
            rx.select(
                UNITS,
                placeholder="단위",
                name=unit_name,
                width="110px",
                background_color="#FFFFFF",
                color="#333333",
                border_radius="12px",
                border="1px solid #E0E0E0",
                padding="8px 12px",
                font_size="0.95em",
            ),
            rx.input(
                placeholder="거리/시간 입력",
                type="number",
                name=value_name,
                width="150px",
                background_color="#FFFFFF",
                color="#333333",
                border_radius="12px",
                border="1px solid #E0E0E0",
                padding="3px 12px",
                font_size="0.95em",
                _focus={
                    "border": "2px solid #4DAB75",
                    "outline": "none",
                },
                _placeholder={
                    "color": "#999999",
                },
            ),
            spacing="4",
            align="center",
            justify="center",
        ),
        padding="20px 24px",
        border_radius="20px",
        background_color="#FFFFFF",
        border="1px solid #E0E0E0",
        margin_y="12px",
        width="100%",
        max_width="450px",
    )


# =======================================================
# 메인 페이지
# =======================================================

def transportation_page():
    return rx.cond(
        AppState.is_logged_in,
        rx.box(
            header(),
            rx.container(
            rx.vstack(
                rx.heading(
                    "Your Daily Transport",
                    size="9",
                    color="#333333",
                    font_weight="700",
                    letter_spacing="-0.02em",
                ),
                rx.text(
                    "오늘 이용한 교통수단을 모두 선택해주세요",
                    color="#666666",
                    font_size="1.15em",
                    font_weight="400",
                    margin_top="8px",
                ),

                rx.box(height="40px"),

                # ----------------------------------
                # 버튼 선택 영역
                # ----------------------------------
                rx.vstack(
                    rx.hstack(
                        transport_button("자동차", AppState.selected_car, AppState.toggle_car),
                        transport_button("버스", AppState.selected_bus, AppState.toggle_bus),
                        transport_button("지하철", AppState.selected_subway, AppState.toggle_subway),
                        transport_button("걷기", AppState.selected_walk, AppState.toggle_walk),
                        transport_button("자전거", AppState.selected_bike, AppState.toggle_bike),
                        wrap="wrap",
                        justify="center",
                        spacing="3",
                    ),
                    spacing="3",
                ),

                rx.box(height="20px"),

                # ----------------------------------
                # 입력하기 버튼 & 건너뛰기 버튼
                # ----------------------------------
                rx.cond(
                    ~AppState.trans_input_mode,
                    rx.hstack(
                        rx.button(
                            "건너뛰기",
                            on_click=rx.redirect("/input/food"),
                            color="#4DAB75",
                            background_color="transparent",
                            border_radius="30px",
                            padding="18px 48px",
                            border="1px solid rgba(77, 171, 117, 0.3)",
                            font_size="1.05em",
                            font_weight="600",
                            cursor="pointer",
                            transition="all 0.25s ease",
                            _hover={
                                "background_color": "rgba(77, 171, 117, 0.05)",
                                "border": "1px solid #4DAB75",
                            },
                        ),
                        rx.button(
                            "입력하기",
                            on_click=AppState.show_trans_input_fields,
                            color="#FFFFFF",
                            background_color="#4DAB75",
                            border_radius="30px",
                            padding="18px 48px",
                            border="none",
                            font_size="1.05em",
                            font_weight="600",
                            cursor="pointer",
                            box_shadow="0 4px 20px rgba(77, 171, 117, 0.3)",
                            transition="all 0.25s ease",
                            _hover={
                                "background_color": "#3d9a66",
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 6px 24px rgba(77, 171, 117, 0.5)",
                            },
                        ),
                        spacing="4",
                        justify="center",
                    ),
                ),

                rx.box(height="10px"),

                # ----------------------------------
                # 입력 필드 렌더링
                # ----------------------------------
                rx.cond(
                    AppState.trans_input_mode,
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "이용량을 입력해주세요",
                                color="#333333",
                                font_size="1.25em",
                                font_weight="700",
                                margin_bottom="20px",
                            ),

                            rx.cond(AppState.show_car,
                                    transport_input_field("자동차", "car_value", "car_unit")),
                            rx.cond(AppState.show_bus,
                                    transport_input_field("버스", "bus_value", "bus_unit")),
                            rx.cond(AppState.show_subway,
                                    transport_input_field("지하철", "subway_value", "subway_unit")),
                            rx.cond(AppState.show_walk,
                                    transport_input_field("걷기", "walk_value", "walk_unit")),
                            rx.cond(AppState.show_bike,
                                    transport_input_field("자전거", "bike_value", "bike_unit")),

                            rx.box(height="30px"),

                            # 버튼 영역
                            rx.hstack(
                                # 다시 선택하기 버튼
                                rx.button(
                                    "다시 선택하기",
                                    type="button",
                                    on_click=AppState.reset_transport_selection,
                                    color="#4DAB75",
                                    background_color="transparent",
                                    border_radius="30px",
                                    padding="16px 40px",
                                    border="1px solid rgba(77, 171, 117, 0.3)",
                                    font_size="1.05em",
                                    font_weight="600",
                                    cursor="pointer",
                                    transition="all 0.25s ease",
                                    _hover={
                                        "background_color": "rgba(77, 171, 117, 0.05)",
                                        "border": "1px solid #4DAB75",
                                    },
                                ),
                                # 다음 버튼
                                rx.button(
                                    "다음",
                                    type="submit",
                                    color="#FFFFFF",
                                    background_color="#4DAB75",
                                    border_radius="30px",
                                    padding="16px 52px",
                                    border="none",
                                    font_size="1.05em",
                                    font_weight="600",
                                    cursor="pointer",
                                    box_shadow="0 4px 20px rgba(77, 171, 117, 0.3)",
                                    transition="all 0.25s ease",
                                    _hover={
                                        "background_color": "#3d9a66",
                                        "transform": "translateY(-2px)",
                                        "box_shadow": "0 6px 24px rgba(77, 171, 117, 0.5)",
                                    },
                                ),
                                spacing="4",
                                justify="center",
                            ),

                            align="center",
                            width="100%",
                            spacing="2",
                        ),
                        on_submit=AppState.handle_transport_submit,
                    ),
                ),

                spacing="5",
                align="center",
                padding="60px 40px",
            ),
            max_width="900px",
            margin="0 auto",
        ),
        min_height="100vh",
        background="#F8F9FA",
        ),
        rx.box(
            on_mount=rx.redirect("/auth"),
        ),
    )
