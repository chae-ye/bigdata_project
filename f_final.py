import requests
import random
import csv
import time

# --- 함수 정의 ---

def print_list(results_list, limit):
    """검색 결과를 지정된 개수만큼 출력하는 함수"""
    if not results_list:
        print("⚠ 표시할 결과가 없습니다.")
        return
    
    print(f"\n--- 검색 결과 (최대 {limit}개) ---")
    for i in range(min(limit, len(results_list))):
        item = results_list[i]
        title = item.get("title", "").replace("<b>", "").replace("</b>", "")
        address = item.get("roadAddress", "주소 정보 없음")
        link = item.get("link", "")
        print(f"{i+1}. {title} - {address}")
        if link:
            print(f"   ▶ {link}")
    print("--------------------------")

# 새로운 핵심 기능: 여러 검색 결과를 합치는 함수
def search_and_combine_results(location, main_keyword, sub_keywords):
    """세부 검색어 목록으로 API를 여러 번 호출하고 결과를 합쳐서 반환하는 함수"""
    
    # API 인증 정보
    CLIENT_ID = 'wNBvkdy4tG0r6duYlgvS'
    CLIENT_SECRET = '67fDDzq7Ly'
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    url = "https://openapi.naver.com/v1/search/local.json"

    combined_results = []
    seen_places = set() # 중복된 장소를 확인하기 위한 set

    # 기본 검색어 + 세부 검색어 목록을 합쳐서 전체 검색어 리스트 생성
    search_queries = [f"{location} {main_keyword}"] + [f"{location} {main_keyword} {sub}" for sub in sub_keywords]

    print("\n여러 관련 검색어로 결과를 확장합니다...")
    for query in search_queries:
        params = {'query': query, 'display': 5, 'sort': 'random'}
        
        try:
            print(f"-> '{query}' 검색 중...")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])

            for item in items:
                # 상호명과 주소로 고유한 장소인지 식별
                place_id = (item.get("title"), item.get("roadAddress"))
                if place_id not in seen_places:
                    seen_places.add(place_id)
                    combined_results.append(item)
            
            time.sleep(0.1) # API에 부담을 주지 않기 위한 짧은 대기

        except requests.exceptions.RequestException as e:
            print(f"❌ '{query}' 검색 중 API 요청 실패: {e}")
            
    return combined_results


# --- 메인 로직 ---
while True:
    print("\n📍 검색할 지역을 입력하세요 (프로그램 종료 시 '종료' 입력): ")
    location = input("▶ 위치 입력: ")

    if not location.strip() or location == '종료':
        print("✅ 프로그램을 종료합니다.")
        break

    while True:
        print(f"\n# [{location}] 주변의 장소를 검색합니다.")
        print("1. 맛집")
        print("2. 술집")
        print("3. 카페")
        print("4. 새로운 위치 검색")
        print("5. 프로그램 종료")

        choice = input("번호 입력: ")

        if choice == '4':
            break
        if choice == '5':
            print("✅ 프로그램을 종료합니다.")
            exit()

        if choice == "1":
            keyword = "맛집"
            # 맛집 검색을 위한 세부 키워드 목록
            sub_keywords_list = ["한식", "일식", "중식", "양식", "분식", "고기", "파스타", "족발"]
        elif choice == "2":
            keyword = "술집"
            # 술집 검색을 위한 세부 키워드 목록
            sub_keywords_list = ["이자카야", "호프", "바", "포차", "와인", "막걸리"]
        elif choice == "3":
            keyword = "카페"
            # 카페 검색을 위한 세부 키워드 목록
            sub_keywords_list = ["디저트", "베이커리", "브런치", "케이크", "전통찻집"]
        else:
            print("❌ 잘못된 입력입니다. 1~5 사이의 숫자를 입력해주세요.")
            continue

        # 여러 검색 결과를 합치는 함수 호출
        results = search_and_combine_results(location, keyword, sub_keywords_list)

        print(f"\n[알림] 총 {len(results)}개의 중복 없는 장소를 찾았습니다.")

        if not results:
            print(f"⚠ '{location} {keyword}'에 대한 최종 검색 결과가 없습니다.")
            continue

        # 서브 메뉴 로직 (이전과 동일)
        while True:
            print(f"\n📂 [{keyword}] 서브 메뉴")
            print("1. 검색 결과 5개 보기")
            print("2. 검색 결과 10개 보기")
            print(f"3. 검색 결과 전부 보기 ({len(results)}개)")
            print("4. 랜덤 추천")
            print("5. CSV 파일로 저장")
            print("6. 카테고리 선택으로")
            print("7. 프로그램 종료")
            
            sub = input("선택: ")

            if sub == "1":
                print_list(results, 5)
            elif sub == "2":
                print_list(results, 10)
            elif sub == "3":
                 print_list(results, len(results))
            elif sub == "4":
                item = random.choice(results)
                title = item.get("title", "").replace("<b>", "").replace("</b>", "")
                address = item.get("roadAddress", "주소 정보 없음")
                link = item.get("link", "")
                print(f"\n🔀 랜덤 추천: {title}")
                print(f"   주소: {address}")
                if link:
                    print(f"   ▶ {link}")
            elif sub == "5":
                filename = f"{location}_{keyword}_통합_검색결과.csv"
                try:
                    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
                        writer = csv.writer(f)
                        writer.writerow(["순위", "이름", "카테고리", "주소", "링크"])
                        for i, item in enumerate(results, 1):
                            title = item.get("title", "").replace("<b>", "").replace("</b>", "")
                            writer.writerow([i, title, item.get("category", ""), item.get("roadAddress", ""), item.get("link", "")])
                    print(f"✅ '{filename}' 저장 완료")
                except IOError as e:
                    print(f"❌ 파일 저장 중 오류가 발생했습니다: {e}")
            elif sub == "6":
                break
            elif sub == "7":
                print("✅ 프로그램을 종료합니다.")
                exit()
            else:
                print("❌ 잘못된 입력입니다. 1~7 사이의 숫자를 입력해주세요.")