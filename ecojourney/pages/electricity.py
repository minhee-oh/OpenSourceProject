# electricity.py - 전기 입력 페이지 (기능 테스트용)

import reflex as rx
from ..states import AppState

def electricity_page() -> rx.Component:
    return rx.vstack(
        rx.heading("전기 사용 입력", size="8"),
        rx.text("전기 사용량을 입력하세요 (여러 기기를 한 번에 입력 가능)", size="4"),
        
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.text("냉방기", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="사용 시간 (시간)",
                        name="cooling_hours",
                        step="0.1",
                        min="0",
                    ),
                    spacing="3",
                ),
                rx.hstack(
                    rx.text("난방기", width="80px"),
                    rx.input(
                        type="number",
                        placeholder="사용 시간 (시간)",
                        name="heating_hours",
                        step="0.1",
                        min="0",
                    ),
                    spacing="3",
                ),
                rx.button(
                    "다음 (쓰레기)",
                    type="submit",
                    color_scheme="green",
                    size="3",
                ),
                spacing="4",
            ),
            on_submit=AppState.handle_electricity_submit,
            width="100%",
            max_width="400px",
        ),
        
        rx.text("현재 입력된 활동 수: ", AppState.all_activities.length(), size="2"),
        
        spacing="6",
        padding="4",
        align="center",
    )
