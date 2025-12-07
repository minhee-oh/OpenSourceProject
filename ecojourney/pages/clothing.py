# clothing.py - 의류 입력 페이지

import reflex as rx
from ..states import AppState

def clothing_input_field(label: str, count_name: str, vintage_name: str):
    """의류 입력 필드 (개수 + 새제품/빈티지 선택)"""
    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="bold",
                min_width="100px",
                color="black",
            ),
            rx.input(
                type="number",
                placeholder="개수",
                name=count_name,
                step="1",
                min="0",
                width="120px",
                background_color="rgba(255, 255, 255, 0.9)",
                color="black",
                border_radius="8px",
            ),
            rx.select(
                ["새제품", "빈티지"],
                placeholder="선택",
                name=vintage_name,
                width="120px",
                background_color="rgba(255, 255, 255, 0.9)",
                color="black",
                border_radius="8px",
            ),
            spacing="4",
            align="center",
            justify="center",
        ),
        padding="12px 16px",
        border_radius="12px",
        background_color="rgba(0, 0, 0, 0.05)",
        border="1px solid rgba(0, 0, 0, 0.1)",
        margin_y="8px",
        width="100%",
        max_width="500px",
    )

def clothing_page() -> rx.Component:
    return rx.vstack(
        rx.heading("의류 입력", size="8"),
        rx.text("의류 구매 정보를 입력하세요 (새제품/빈티지 구분)", size="4"),
        
        rx.form(
            rx.vstack(
                clothing_input_field("상의", "top_count", "top_vintage"),
                clothing_input_field("하의", "bottom_count", "bottom_vintage"),
                clothing_input_field("신발", "shoes_count", "shoes_vintage"),
                clothing_input_field("가방/잡화", "bag_count", "bag_vintage"),
                
                rx.button(
                    "다음 (전기)",
                    type="submit",
                    color_scheme="green",
                    size="3",
                    margin_top="20px",
                ),
                spacing="4",
                align="center",
            ),
            on_submit=AppState.handle_clothing_submit,
            width="100%",
            max_width="500px",
        ),
        
        rx.text("현재 입력된 활동 수: ", AppState.all_activities.length(), size="2"),
        
        spacing="6",
        padding="4",
        align="center",
    )
