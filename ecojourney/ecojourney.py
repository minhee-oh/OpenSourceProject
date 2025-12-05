import reflex as rx
from .states import AppState
from .pages.home import home_page
from .pages.intro import intro_page
from .pages.auth import auth_page
from .pages.transportation import transportation_page
from .pages.food import food_page
from .pages.clothing import clothing_page
from .pages.electricity import electricity_page
from .pages.waste import waste_page
from .pages.water import water_page
from .pages.report import report_page
from .pages.mypage import mypage_page

# ----------------------------------------------------
# 앱 인스턴스 정의 및 라우팅
# ----------------------------------------------------

# AppState를 사용하여 앱을 초기화합니다.
# _state 파라미터를 사용하여 Reflex가 AppState를 인식하도록 함
app = rx.App()

# 1. 메인 홈 화면 라우팅 (EcoJourney.py 파일 내 home_page 함수 사용)
app.add_page(home_page, route="/", title="EcoJourney | 시작")

# 2. 서비스 소개 화면 라우팅
app.add_page(intro_page, route="/intro", title="EcoJourney | 소개")

# 2-1. 로그인/회원가입 화면 라우팅
app.add_page(auth_page, route="/auth", title="EcoJourney | 로그인")

# 3. 카테고리 입력 화면 라우팅 (CATEGORY_CONFIG 기반 자동 등록)
app.add_page(transportation_page, route="/input/transportation", title="EcoJourney | 교통")
app.add_page(food_page, route="/input/food", title="EcoJourney | 식품")
app.add_page(clothing_page, route="/input/clothing", title="EcoJourney | 의류")
app.add_page(electricity_page, route="/input/electricity", title="EcoJourney | 전기")
app.add_page(waste_page, route="/input/waste", title="EcoJourney | 쓰레기")
app.add_page(water_page, route="/input/water", title="EcoJourney | 물")


# 4. 결과 리포트 화면 라우팅
app.add_page(report_page, route="/report", title="EcoJourney | 결과 리포트")

# 5. 마이페이지 라우팅
app.add_page(mypage_page, route="/mypage", title="EcoJourney | 마이페이지", on_load=AppState.load_mypage_data)