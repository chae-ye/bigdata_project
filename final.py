#배달앱 선택지 입력칸
#1일때 배달의 민족, 2일때 요기요, 3일때 종료

#1을 입력했을 때
#A:검색어순위 5
#B:검색어순위 10
#C:검색어순위 20
#D:20개의 배달 순위중 랜덤으로 1개 추천
#E:csv파일
#R:다시 처음의 1,2 선택지 띄우기
#X:종료
#R이나 X를 선택하지 않으면 1번이후의 선택지 반복

#2를 입력했을 때
#a:검색어순위 5
#b:검색어순위 10
#c:검색어순위 20
#d:20개의 배달 순위중 랜덤으로 1개 추천
#e:csv파일
#r:다시 처음의 1,2 선택지 띄우기
#x:종료
#r이나 x를 선택하지 않으면 2번이후의 선택지 반복

##배달의 민족 검색어순위 크롤링 코드
##요기요 검색어순위 크롤링 코드
##(가능하다면)f_frame을 def명령어로

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 모바일 환경 설정 (iPhone X 등)
mobile_emulation = {"deviceName": "iPhone X"}

options = Options()
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # 창 유지

driver = webdriver.Chrome(options=options)

# 배민 모바일 웹 열기
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# ✅ 1. 모바일 기기 에뮬레이션 설정
mobile_emulation = {
    "deviceName": "iPhone 16"  # 또는 "iPhone SE", "Pixel 2", "Galaxy S5" 등
}

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)  # 창이 자동으로 닫히지 않도록 유지

# ✅ 2. 크롬 드라이버 실행
driver = webdriver.Chrome(options=chrome_options)

# ✅ 3. 테스트용 모바일 웹사이트 열기 (배민 모바일 웹)
driver.get("https://m.baemin.com")

# ✅ 4. 결과 확인
print("모바일 환경으로 배달의민족 열렸습니다!")

# ✅ 5. 종료 대기
input("확인 후 Enter를 누르면 창이 닫힙니다.")
driver.quit()


print("👉 로그인 및 위치 설정을 수동으로 완료해주세요.")
input("완료 후 Enter를 누르세요.")

# 검색 페이지로 이동
driver.get("https://m.baemin.com/search?query=치킨")
time.sleep(5)

# 음식점 이름 추출 (클래스명은 실제 구조에 따라 달라질 수 있음)
stores = driver.find_elements(By.CSS_SELECTOR, "div.sc-dkzDqf")  # 클래스명은 예시

print(f"[치킨] 검색 결과 순위:")
for idx, store in enumerate(stores[:10], start=1):
    print(f"{idx}. {store.text.splitlines()[0]}")  # 첫 줄만 가게 이름으로 추정

driver.quit()


import random

def baemin_service():
    """배달의 민족 서비스 메뉴를 처리하는 함수"""
    while True:
        print("\n--- 배달의 민족 ---")
        print("A: 배달순위 5")
        print("B: 배달순위 10")
        print("C: 배달순위 20")
        print("D: 20개의 배달 순위 중 랜덤으로 1개 추천")
        print("E: CSV 파일")
        print("R: 처음으로 돌아가기")
        print("X: 종료")
        choice = input("선택: ")

        if choice == 'A':
            print("배달의 민족: 배달순위 5입니다.")
        elif choice == 'B':
            print("배달의 민족: 배달순위 10입니다.")
        elif choice == 'C':
            print("배달의 민족: 배달순위 20입니다.")
        elif choice == 'D':
            random_rank = random.randint(1, 20)
            print(f"배달의 민족: 추천 배달순위는 {random_rank}입니다.")
        elif choice == 'E':
            print("배달의 민족: CSV 파일 관련 기능입니다. (구현 예정)")
        elif choice == 'R':
            print("처음 메뉴로 돌아갑니다.")
            return "return_to_main"  # 메인 메뉴로 돌아가기 위한 신호
        elif choice == 'X':
            print("프로그램을 종료합니다.")
            return "exit_program"  # 프로그램 종료 신호
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")
            # R이나 X가 아니면 현재 루프를 반복합니다.

def yogiyo_service():
    """요기요 서비스 메뉴를 처리하는 함수"""
    while True:
        print("\n--- 요기요 ---")
        print("a: 배달순위 5")
        print("b: 배달순위 10")
        print("c: 배달순위 20")
        print("d: 20개의 배달 순위 중 랜덤으로 1개 추천")
        print("e: CSV 파일")
        print("r: 처음으로 돌아가기")
        print("x: 종료")
        choice = input("선택: ")

        if choice == 'a':
            print("요기요: 배달순위 5입니다.")
        elif choice == 'b':
            print("요기요: 배달순위 10입니다.")
        elif choice == 'c':
            print("요기요: 배달순위 20입니다.")
        elif choice == 'd':
            random_rank = random.randint(1, 20)
            print(f"요기요: 추천 배달순위는 {random_rank}입니다.")
        elif choice == 'e':
            print("요기요: CSV 파일 관련 기능입니다. (구현 예정)")
        elif choice == 'r':
            print("처음 메뉴로 돌아갑니다.")
            return "return_to_main"  # 메인 메뉴로 돌아가기 위한 신호
        elif choice == 'x':
            print("프로그램을 종료합니다.")
            return "exit_program"  # 프로그램 종료 신호
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")
            # r이나 x가 아니면 현재 루프를 반복합니다.

def main():
    """메인 프로그램 실행 함수"""
    while True:
        print("\n=== 배달앱 선택 ===")
        print("1: 배달의 민족")
        print("2: 요기요")
        print("3: 종료")
        app_choice = input("선택 (1, 2, 3): ")

        if app_choice == '1':
            result = baemin_service()
            if result == "exit_program":
                break  # 프로그램 종료
            elif result == "return_to_main":
                continue # 메인 선택지로 다시 시작
        elif app_choice == '2':
            result = yogiyo_service()
            if result == "exit_program":
                break  # 프로그램 종료
            elif result == "return_to_main":
                continue # 메인 선택지로 다시 시작
        elif app_choice == '3':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 1, 2, 3 중에서 선택해주세요.")

if __name__ == "__main__":
    main()