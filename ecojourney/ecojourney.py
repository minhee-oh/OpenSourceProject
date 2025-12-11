import reflex as rx
from .states import AppState
from .pages.home import home_page
from .pages.intro import intro_page
from .pages.info import info_page
from .pages.auth import auth_page
from .pages.transportation import transportation_page
from .pages.food import food_page
from .pages.clothing import clothing_page
from .pages.electricity import electricity_page
from .pages.waste import waste_page
from .pages.water import water_page
from .pages.report import report_page
from .pages.mypage import mypage_page
from .pages.battle import battle_page
from .pages.ranking import ranking_page

# ----------------------------------------------------
# 앱 인스턴스 정의 및 라우팅
# ----------------------------------------------------

# AppState를 사용하여 앱을 초기화합니다.
# _state 파라미터를 사용하여 Reflex가 AppState를 인식하도록 함
app = rx.App()

# 1. 메인 홈 화면 라우팅 (EcoJourney.py 파일 내 home_page 함수 사용)
app.add_page(home_page, route="/", title="ECOJOURNEY")

# 2. 리포트 시작 화면 라우팅
app.add_page(intro_page, route="/intro", title="ECOJOURNEY | 리포트")
# 2-1. 챌린지 페이지
app.add_page(info_page, route="/info", title="ECOJOURNEY | 챌린지", on_load=AppState.load_active_challenges)

# 2-1. 로그인/회원가입 화면 라우팅
app.add_page(auth_page, route="/auth", title="ECOJOURNEY | 로그인")

# 3. 카테고리 입력 화면 라우팅 (CATEGORY_CONFIG 기반 자동 등록)
app.add_page(transportation_page, route="/input/transportation", title="ECOJOURNEY | 교통")
app.add_page(food_page, route="/input/food", title="ECOJOURNEY | 식품")
app.add_page(clothing_page, route="/input/clothing", title="ECOJOURNEY | 의류")
app.add_page(electricity_page, route="/input/electricity", title="ECOJOURNEY | 전기")
app.add_page(waste_page, route="/input/waste", title="ECOJOURNEY | 쓰레기")
app.add_page(water_page, route="/input/water", title="ECOJOURNEY | 물")


# 4. 결과 리포트 화면 라우팅
app.add_page(report_page, route="/report", title="ECOJOURNEY | 결과 리포트")

# 5. 마이페이지 라우팅
app.add_page(mypage_page, route="/mypage", title="ECOJOURNEY | 마이페이지", on_load=AppState.load_mypage_data)

# 6. 배틀 페이지 라우팅
app.add_page(battle_page, route="/battle", title="ECOJOURNEY | 배틀", on_load=AppState.load_current_battle)

# 7. 저번주 랭킹 페이지 라우팅
app.add_page(
    ranking_page, 
    route="/ranking", 
    title="EcoJourney | 랭킹", 
    on_load=AppState.load_ranking_data
)