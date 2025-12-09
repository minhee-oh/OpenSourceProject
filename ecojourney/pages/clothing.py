# clothing.py

import reflex as rx
from ..state import AppState

CLOTHING_SUBCATEGORIES = ["새제품", "빈티지"]

def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.button(
                "EcoJourney",
                on_click=rx.redirect("/"),
                background_color="transparent",
                color="#2d3e2d",
                font_size="1.5em",
                font_weight="bold",
                padding="0",
                border="none",
                cursor="pointer",
                _hover={
                    "color": "#1a5f1a",
                },
            ),
            rx.hstack(
                rx.cond(
                    AppState.is_logged_in,
                    rx.hstack(
                        rx.text(
                            f"{AppState.current_user_id}님",
                            color="#2d3e2d",
                            font_size="0.95em",
                            font_weight="500",
                        ),
                        rx.button(
                            "마이페이지",
                            on_click=rx.redirect("/mypage"),
                            background_color="transparent",
                            color="#2d3e2d",
                            border="none",
                            padding="8px 16px",
                            font_size="0.95em",
                            font_weight="500",
                            cursor="pointer",
                            _hover={
                                "color": "#1a5f1a",
                            },
                        ),
                        rx.button(
                            "로그아웃",
                            on_click=AppState.logout,
                            background_color="transparent",
                            color="#2d3e2d",
                            border="2px solid #2d3e2d",
                            border_radius="25px",
                            padding="8px 24px",
                            font_size="0.95em",
                            font_weight="500",
                            cursor="pointer",
                            _hover={
                                "background_color": "#2d3e2d",
                                "color": "white",
                            },
                        ),
                        spacing="4",
                        align="center",
                    ),
                    rx.button(
                        "로그인",
                        on_click=rx.redirect("/auth"),
                        background_color="transparent",
                        color="#2d3e2d",
                        border="2px solid #2d3e2d",
                        border_radius="25px",
                        padding="8px 24px",
                        font_size="0.95em",
                        font_weight="500",
                        cursor="pointer",
                        _hover={
                            "background_color": "#2d3e2d",
                            "color": "white",
                        },
                    ),
                ),
                spacing="3",
                align="center",
            ),
            justify="between",
            align="center",
            padding="1.2em 3em",
        ),
        width="100%",
        position="relative",
        z_index="10",
        background_color="#f5f7f5",
    )


# =======================================================
# 공통 버튼 UI
# =======================================================

def clothing_button(label: str, is_selected, on_click):
    disabled = AppState.clothing_input_mode

    base = rx.hstack(
        rx.text(label),
        spacing="2",
    )

    selected_bg = rx.cond(disabled, "#c4d8c4", "#3d5a3d")
    default_bg  = rx.cond(disabled, "#e8ede8", "#f5f7f5")

    text_color = rx.cond(is_selected, "white", "#2d3e2d")
    cursor_style = rx.cond(disabled, "not-allowed", "pointer")

    return rx.button(
        base,
        on_click=rx.cond(disabled, None, on_click),
        disabled=disabled,
        background_color=rx.cond(is_selected, selected_bg, default_bg),
        color=text_color,
        border_radius="30px",
        padding=rx.cond(is_selected, "18px 36px", "16px 32px"),
        border=rx.cond(is_selected, "3px solid #2d4a2d", "2px solid #d0d8d0"),
        font_size="1em",
        font_weight="600",
        cursor=cursor_style,
        transition="all 0.25s ease",
        box_shadow=rx.cond(is_selected, "0 4px 12px rgba(61, 90, 61, 0.3)", "0 2px 6px rgba(0, 0, 0, 0.08)"),
        _hover=rx.cond(
            disabled,
            {},
            {
                "transform": "translateY(-2px)",
                "box_shadow": "0 6px 16px rgba(61, 90, 61, 0.25)",
            }
        ),
    )

# =======================================================
# 입력 필드 UI
# =======================================================

def clothing_input_field(label: str, value_name: str, unit_name: str, sub_name: str):
    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="600",
                min_width="90px",
                color="#2d3e2d",
                font_size="1em",
            ),
            rx.select(
                CLOTHING_SUBCATEGORIES,
                placeholder=f"옵션 선택",
                name=sub_name,
                width="130px",
                background_color="white",
                color="#2d3e2d",
                border_radius="12px",
                border="2px solid #d0d8d0",
                padding="8px 12px",
                font_size="0.95em",
            ),
            rx.input(
                placeholder="개수 입력",
                type="number",
                name=value_name,
                width="150px",
                background_color="white",
                color="#2d3e2d",
                border_radius="12px",
                border="2px solid #d0d8d0",
                padding="3px 12px",
                font_size="0.95em",
                _focus={
                    "border": "2px solid #3d5a3d",
                    "outline": "none",
                },
            ),
            spacing="4",
            align="center",
            justify="center",
        ),
        padding="20px 24px",
        border_radius="20px",
        background_color="white",
        border="2px solid #e0e8e0",
        margin_y="12px",
        width="100%",
        max_width="500px",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.06)",
    )


# =======================================================
# 메인 페이지
# =======================================================

def clothing_page():
    return rx.box(
        header(),
        rx.container(
            rx.vstack(
                rx.heading(
                    "Your Clothing Choices",
                    size="9",
                    color="#2d3e2d",
                    font_weight="700",
                    letter_spacing="-0.02em",
                ),
                rx.text(
                    "오늘 구매한 의류를 모두 선택해주세요",
                    color="#5a6d5a",
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
                        clothing_button("티셔츠", AppState.selected_tshirts, AppState.toggle_tshirts),
                        clothing_button("청바지", AppState.selected_jeans, AppState.toggle_jeans),
                        clothing_button("신발", AppState.selected_shoes, AppState.toggle_shoes),
                        clothing_button("가방/잡화", AppState.selected_acc, AppState.toggle_acc),
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
                    ~AppState.clothing_input_mode,
                    rx.hstack(
                        rx.button(
                            "건너뛰기",
                            on_click=rx.redirect("/input/electricity"),
                            color="#2d3e2d",
                            background_color="transparent",
                            border_radius="30px",
                            padding="18px 48px",
                            border="2px solid #d0d8d0",
                            font_size="1.05em",
                            font_weight="600",
                            cursor="pointer",
                            transition="all 0.25s ease",
                            _hover={
                                "background_color": "#f5f7f5",
                                "border": "2px solid #3d5a3d",
                            },
                        ),
                        rx.button(
                            "입력하기",
                            on_click=AppState.show_clothing_input_fields,
                            color="white",
                            background_color="#3d5a3d",
                            border_radius="30px",
                            padding="18px 48px",
                            border="none",
                            font_size="1.05em",
                            font_weight="600",
                            cursor="pointer",
                            box_shadow="0 4px 12px rgba(61, 90, 61, 0.3)",
                            transition="all 0.25s ease",
                            _hover={
                                "background_color": "#2d4a2d",
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 6px 16px rgba(61, 90, 61, 0.4)",
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
                    AppState.clothing_input_mode,
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "구매수를 입력해주세요",
                                color="#2d3e2d",
                                font_size="1.25em",
                                font_weight="700",
                                margin_bottom="20px",
                            ),

                            rx.cond(AppState.show_tshirts,
                                clothing_input_field("티셔츠", "tshirts_value", "tshirts_unit", "tshirts_sub")),
                            rx.cond(AppState.show_jeans,
                                clothing_input_field("청바지", "jeans_value", "jeans_unit", "jeans_sub")),
                            rx.cond(AppState.show_shoes,
                                clothing_input_field("신발", "shoes_value", "shoes_unit", "shoes_sub")),
                            rx.cond(AppState.show_acc,
                                clothing_input_field("가방/잡화", "acc_value", "acc_unit", "acc_sub")),

                            rx.box(height="30px"),

                            # 버튼 영역
                            rx.hstack(
                                # 다시 선택하기 버튼
                                rx.button(
                                    "다시 선택하기",
                                    type="button",
                                    on_click=AppState.reset_clothing_selection,
                                    color="#2d3e2d",
                                    background_color="transparent",
                                    border_radius="30px",
                                    padding="16px 40px",
                                    border="2px solid #d0d8d0",
                                    font_size="1.05em",
                                    font_weight="600",
                                    cursor="pointer",
                                    transition="all 0.25s ease",
                                    _hover={
                                        "background_color": "#f5f7f5",
                                        "border": "2px solid #3d5a3d",
                                    },
                                ),
                                # 다음 버튼
                                rx.button(
                                    "다음",
                                    type="submit",
                                    color="white",
                                    background_color="#3d5a3d",
                                    border_radius="30px",
                                    padding="16px 52px",
                                    border="none",
                                    font_size="1.05em",
                                    font_weight="600",
                                    cursor="pointer",
                                    box_shadow="0 4px 12px rgba(61, 90, 61, 0.3)",
                                    transition="all 0.25s ease",
                                    _hover={
                                        "background_color": "#2d4a2d",
                                        "transform": "translateY(-2px)",
                                        "box_shadow": "0 6px 16px rgba(61, 90, 61, 0.4)",
                                    },
                                ),
                                spacing="4",
                                justify="center",
                            ),

                            align="center",
                            width="100%",
                            spacing="2",
                        ),
                        on_submit=AppState.handle_clothing_submit,
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
        background="linear-gradient(135deg, #f5f7f5 0%, #e8ede8 50%, #d8e3d8 100%)",
    )
