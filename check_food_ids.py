"""
Climatiq API에서 식품 관련 activity_id 검색 스크립트
햄버거, 피자 등 패스트푸드 관련 ID 확인
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CLIMATIQ_API_KEY", "")

if not API_KEY:
    print("❌ CLIMATIQ_API_KEY가 .env 파일에 설정되지 않았습니다.")
    exit(1)

BASE_URL = "https://beta4.api.climatiq.io/search"

def search_climatiq(query: str, max_results: int = 10):
    """Climatiq API에서 activity_id 검색"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "query": query,
        "data_version": "^1",
        "results_per_page": max_results
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            results = response.json().get("results", [])
            print(f"\n🔍 '{query}' 검색 결과 ({len(results)}개):")
            
            if not results:
                print("   ⚠️  검색 결과가 없습니다.")
                return []
            
            found_ids = []
            for idx, item in enumerate(results, 1):
                activity_id = item.get('activity_id', 'N/A')
                name = item.get('name', 'N/A')
                region = item.get('region', 'N/A')
                category = item.get('category', 'N/A')
                
                print(f"\n[{idx}] {name}")
                print(f"    ID: {activity_id}")
                print(f"    Region: {region}")
                print(f"    Category: {category}")
                
                found_ids.append({
                    "activity_id": activity_id,
                    "name": name,
                    "region": region,
                    "category": category
                })
            
            return found_ids
        else:
            print(f"❌ 검색 실패 ({response.status_code})")
            return []
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return []

if __name__ == "__main__":
    print("=" * 70)
    print("Climatiq API 식품 카테고리 검색")
    print("=" * 70)
    print(f"API 키: {API_KEY[:10]}...{API_KEY[-4:] if len(API_KEY) > 14 else '***'}\n")
    
    # 검색할 키워드 목록
    search_queries = [
        "hamburger",
        "pizza", 
        "fast food",
        "processed food",
        "ready meal",
        "convenience food",
        "bread",
        "bakery products",
        "pasta",
        "noodles",
        "sandwich",
        "fried food"
    ]
    
    all_results = {}
    
    for query in search_queries:
        results = search_climatiq(query, max_results=5)
        if results:
            all_results[query] = results
    
    # 요약 출력
    print("\n" + "=" * 70)
    print("검색 결과 요약")
    print("=" * 70)
    
    for query, results in all_results.items():
        if results:
            print(f"\n✅ '{query}': {len(results)}개 결과")
            for r in results[:3]:  # 상위 3개만 표시
                print(f"   - {r['name']} ({r['activity_id']})")
    
    print("\n" + "=" * 70)
    print("검색 완료!")
    print("=" * 70)
    print("\n💡 위 결과에서 사용 가능한 activity_id를 확인하세요.")
    print("   carbon_api.py의 food_map에 추가할 수 있습니다.")




