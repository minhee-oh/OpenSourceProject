"""
Climatiq API에서 사용 가능한 activity_id를 찾는 진단 스크립트
프로젝트 루트에서 실행: python check_ids.py
"""

import requests
import json
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("CLIMATIQ_API_KEY", "")

if not API_KEY:
    print("❌ CLIMATIQ_API_KEY가 .env 파일에 설정되지 않았습니다.")
    print("   .env 파일에 CLIMATIQ_API_KEY=your_api_key_here 를 추가하세요.")
    exit(1)

BASE_URL = "https://beta4.api.climatiq.io/search"


def search_climatiq(query: str):
    """
    Climatiq API에서 activity_id 검색
    
    Args:
        query: 검색 키워드
    """
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "query": query,
        "data_version": "^1",
        "results_per_page": 5  # 더 많은 결과 확인
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            results = response.json().get("results", [])
            print(f"\n🔍 '{query}' 검색 결과 ({len(results)}개):")
            
            if not results:
                print("   ⚠️  검색 결과가 없습니다.")
                return
            
            for idx, item in enumerate(results, 1):
                print(f"\n[{idx}] ID: {item.get('activity_id', 'N/A')}")
                print(f"    Name: {item.get('name', 'N/A')}")
                print(f"    Region: {item.get('region', 'N/A')}")
                print(f"    Year: {item.get('year', 'N/A')}")
                print(f"    Category: {item.get('category', 'N/A')}")
                
                # 사용 가능한 파라미터 정보
                if 'parameters' in item:
                    print(f"    Parameters: {item['parameters']}")
        else:
            print(f"❌ 검색 실패 ({response.status_code}):")
            try:
                error_data = response.json()
                print(f"   {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   {response.text}")
                
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


def test_estimate(activity_id: str, region: str = "Global", test_params: dict = None):
    """
    특정 activity_id로 실제 계산 테스트
    
    Args:
        activity_id: 테스트할 activity_id
        region: 지역 코드
        test_params: 테스트 파라미터
    """
    if not test_params:
        return
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "emission_factor": {
            "activity_id": activity_id,
            "data_version": "^1",
            "region": region
        },
        "parameters": test_params
    }
    
    try:
        response = requests.post(
            "https://beta4.api.climatiq.io/estimate",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            co2e = data.get("co2e", 0.0)
            co2e_unit = data.get("co2e_unit", "kg")
            print(f"   ✅ 테스트 성공: {co2e} {co2e_unit}")
        else:
            print(f"   ❌ 테스트 실패 ({response.status_code}):")
            try:
                error_data = response.json()
                print(f"      {json.dumps(error_data, indent=6, ensure_ascii=False)}")
            except:
                print(f"      {response.text}")
    except Exception as e:
        print(f"   ❌ 테스트 오류: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Climatiq API Activity ID 진단 스크립트")
    print("=" * 60)
    print(f"API 키: {API_KEY[:10]}...{API_KEY[-4:] if len(API_KEY) > 14 else '***'}")
    print()
    
    # 주요 키워드로 검색 실행
    print("\n" + "=" * 60)
    print("1. 전기 (Electricity)")
    print("=" * 60)
    search_climatiq("electricity grid mix")
    
    print("\n" + "=" * 60)
    print("2. 자동차 (Passenger Car)")
    print("=" * 60)
    search_climatiq("passenger car petrol")
    search_climatiq("passenger vehicle automobile")
    
    print("\n" + "=" * 60)
    print("3. 버스 (Bus)")
    print("=" * 60)
    search_climatiq("passenger bus")
    
    print("\n" + "=" * 60)
    print("4. 지하철 (Subway)")
    print("=" * 60)
    search_climatiq("subway")
    search_climatiq("passenger train")
    
    print("\n" + "=" * 60)
    print("5. 소고기 (Beef)")
    print("=" * 60)
    search_climatiq("beef")
    search_climatiq("meat products beef")
    
    print("\n" + "=" * 60)
    print("6. 돼지고기 (Pork)")
    print("=" * 60)
    search_climatiq("pork")

    print("\n" + "=" * 60)
    print("7. 의류 / 텍스타일 (Textiles & Clothing)")
    print("=" * 60)
    # 면/합성섬유/의류 관련 ID 탐색
    search_climatiq("textiles cotton")
    search_climatiq("cotton t-shirt")
    search_climatiq("synthetic fabric")
    search_climatiq("clothing")

    print("\n" + "=" * 60)
    print("8. 쓰레기 (Waste)")
    print("=" * 60)
    # 생활폐기물 매립/재활용 관련 ID 탐색
    search_climatiq("municipal solid waste landfill")
    search_climatiq("municipal solid waste recycling")

    print("\n" + "=" * 60)
    print("9. 물 / 수돗물 (Water)")
    print("=" * 60)
    # 수돗물 공급/정수/처리 관련 ID 탐색
    search_climatiq("water treatment")
    search_climatiq("tap water supply")

    print("\n" + "=" * 60)
    print("진단 완료!")
    print("=" * 60)
    print("\n💡 위 결과에서 사용 가능한 activity_id를 확인하고,")
    print("   carbon_api.py의 TRANSPORT_VEHICLE_TYPES, food_map,")
    print("   calculate_clothing_emission / calculate_waste_emission / calculate_water_emission")
    print("   내부의 activity_id를 업데이트하세요.")

