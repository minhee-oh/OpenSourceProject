# food.py

import reflex as rx
from ..state import AppState

FOOD_SUBCATEGORIES = {
    "고기류": ["소고기", "돼지고기", "닭고기"],
    "채소류": ["양파", "파", "마늘"],
    "유제품류": ["우유", "치즈"],
    "쌀밥": [],  # 쌀밥은 하위 카테고리 없음
    "커피": ["아메리카노", "카페라떼"],  # 커피 하위 카테고리
}
UNITS = ["g", "ml", "회"]

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

def background_video() -> rx.Component:
    """순수 HTML5 <video> 태그를 사용하여 자동 재생을 강제하고 레이어를 안정화합니다."""
    return rx.box(
        # 💡 rx.html을 사용하여 필수 속성을 가진 순수 HTML 태그를 삽입
        rx.html(
            # src 경로가 정확한지 확인하면서, 필수 속성(autoplay, loop, muted, playsinline)을 강제합니다.
            """
            <video autoplay loop muted playsinline 
                src="/transportation_background.mp4" 
                style='
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    object-position: center bottom;
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

# =======================================================
# 공통 버튼 UI
# =======================================================

def food_button(label: str, is_selected, on_click):

    # 🔥 input_mode 상태를 가져옴 (Var 그대로)
    disabled = AppState.food_input_mode

    base = rx.hstack(
        rx.text(label),
        spacing="2",
    )

    # 🔥 스타일도 rx.cond 로 처리해야 함
    selected_bg = rx.cond(disabled, "rgba(0,0,0,0.2)", "rgba(0,0,0,0.52)")
    default_bg  = rx.cond(disabled, "rgba(0,0,0,0.1)", "rgba(0,0,0,0.22)")

    cursor_style = rx.cond(disabled, "not-allowed", "pointer")

    return rx.button(
        base,
        # 🔥 클릭 비활성화 → on_click 제거 조건화
        on_click=rx.cond(disabled, None, on_click),

        disabled=disabled,  # 🔥 Reflex는 disabled에 Var 허용

        # 🔥 선택 여부에 따른 스타일
        background_color=rx.cond(is_selected, selected_bg, default_bg),

        border_radius="40px",
        padding=rx.cond(is_selected, "27px 40px", "24px 40px"),
        border="4px solid rgba(255, 255, 255, 0.5)",
        font_size="1.1em",
        font_weight="bold",
        cursor=cursor_style,
        transition="all 0.2s ease",
    )

# =======================================================
# 입력 필드 UI
# =======================================================

def food_input_field(label: str, value_name: str, unit_name: str, sub_name: str):
    sub_items = FOOD_SUBCATEGORIES.get(label, [])
    has_subcategories = len(sub_items) > 0

    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="bold",
                min_width="80px",
                color="black",       # ← 여기만 바꾸면 바로 해결됨
            ),
            rx.cond(
                has_subcategories,
                rx.select(
                    items=sub_items,
                    placeholder=f"세부 카테고리 선택",
                    name=sub_name,
                    width="140px",
                    background_color="rgba(255, 255, 255, 0.9)",
                    color="black",
                    border_radius="8px",
                ),
                rx.box(width="140px"),  # 하위 카테고리가 없으면 빈 공간
            ),
            rx.select(
                UNITS,
                placeholder="단위",
                name=unit_name,
                width="100px",
                background_color="rgba(255, 255, 255, 0.9)",
                color="black",
                border_radius="8px",
            ),
            rx.input(
                placeholder="섭취량/횟수 입력",
                type="number",
                name=value_name,
                width="140px",
                background_color="rgba(255, 255, 255, 0.9)",
                color="black",
                border_radius="8px",
            ),
            spacing="4",
            align="center",
            justify="center",
        ),
        padding="16px 20px",
        border_radius="16px",
        background_color="rgba(0, 0, 0, 0.1)",
        border="2px solid rgba(0, 0, 0, 0.2)",
        margin_y="10px",
        width="100%",
        max_width="550px",
    )


# =======================================================
# 메인 페이지
# =======================================================

def food_page():
    return rx.box(
        background_video(),
        header(),
        rx.container(
            rx.vstack(
                rx.heading("음식 선택", size="7", color="white"),
                rx.text(
                    "오늘 섭취한 음식을 모두 선택해주세요",
                    color="rgba(255, 255, 255, 0.8)",
                    font_size="1.1em",
                ),

                rx.box(height="30px"),

                # ----------------------------------
                # 버튼 선택 영역
                # ----------------------------------
                rx.vstack(
                    rx.hstack(
                        food_button("고기류", AppState.selected_meat, AppState.toggle_meat),
                        food_button("채소류", AppState.selected_veg, AppState.toggle_veg),
                        food_button("유제품류", AppState.selected_dairy, AppState.toggle_dairy),
                        food_button("쌀밥", AppState.selected_rice, AppState.toggle_rice),
                        food_button("커피", AppState.selected_coffee, AppState.toggle_coffee),
                        wrap="nowrap",
                        justify="center",
                        spacing="3",
                    ),
                    spacing="3",
                ),

                rx.box(),

                # ----------------------------------
                # 입력하기 버튼
                # ----------------------------------
                rx.cond(
                    ~AppState.food_input_mode,
                    rx.button(
                        "입력하기",
                        on_click=AppState.show_food_input_fields,
                        color="black",
                        background_color="rgba(34,139,34,0.7)",
                        border_radius="40px",
                        padding="24px 45px",
                        border="4px solid rgba(255,255,255,0.2)",
                        font_size="1.1em",
                        font_weight="600",
                        cursor="pointer",
                        _hover={"background_color": "rgba(34,139,34,0.9)"},
                    ),
                ),

                rx.box(),

                # ----------------------------------
                # 입력 필드 렌더링
                # ----------------------------------
                rx.cond(
                    AppState.food_input_mode,
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "섭취량을 입력해주세요",
                                color="black",
                                font_size="1.2em",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),

                            rx.cond(AppState.show_meat,
                                food_input_field("고기류", "meat_value", "meat_unit", "meat_sub")),
                            rx.cond(AppState.show_veg,
                                food_input_field("채소류", "veg_value", "veg_unit", "veg_sub")),
                            rx.cond(AppState.show_dairy,
                                food_input_field("유제품류", "dairy_value", "dairy_unit", "dairy_sub")),
                            rx.cond(AppState.show_rice,
                                food_input_field("쌀밥", "rice_value", "rice_unit", "rice_sub")),
                            rx.cond(AppState.show_coffee,
                                food_input_field("커피", "coffee_value", "coffee_unit", "coffee_sub")),

                            rx.box(height="20px"),

                            # 다음 버튼
                            rx.button(
                                "다음",
                                type="submit",
                                color="black",
                                background_color="rgba(34,139,34,0.7)",
                                border_radius="40px",
                                padding="20px 50px",
                                border="4px solid rgba(255,255,255,0.2)",
                                font_size="1.1em",
                                font_weight="600",
                                cursor="pointer",
                                _hover={"background_color": "rgba(34,139,34,0.9)"},
                            ),

                            align="center",
                            width="100%",
                            spacing="2",
                        ),
                        on_submit=AppState.handle_food_submit,
                    ),
                ),

                spacing="4",
                align="center",
                padding="40px",
            ),
            max_width="800px",
            margin="0 auto",
        ),
    )
