import requests
import random
import csv

# 네이버 API 인증 정보 입력
CLIENT_ID = 'YOUR_CLIENT_ID'        # ← 본인의 네이버 Client ID
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'  # ← 본인의 Client Secret

# 위치 입력
print("\n📍 검색할 지역을 입력하세요 (예: 강남역, 홍대입구 등): ")
location = input("▶ 위치 입력: ")

while True:
    print("\n# 지정한 위치 주변의 맛집, 술집, 카페 추천")
    print("1. 맛집")
    print("2. 술집")
    print("3. 카페")
    print("4. 종료")
    choice = input("번호 입력: ")

    if choice == "4":
        break

    if choice == "1":
        keyword = "맛집"
        submenu_keys = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅎ"]
    elif choice == "2":
        keyword = "술집"
        submenu_keys = ["A", "B", "C", "D", "E", "F", "Q"]
    elif choice == "3":
        keyword = "카페"
        submenu_keys = ["a", "b", "c", "d", "e", "f", "q"]
    else:
        print("❌ 잘못된 입력입니다.")
        continue

    # 네이버 API 호출
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": f"{location} {keyword}",
        "display": 30,
        "start": 1,
        "sort": "random"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("items", [])
    else:
        print("❌ 요청 실패:", response.status_code)
        continue

    if not results:
        print("⚠ 검색 결과가 없습니다.")
        continue

    # 서브 메뉴 시작
    while True:
        print(f"\n📂 [{keyword} 서브 메뉴]")
        if keyword == "맛집":
            print("ㄱ. 순위 5")
            print("ㄴ. 순위 10")
            print("ㄷ. 순위 30")
            print("ㄹ. 랜덤 추천")
            print("ㅁ. CSV 저장")
            print("ㅂ. 첫 화면으로")
            print("ㅎ. 종료")
        elif keyword == "술집":
            print("A. 순위 5")
            print("B. 순위 10")
            print("C. 순위 30")
            print("D. 랜덤 추천")
            print("E. CSV 저장")
            print("F. 첫 화면으로")
            print("Q. 종료")
        elif keyword == "카페":
            print("a. 순위 5")
            print("b. 순위 10")
            print("c. 순위 30")
            print("d. 랜덤 추천")
            print("e. CSV 저장")
            print("f. 첫 화면으로")
            print("q. 종료")

        sub = input("선택: ")

        # 출력 함수
        def print_list(limit):
            for i in range(min(limit, len(results))):
                item = results[i]
                title = item["title"].replace("<b>", "").replace("</b>", "")
                print(f"{i+1}. {title} - {item['roadAddress']}")
                print(f"   ▶ {item['link']}")

        # 서브메뉴 처리
        if sub in ["ㄱ", "A", "a"]:
            print_list(5)
        elif sub in ["ㄴ", "B", "b"]:
            print_list(10)
        elif sub in ["ㄷ", "C", "c"]:
            print_list(30)
        elif sub in ["ㄹ", "D", "d"]:
            item = random.choice(results)
            title = item["title"].replace("<b>", "").replace("</b>", "")
            print(f"\n🔀 랜덤 추천: {title}")
            print(f"   주소: {item['roadAddress']}")
            print(f"   ▶ {item['link']}")
        elif sub in ["ㅁ", "E", "e"]:
            filename = f"{keyword}_{location}.csv"
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["순위", "이름", "카테고리", "주소", "링크"])
                for i, item in enumerate(results, 1):
                    title = item["title"].replace("<b>", "").replace("</b>", "")
                    writer.writerow([i, title, item["category"], item["roadAddress"], item["link"]])
            print(f"✅ '{filename}' 저장 완료")
        elif sub in ["ㅂ", "F", "f"]:
            break
        elif sub in ["ㅎ", "Q", "q"]:
            exit()
        else:
            print("❌ 잘못된 입력입니다.")
