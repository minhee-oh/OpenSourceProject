# waste.py - 쓰레기 입력 페이지 (기능 테스트용)

import reflex as rx
from ..states import AppState

def waste_page() -> rx.Component:
    return rx.vstack(
        rx.heading("쓰레기 입력", size="8"),
        rx.text("쓰레기 배출량을 입력하세요 (여러 종류를 한 번에 입력 가능)", size="4"),
        
        rx.form(
            rx.vstack(
                # 일반
                rx.hstack(
                    rx.text("일반", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="양",
                        name="waste_general_amount",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["kg", "개"],
                        placeholder="단위",
                        name="waste_general_unit",
                        default_value="kg",
                    ),
                    spacing="3",
                ),
                # 플라스틱
                rx.hstack(
                    rx.text("플라스틱", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="양",
                        name="waste_plastic_amount",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["kg", "개"],
                        placeholder="단위",
                        name="waste_plastic_unit",
                        default_value="kg",
                    ),
                    spacing="3",
                ),
                # 종이
                rx.hstack(
                    rx.text("종이", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="양",
                        name="waste_paper_amount",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["kg", "개"],
                        placeholder="단위",
                        name="waste_paper_unit",
                        default_value="kg",
                    ),
                    spacing="3",
                ),
                # 유리
                rx.hstack(
                    rx.text("유리", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="양",
                        name="waste_glass_amount",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["kg", "개"],
                        placeholder="단위",
                        name="waste_glass_unit",
                        default_value="kg",
                    ),
                    spacing="3",
                ),
                # 캔
                rx.hstack(
                    rx.text("캔", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="양",
                        name="waste_can_amount",
                        step="0.1",
                        min="0",
                    ),
                    rx.select(
                        ["kg", "개"],
                        placeholder="단위",
                        name="waste_can_unit",
                        default_value="kg",
                    ),
                    spacing="3",
                ),
                rx.button(
                    "다음 (물)",
                    type="submit",
                    color_scheme="green",
                    size="3",
                ),
                spacing="4",
            ),
            on_submit=AppState.handle_waste_submit,
            width="100%",
            max_width="400px",
        ),
        
        rx.text("현재 입력된 활동 수: ", AppState.all_activities.length(), size="2"),
        
        spacing="6",
        padding="4",
        align="center",
    )
