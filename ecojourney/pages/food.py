# food.py

import reflex as rx
from ..state import AppState

FOOD_SUBCATEGORIES = {
    "유제품": ["우유", "치즈", "두유"],
    "밥": ["쌀밥", "잡곡밥", "현미밥", "보리밥", "콩밥", "김밥", "비빔밥불고기", "비빔밥산채", "김치볶음밥"],
    "커피": ["에스프레소", "카페라떼"],  # 한국일보 기준만
    "패스트푸드": ["피자", "햄버거세트", "후라이드치킨"],  # 한국일보 기준만
    "면": ["물냉면", "비빔냉면", "잔치국수", "비빔국수", "해물칼국수"],  # 한국일보 기준만
    "국/찌개": ["된장국", "미역국", "콩나물국", "된장찌개", "김치찌개", "순두부찌개", "설렁탕", "갈비탕", "곰탕"],  # 한국일보 기준만
    "반찬": ["배추김치", "깍두기", "총각김치", "열무김치", "숙주나물", "콩나물무침", "시금치나물", "무생채", "소고기장조림", "멸치조림", "콩자반", "깻잎장아찌", "제육볶음", "오징어볶음", "불고기", "잡채", "고등어구이", "달걀프라이", "달걀찜"],
    "고기": ["소고기구이", "삼겹살구이"],
    "과일": ["딸기", "참외", "수박", "사과", "복숭아", "단감", "포도", "감귤", "키위", "토마토", "방울토마토"],
    # Climatiq API 사용 항목
    "파스타": ["카르보나라", "라자냐", "라비올리", "파스타샐러드"],  # Climatiq API 사용 (완성된 요리만)
}

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

def food_button(label: str, is_selected, on_click):
    """상위 카테고리 선택 버튼"""
    disabled = AppState.food_input_mode

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

def subcategory_checkbox(category: str, subcategory: str, selected_list):
    """세부 카테고리 체크박스"""
    return rx.hstack(
        rx.checkbox(
            checked=selected_list.contains(subcategory),
            on_change=lambda: AppState.toggle_food_subcategory(category, subcategory),
            color_scheme="green",
        ),
        rx.text(
            subcategory,
            font_size="0.95em",
            color="#2d3e2d",
        ),
        spacing="2",
        align="center",
        padding="10px 16px",
        border_radius="12px",
        background_color="white",
        border="2px solid #d0d8d0",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background_color": "#f5f7f5",
            "border": "2px solid #3d5a3d",
        },
        on_click=lambda: AppState.toggle_food_subcategory(category, subcategory),
    )

def subcategory_selection_section(label: str, subcategories: list, selected_list):
    """세부 카테고리 선택 섹션 (체크박스 형태)"""
    return rx.vstack(
        rx.text(
            label,
            font_weight="700",
            font_size="1.15em",
            color="#2d3e2d",
            margin_bottom="12px",
        ),
        rx.hstack(
            *[subcategory_checkbox(label, sub, selected_list) for sub in subcategories],
            wrap="wrap",
            spacing="3",
            justify="start",
        ),
        spacing="2",
        align="start",
        width="100%",
        padding="20px",
        border_radius="20px",
        background_color="rgba(255, 255, 255, 0.5)",
        border="2px solid #e0e8e0",
        margin_y="12px",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.06)",
    )

def quantity_input_field(category_key: str, subcategory: str):
    """횟수 입력 필드 (개별 세부 카테고리용)"""
    return rx.box(
        rx.hstack(
            rx.text(
                subcategory,
                font_weight="600",
                min_width="120px",
                color="#2d3e2d",
            ),
            rx.input(
                placeholder="횟수 입력",
                type="number",
                name=f"{category_key}_{subcategory}_value",
                width="150px",
                background_color="white",
                color="#2d3e2d",
                border_radius="12px",
                border="2px solid #d0d8d0",
                padding="3px 12px",
                _focus={
                    "border": "2px solid #3d5a3d",
                    "outline": "none",
                },
            ),
            rx.text(
                "회",
                min_width="40px",
                color="#2d3e2d",
                font_weight="600",
                text_align="center",
            ),
            spacing="4",
            align="center",
            justify="center",
            padding="16px 20px",
            border_radius="16px",
            background_color="white",
            border="2px solid #e0e8e0",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.06)",
        ),
        display="flex",
        justify_content="center",
        width="100%",
        margin_y="8px",
    )


# =======================================================
# 메인 페이지
# =======================================================

def food_page():
    return rx.box(
        header(),
        rx.container(
            rx.vstack(
                rx.heading(
                    "Your Daily Food",
                    size="9",
                    color="#2d3e2d",
                    font_weight="700",
                    letter_spacing="-0.02em",
                ),
                rx.text(
                    "오늘 섭취한 식품을 모두 선택해주세요",
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
                        food_button("유제품", AppState.selected_dairy, AppState.toggle_dairy),
                        food_button("밥", AppState.selected_rice, AppState.toggle_rice),
                        food_button("커피", AppState.selected_coffee, AppState.toggle_coffee),
                        food_button("패스트푸드", AppState.selected_fastfood, AppState.toggle_fastfood),
                        food_button("면", AppState.selected_noodles, AppState.toggle_noodles),
                        food_button("국/찌개", AppState.selected_cooked, AppState.toggle_cooked),
                        food_button("반찬", AppState.selected_side_dish, AppState.toggle_side_dish),
                        food_button("고기", AppState.selected_grilled_meat, AppState.toggle_grilled_meat),
                        food_button("과일", AppState.selected_fruit, AppState.toggle_fruit),
                        food_button("파스타", AppState.selected_pasta, AppState.toggle_pasta),
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
                    ~AppState.food_input_mode,
                    rx.hstack(
                        rx.button(
                            "건너뛰기",
                            on_click=rx.redirect("/input/clothing"),
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
                            on_click=AppState.show_food_input_fields,
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
                # 1단계: 세부 카테고리 선택
                # ----------------------------------
                rx.cond(
                    AppState.food_step == 1,
                    rx.vstack(
                        rx.text(
                            "세부 카테고리를 선택해주세요",
                            color="#2d3e2d",
                            font_size="1.25em",
                            font_weight="700",
                            margin_bottom="20px",
                        ),

                        # 유제품 세부 카테고리 선택
                        rx.cond(AppState.show_dairy,
                            subcategory_selection_section("유제품", FOOD_SUBCATEGORIES["유제품"], AppState.selected_dairy_subs)),

                        # 밥 세부 카테고리 선택
                        rx.cond(AppState.show_rice,
                            subcategory_selection_section("밥", FOOD_SUBCATEGORIES["밥"], AppState.selected_rice_subs)),

                        # 커피 세부 카테고리 선택
                        rx.cond(AppState.show_coffee,
                            subcategory_selection_section("커피", FOOD_SUBCATEGORIES["커피"], AppState.selected_coffee_subs)),

                        # 패스트푸드 세부 카테고리 선택
                        rx.cond(AppState.show_fastfood,
                            subcategory_selection_section("패스트푸드", FOOD_SUBCATEGORIES["패스트푸드"], AppState.selected_fastfood_subs)),

                        # 면 세부 카테고리 선택
                        rx.cond(AppState.show_noodles,
                            subcategory_selection_section("면", FOOD_SUBCATEGORIES["면"], AppState.selected_noodles_subs)),

                        # 국/찌개 세부 카테고리 선택
                        rx.cond(AppState.show_cooked,
                            subcategory_selection_section("국/찌개", FOOD_SUBCATEGORIES["국/찌개"], AppState.selected_cooked_subs)),

                        # 반찬 세부 카테고리 선택
                        rx.cond(AppState.show_side_dish,
                            subcategory_selection_section("반찬", FOOD_SUBCATEGORIES["반찬"], AppState.selected_side_dish_subs)),

                        # 고기 세부 카테고리 선택
                        rx.cond(AppState.show_grilled_meat,
                            subcategory_selection_section("고기", FOOD_SUBCATEGORIES["고기"], AppState.selected_grilled_meat_subs)),

                        # 과일 세부 카테고리 선택
                        rx.cond(AppState.show_fruit,
                            subcategory_selection_section("과일", FOOD_SUBCATEGORIES["과일"], AppState.selected_fruit_subs)),

                        # 파스타 세부 카테고리 선택
                        rx.cond(AppState.show_pasta,
                            subcategory_selection_section("파스타", FOOD_SUBCATEGORIES["파스타"], AppState.selected_pasta_subs)),

                        rx.box(height="30px"),

                        # 버튼 영역
                        rx.hstack(
                            # 다시 선택하기 버튼
                            rx.button(
                                "다시 선택하기",
                                type="button",
                                on_click=AppState.reset_food_selection,
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
                                type="button",
                                on_click=AppState.proceed_to_quantity_input,
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
                        spacing="3",
                        padding="20px",
                    ),
                ),

                # ----------------------------------
                # 2단계: 횟수 입력
                # ----------------------------------
                rx.cond(
                    AppState.food_step == 2,
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "섭취 횟수를 입력해주세요",
                                color="#2d3e2d",
                                font_size="1.25em",
                                font_weight="700",
                                margin_bottom="20px",
                            ),

                            # 유제품 횟수 입력
                            rx.cond(AppState.show_dairy,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_dairy_subs,
                                        lambda sub: quantity_input_field("dairy", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 밥 횟수 입력
                            rx.cond(AppState.show_rice,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_rice_subs,
                                        lambda sub: quantity_input_field("rice", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 커피 횟수 입력
                            rx.cond(AppState.show_coffee,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_coffee_subs,
                                        lambda sub: quantity_input_field("coffee", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 패스트푸드 횟수 입력
                            rx.cond(AppState.show_fastfood,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_fastfood_subs,
                                        lambda sub: quantity_input_field("fastfood", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 면 횟수 입력
                            rx.cond(AppState.show_noodles,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_noodles_subs,
                                        lambda sub: quantity_input_field("noodles", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 국/찌개 횟수 입력
                            rx.cond(AppState.show_cooked,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_cooked_subs,
                                        lambda sub: quantity_input_field("cooked", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 반찬 횟수 입력
                            rx.cond(AppState.show_side_dish,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_side_dish_subs,
                                        lambda sub: quantity_input_field("side_dish", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 고기 횟수 입력
                            rx.cond(AppState.show_grilled_meat,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_grilled_meat_subs,
                                        lambda sub: quantity_input_field("grilled_meat", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 과일 횟수 입력
                            rx.cond(AppState.show_fruit,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_fruit_subs,
                                        lambda sub: quantity_input_field("fruit", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            # 파스타 횟수 입력
                            rx.cond(AppState.show_pasta,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_pasta_subs,
                                        lambda sub: quantity_input_field("pasta", sub)
                                    ),
                                    spacing="2",
                                    width="100%",
                                )),

                            rx.box(height="30px"),

                            # 버튼 영역
                            rx.hstack(
                                # 다시 선택하기 버튼
                                rx.button(
                                    "다시 선택하기",
                                    type="button",
                                    on_click=AppState.reset_food_selection,
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
                                # 제출 버튼
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
                            spacing="3",
                            padding="20px",
                        ),
                        on_submit=AppState.handle_food_submit,
                    ),
                ),

                spacing="5",
                align="center",
                padding="60px 40px",
            ),
            max_width="1000px",
            margin="0 auto",
        ),
        min_height="100vh",
        background="linear-gradient(135deg, #f5f7f5 0%, #e8ede8 50%, #d8e3d8 100%)",
    )
