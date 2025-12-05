# water.py - 물 입력 페이지 (기능 테스트용)

import reflex as rx
from ..states import AppState

def water_page() -> rx.Component:
    return rx.vstack(
        rx.heading("물 사용 입력", size="8"),
        rx.text("물 사용량을 입력하세요 (여러 활동을 한 번에 입력 가능)", size="4"),
        
        rx.form(
            rx.vstack(
                # 샤워
                rx.hstack(
                    rx.text("샤워", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="횟수",
                        name="water_shower_count",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["회", "분"],
                        placeholder="단위",
                        name="water_shower_unit",
                        default_value="회",
                    ),
                    spacing="3",
                ),
                # 설거지
                rx.hstack(
                    rx.text("설거지", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="횟수",
                        name="water_dish_count",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["회"],
                        placeholder="단위",
                        name="water_dish_unit",
                        default_value="회",
                    ),
                    spacing="3",
                ),
                # 세탁
                rx.hstack(
                    rx.text("세탁", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="횟수",
                        name="water_laundry_count",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["회"],
                        placeholder="단위",
                        name="water_laundry_unit",
                        default_value="회",
                    ),
                    spacing="3",
                ),
                rx.button(
                    "결과 리포트 보기",
                    type="submit",
                    color_scheme="green",
                    size="3",
                ),
                spacing="4",
            ),
            on_submit=AppState.handle_water_submit,
            width="100%",
            max_width="400px",
        ),
        
        rx.text("현재 입력된 활동 수: ", AppState.all_activities.length(), size="2"),
        
        spacing="6",
        padding="4",
        align="center",
    )
