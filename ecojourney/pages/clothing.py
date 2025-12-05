# clothing.py - 의류 입력 페이지 (기능 테스트용)

import reflex as rx
from ..states import AppState

def clothing_page() -> rx.Component:
    return rx.vstack(
        rx.heading("의류 입력", size="8"),
        rx.text("의류 구매 정보를 입력하세요", size="4"),
        
        rx.form(
            rx.vstack(
                # 상의
                rx.hstack(
                    rx.text("상의", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="개수",
                        name="top_count",
                        step="1",
                        min="0",
                    ),
                    spacing="3",
                ),
                # 하의
                rx.hstack(
                    rx.text("하의", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="개수",
                        name="bottom_count",
                        step="1",
                        min="0",
                    ),
                    spacing="3",
                ),
                # 신발
                rx.hstack(
                    rx.text("신발", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="개수",
                        name="shoes_count",
                        step="1",
                        min="0",
                    ),
                    spacing="3",
                ),
                # 가방/잡화
                rx.hstack(
                    rx.text("가방/잡화", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="개수",
                        name="bag_count",
                        step="1",
                        min="0",
                    ),
                    spacing="3",
                ),
                rx.button(
                    "다음 (전기)",
                    type="submit",
                    color_scheme="green",
                    size="3",
                ),
                spacing="4",
            ),
            on_submit=AppState.handle_clothing_submit,
            width="100%",
            max_width="400px",
        ),
        
        rx.text("현재 입력된 활동 수: ", AppState.all_activities.length(), size="2"),
        
        spacing="6",
        padding="4",
        align="center",
    )
