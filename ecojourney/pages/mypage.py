# mypage.py - 마이페이지

import reflex as rx
from ecojourney.state import AppState

# -----------------------------------------
# 공통 헤더
# -----------------------------------------
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
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"border": "1px solid #FFFFFF"},
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
                        border="1px solid #FFFFFF",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
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


# -----------------------------------------
# ① 내 포인트 섹션
# -----------------------------------------
def render_points_section():
    return rx.vstack(
        rx.heading("내 포인트", size="8", color="#333333"),

        rx.box(
            rx.vstack(
                rx.heading("현재 보유 포인트", size="6", color="#333333"),
                rx.text(
                    f"{AppState.current_user_points:,}점",
                    size="9",
                    color="yellow.300",
                    font_weight="bold",
                ),
                rx.text(
                    f"단과대: {AppState.current_user_college}",
                    size="3",
                    color="gray.300",
                ),
                spacing="2",
                align="center",
            ),
            padding="30px",
            border_radius="16px",
            background="#F1F3F4",
            width="100%",
            max_width="600px",
        ),

        rx.divider(),

        rx.heading("포인트 획득 내역", size="6", color="#333333"),

        rx.box(
            rx.cond(
                AppState.points_log.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.points_log,
                        lambda log: rx.hstack(
                            rx.text(log["date"], color="#555", size="4", width="150px"),
                            rx.text(
                                f"+{log['points']} 포인트",
                                color="#4DAB75",
                                size="4",
                                font_weight="bold",
                            ),
                            justify="between",
                            width="100%",
                            padding="12px",
                            border_radius="8px",
                            background="#F1F3F4",
                            margin_bottom="6px",
                        ),
                    ),
                    spacing="2",
                ),
                rx.text("포인트 내역이 없습니다.", color="gray"),
            ),
            width="100%",
            max_width="600px",
        ),

        spacing="5",
        width="100%",
        align="center",
    )


# -----------------------------------------
# ② 챌린지 현황 섹션
# -----------------------------------------
def render_challenge_section():
    return rx.vstack(
        rx.heading("챌린지 현황", size="8", color="#333333"),

        rx.cond(
            AppState.user_challenge_progress.length() > 0,
            rx.vstack(
                rx.foreach(
                    AppState.user_challenge_progress,
                    lambda progress: rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text(progress["title"], size="4", font_weight="bold"),
                                rx.cond(
                                    progress["is_completed"],
                                    rx.badge("완료", color_scheme="green"),
                                    rx.badge("진행중", color_scheme="blue"),
                                ),
                                justify="between",
                                width="100%",
                            ),
                            rx.text(
                                f"{progress['current_value']} / {progress['goal_value']}",
                                color="#777",
                                size="3",
                            ),
                            rx.progress(
                                value=progress["progress_percent"],
                                width="100%",
                                color_scheme="green",
                            ),
                            rx.text(
                                f"보상: {progress['reward_points']}점",
                                color="#777",
                                size="2",
                            ),
                            spacing="2",
                        ),
                        padding="20px",
                        background="#F1F3F4",
                        border_radius="12px",
                        width="100%",
                        max_width="700px",
                        margin_bottom="12px",
                    ),
                ),
                align="center",
                width="100%",
            ),
            rx.text("참여 중인 챌린지가 없습니다.", color="gray"),
        ),

        spacing="4",
        width="100%",
        align="center",
    )


# -----------------------------------------
# ③ 탄소 배출 대시보드 섹션
# -----------------------------------------
def render_dashboard_section():
    return rx.vstack(
        rx.heading("탄소 배출 대시보드", size="8", color="#333333"),

        rx.cond(
            AppState.carbon_total_logs > 0,
            rx.vstack(
                # 요약 카드
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.vstack(
                                rx.text("이번주 총 배출량", size="2", color="#777"),
                                rx.text(
                                    f"{AppState.weekly_emission}kg",
                                    size="6",
                                    font_weight="bold",
                                    color="#333",
                                ),
                                align="center",
                            ),
                            background="#F1F3F4",
                            padding="20px",
                            border_radius="10px",
                            flex="1",
                            width="150px",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("이번달 총 배출량", size="2", color="#777"),
                                rx.text(
                                    f"{AppState.monthly_emission}kg",
                                    size="6",
                                    font_weight="bold",
                                    color="#333",
                                ),
                                align="center",
                            ),
                            background="#F1F3F4",
                            padding="20px",
                            border_radius="10px",
                            flex="1",
                            width="150px",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("총 기록일", size="2", color="#777"),
                                rx.text(
                                    f"{AppState.carbon_total_logs}일",
                                    size="6",
                                    font_weight="bold",
                                    color="#333",
                                ),
                                align="center",
                            ),
                            background="#F1F3F4",
                            padding="20px",
                            border_radius="10px",
                            flex="1",
                            width="150px",
                        ),
                        spacing="4",
                        max_width="800px",
                    ),
                    width="100%",
                    display="flex",
                    justify_content="center",
                ),

                rx.divider(),

                # 그래프들을 가로로 배치
                rx.hstack(
                    # 이번주 그래프
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "이번주 일별 배출량",
                                size="5",
                                color="#333333",
                                margin_bottom="15px",
                            ),
                            rx.cond(
                                AppState.weekly_daily_data.length() > 0,
                                rx.vstack(
                                    # 막대 그래프
                                    rx.hstack(
                                        rx.foreach(
                                            AppState.weekly_daily_data,
                                            lambda day_data: rx.vstack(
                                                rx.text(
                                                    f"{day_data['emission']}kg",
                                                    color="#333333",
                                                    size="1",
                                                    margin_bottom="5px",
                                                ),
                                                rx.cond(
                                                    day_data["has_emission"],
                                                    rx.box(
                                                        width="40px",
                                                        height=f"{day_data['height']}px",
                                                        background="#4DAB75",
                                                        border_radius="4px 4px 0 0",
                                                        min_height="4px",
                                                        transition="all 0.3s",
                                                    ),
                                                    rx.box(
                                                        width="40px",
                                                        height="4px",
                                                        background="rgba(255, 255, 255, 0.1)",
                                                        border_radius="4px 4px 0 0",
                                                        min_height="4px",
                                                    ),
                                                ),
                                                rx.text(
                                                    day_data["day"],
                                                    color="gray.300",
                                                    size="2",
                                                    font_weight="bold",
                                                ),
                                                spacing="1",
                                                align="center",
                                                width="50px",
                                            ),
                                        ),
                                        spacing="2",
                                        justify="between",
                                        align="end",
                                        width="100%",
                                        height="250px",
                                        padding="10px",
                                    ),
                                    spacing="2",
                                ),
                                rx.text(
                                    "이번주 데이터가 없습니다.",
                                    color="gray.400",
                                    size="3",
                                ),
                            ),
                            spacing="2",
                        ),
                        padding="20px",
                        border_radius="12px",
                        background="#F1F3F4",
                        width="600px",
                    ),

                    # 최근 30일 일별 배출량 그래프 (꺾은선)
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "최근 30일 일별 배출량",
                                size="5",
                                color="#333333",
                                margin_bottom="15px",
                            ),
                            rx.box(
                                # SVG로 꺾은선 그래프 그리기
                                rx.html(
                                    f"""
                                    <svg width="100%" height="250" style="overflow: visible;">
                                        <!-- 그리드 라인 -->
                                        <line x1="0" y1="200" x2="100%" y2="200" stroke="#E0E0E0" stroke-width="1"/>
                                        <line x1="0" y1="150" x2="100%" y2="150" stroke="#E0E0E0" stroke-width="1"/>
                                        <line x1="0" y1="100" x2="100%" y2="100" stroke="#E0E0E0" stroke-width="1"/>
                                        <line x1="0" y1="50" x2="100%" y2="50" stroke="#E0E0E0" stroke-width="1"/>

                                        <!-- 꺾은선 경로 -->
                                        <polyline id="emission-line" fill="none" stroke="#4DAB75" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>

                                        <!-- 데이터 포인트들 -->
                                        <g id="data-points"></g>
                                    </svg>
                                    <script>
                                        (function() {{
                                            const data = {rx.Var.create(AppState.monthly_daily_data)};
                                            const svg = document.querySelector('#emission-line').closest('svg');
                                            const line = document.querySelector('#emission-line');
                                            const pointsGroup = document.querySelector('#data-points');

                                            if (!data || data.length === 0) return;

                                            const svgWidth = svg.clientWidth;
                                            const spacing = svgWidth / (data.length + 1);
                                            const maxHeight = 180;

                                            // 최대값 찾기
                                            const maxEmission = Math.max(...data.map(d => d.emission || 0));
                                            const scale = maxEmission > 0 ? maxHeight / maxEmission : 1;

                                            // 꺾은선 경로 생성
                                            const points = data.map((d, i) => {{
                                                const x = spacing * (i + 1);
                                                const y = 200 - (d.emission || 0) * scale;
                                                return `${{x}},${{y}}`;
                                            }}).join(' ');

                                            line.setAttribute('points', points);

                                            // 데이터 포인트와 툴팁 추가
                                            data.forEach((d, i) => {{
                                                const x = spacing * (i + 1);
                                                const y = 200 - (d.emission || 0) * scale;

                                                // 포인트 그룹
                                                const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                                                g.style.cursor = 'pointer';

                                                // 데이터 포인트 (원)
                                                const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                                                circle.setAttribute('cx', x);
                                                circle.setAttribute('cy', y);
                                                circle.setAttribute('r', '4');
                                                circle.setAttribute('fill', '#4DAB75');
                                                circle.setAttribute('stroke', '#FFFFFF');
                                                circle.setAttribute('stroke-width', '2');

                                                // 날짜 라벨 (x축)
                                                const dateLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                                                dateLabel.setAttribute('x', x);
                                                dateLabel.setAttribute('y', '220');
                                                dateLabel.setAttribute('text-anchor', 'middle');
                                                dateLabel.setAttribute('font-size', '10');
                                                dateLabel.setAttribute('fill', '#777');
                                                dateLabel.textContent = d.month_day;

                                                // 툴팁
                                                const tooltip = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                                                tooltip.style.opacity = '0';
                                                tooltip.style.transition = 'opacity 0.2s';
                                                tooltip.style.pointerEvents = 'none';

                                                const tooltipBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                                                tooltipBg.setAttribute('x', x - 40);
                                                tooltipBg.setAttribute('y', y - 50);
                                                tooltipBg.setAttribute('width', '80');
                                                tooltipBg.setAttribute('height', '35');
                                                tooltipBg.setAttribute('rx', '6');
                                                tooltipBg.setAttribute('fill', '#333333');
                                                tooltipBg.setAttribute('opacity', '0.9');

                                                const tooltipDate = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                                                tooltipDate.setAttribute('x', x);
                                                tooltipDate.setAttribute('y', y - 35);
                                                tooltipDate.setAttribute('text-anchor', 'middle');
                                                tooltipDate.setAttribute('font-size', '11');
                                                tooltipDate.setAttribute('fill', '#FFFFFF');
                                                tooltipDate.textContent = d.month_day;

                                                const tooltipValue = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                                                tooltipValue.setAttribute('x', x);
                                                tooltipValue.setAttribute('y', y - 22);
                                                tooltipValue.setAttribute('text-anchor', 'middle');
                                                tooltipValue.setAttribute('font-size', '12');
                                                tooltipValue.setAttribute('font-weight', 'bold');
                                                tooltipValue.setAttribute('fill', '#4DAB75');
                                                tooltipValue.textContent = `${{d.emission}}kg`;

                                                tooltip.appendChild(tooltipBg);
                                                tooltip.appendChild(tooltipDate);
                                                tooltip.appendChild(tooltipValue);

                                                // 호버 이벤트
                                                g.addEventListener('mouseenter', () => {{
                                                    tooltip.style.opacity = '1';
                                                    circle.setAttribute('r', '6');
                                                }});

                                                g.addEventListener('mouseleave', () => {{
                                                    tooltip.style.opacity = '0';
                                                    circle.setAttribute('r', '4');
                                                }});

                                                g.appendChild(circle);
                                                g.appendChild(tooltip);
                                                pointsGroup.appendChild(g);

                                                // 날짜 라벨은 별도로 추가
                                                if (i % 3 === 0) {{ // 3일마다만 표시
                                                    svg.appendChild(dateLabel);
                                                }}
                                            }});
                                        }})();
                                    </script>
                                    """
                                ),
                                width="100%",
                                min_height="250px",
                            ),
                            spacing="2",
                        ),
                        padding="20px",
                        border_radius="12px",
                        background="#F1F3F4",
                        width="600px",
                    ),

                    spacing="4",
                    align="start",
                    width="100%",
                ),

                spacing="4",
            ),
            rx.text("기록된 배출 데이터가 없습니다.", color="gray"),
        ),

        spacing="5",
        width="100%",
        align="center",
    )




# -----------------------------------------
# 메인 페이지 구조 (사이드바 + 컨텐츠)
# -----------------------------------------
def mypage_page() -> rx.Component:
    return rx.box(
        header(),

        rx.hstack(
            # ----------- 왼쪽 사이드바 -----------
            rx.box(
                rx.vstack(
                    rx.button(
                        "내 포인트",
                        on_click=lambda: AppState.set_mypage_section("points"),
                        size="3",
                        background=rx.cond(AppState.mypage_section == "points", "#F1F3F4", "transparent"),
                        color="#333333",
                        width="100%",
                        border_radius="10px",
                        padding="12px",

                        # 텍스트 왼쪽 정렬
                        justify_content="start",
                        text_align="left",
                    ),
                    rx.button(
                        "챌린지 현황",
                        on_click=lambda: AppState.set_mypage_section("challenge"),
                        size="3",
                        background=rx.cond(AppState.mypage_section == "challenge", "#F1F3F4", "transparent"),
                        color="#333333",
                        width="100%",
                        border_radius="10px",
                        padding="12px",

                        # 텍스트 왼쪽 정렬
                        justify_content="start",
                        text_align="left",
                    ),
                    rx.button(
                        "탄소 배출 대시보드",
                        on_click=lambda: AppState.set_mypage_section("dashboard"),
                        size="3",
                        background=rx.cond(AppState.mypage_section == "dashboard", "#F1F3F4", "transparent"),
                        color="#333333",
                        width="100%",
                        border_radius="10px",
                        padding="12px",

                        # 텍스트 왼쪽 정렬
                        justify_content="start",
                        text_align="left",
                    ),
                    spacing="3",
                    padding="20px",
                ),
                width="300px",
                background="#4DAB75",
                min_height="600px",
                border_radius="20px",
                margin="30px",
            ),


            # ----------- 오른쪽 컨텐츠 -----------
            rx.box(
                rx.cond(
                    AppState.mypage_section == "points",
                    render_points_section(),
                    rx.cond(
                        AppState.mypage_section == "challenge",
                        render_challenge_section(),
                        render_dashboard_section(),
                    ),
                ),
                width="100%",
                padding="40px",
            ),

            width="100%",
        ),

        background="#F8F9FA",
        min_height="100vh",
    )
