from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_naver_monday_webtoons():
    """
    네이버 월요 웹툰 목록에서 썸네일, 주소, 제목, 작가, 평점을 크롤링합니다.
    """
    # Chrome 옵션 설정 ( headless 모드 등 )
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
    chrome_options.add_argument("--disable-gpu") # 일부 시스템에서 headless 모드 시 필요
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    # 웹 드라이버 설정
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        print(f"WebDriver Manager를 통한 드라이버 설정 실패: {e}")
        print("로컬 ChromeDriver를 사용합니다. PATH에 설정되어 있어야 합니다.")
        # 로컬 드라이버 사용시 (PATH에 chromedriver.exe가 있어야 함)
        # driver = webdriver.Chrome(options=chrome_options)
        return []


    # 네이버 웹툰 월요일 목록 페이지 URL
    # 과거에는 weekdayList.nhn 이었으나, 현재는 /weekday?week=mon 형태
    url = "https://comic.naver.com/webtoon/weekday?week=mon"
    driver.get(url)

    webtoon_data = []

    try:
        # 웹툰 목록이 로드될 때까지 최대 10초 대기
        # 네이버 웹툰의 경우 목록은 ul 태그에 class="WeekdayMainView__comics_list--3HNfV" 와 같은
        # 동적으로 변할 수 있는 클래스명을 가질 수 있으므로, 좀 더 일반적인 선택자를 사용합니다.
        # 여기서는 #content 내의 list_area 안에 있는 ul.img_list 를 기준으로 합니다.
        # (2025년 5월 기준) 만약 이 구조가 변경되면 이 부분을 수정해야 합니다.
        # 좀 더 현대적인 구조는 div#content ul[class*="WeekdayMainView__comics_list"] li 형태일 수 있습니다.
        # 여기서는 좀 더 전통적이고 안정적인 구조를 가정합니다.
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "#content div.list_area ul.img_list li"))
        # )
        # 페이지 로딩을 위해 잠시 대기 (필요에 따라 조절)
        time.sleep(3) # DOM이 완전히 그려질 시간을 줍니다. WebDriverWait가 더 나은 선택일 수 있습니다.

        # 모든 웹툰 아이템 선택
        # 네이버 웹툰의 HTML 구조는 자주 변경될 수 있습니다.
        # 최신 구조 (2025년 기준)에서는 아래와 같은 선택자를 사용할 수 있습니다.
        # webtoon_elements = driver.find_elements(By.CSS_SELECTOR, "ul[class*='WeekdayMainView__comics_list'] > li[class*='WeekdayMainView__item']")
        # 또는 더 이전/일반적인 구조:
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, "#content div.list_area ul.img_list li")


        if not webtoon_elements:
            print("웹툰 목록을 찾을 수 없습니다. CSS 선택자를 확인해주세요.")
            # 대체 선택자 시도 (새로운 UI 대응)
            webtoon_elements = driver.find_elements(By.CSS_SELECTOR, "ul[class^='WeekdayMainView__comics_list'] li[class^='WeekdayMainView__item']")
            if not webtoon_elements:
                 print("대체 선택자로도 웹툰 목록을 찾을 수 없습니다.")
                 driver.quit()
                 return []


        for item in webtoon_elements:
            try:
                # 썸네일 이미지 URL
                # 이전 구조: item.find_element(By.CSS_SELECTOR, "div.thumb img").get_attribute("src")
                # 현재 구조:
                thumbnail_img_element = item.find_element(By.CSS_SELECTOR, "img[class*='Thumbnail__image']")
                thumbnail_url = thumbnail_img_element.get_attribute("src")
                if not thumbnail_url.startswith("http"): # 상대경로인 경우 처리 (거의 없음)
                    thumbnail_url = "https://comic.naver.com" + thumbnail_url

                # 웹툰 상세 페이지 주소
                # 이전 구조: item.find_element(By.CSS_SELECTOR, "div.thumb a").get_attribute("href")
                # 현재 구조: li 요소 자체가 a 태그를 가지고 있거나, 내부의 특정 a 태그
                try: # li > a 가 링크인 경우
                    link_element = item.find_element(By.CSS_SELECTOR, "a[class*='Item__link']") # 또는 a[class*='WeekdayMainView__link_item'] 등
                    webtoon_url = link_element.get_attribute("href")
                except: # div.thumb a 구조 (이전) 또는 다른 구조
                    link_element = item.find_element(By.CSS_SELECTOR, "div.thumb a") # 이전 구조 호환
                    webtoon_url = link_element.get_attribute("href")


                # 제목
                # 이전 구조: item.find_element(By.CSS_SELECTOR, "a.title").text
                # 현재 구조:
                title_element = item.find_element(By.CSS_SELECTOR, "[class*='ContentTitle__title']") # span.ContentTitle__title--e3qXt 등
                title = title_element.text

                # 작가명
                # 이전 구조: item.find_element(By.CSS_SELECTOR, "dd.desc a.author").text 또는 item.find_element(By.CSS_SELECTOR, "a.author").text
                # 현재 구조:
                author_element = item.find_element(By.CSS_SELECTOR, "[class*='ContentAuthor__author']") # span.ContentAuthor__author--6n_1d 등
                author = author_element.text.strip() # 작가명 앞뒤 공백 제거

                # 평점
                # 이전 구조: item.find_element(By.CSS_SELECTOR, "div.rating_type strong").text
                # 현재 구조:
                rating_element = item.find_element(By.CSS_SELECTOR, "span[class*='Rating__star_area'] span.text") # span.Rating__star_area--EN06X > span.text
                rating = rating_element.text.strip()

                webtoon_data.append({
                    "thumbnail_url": thumbnail_url,
                    "webtoon_url": webtoon_url,
                    "title": title,
                    "author": author,
                    "rating": rating
                })

            except Exception as e:
                # 간혹 광고나 다른 구조의 아이템이 있을 수 있으므로 오류 발생 시 해당 아이템은 건너뜁니다.
                print(f"하나의 웹툰 아이템 처리 중 오류 발생: {e}")
                # 현재 아이템의 HTML 구조를 출력하여 디버깅에 도움
                try:
                    print(f"오류 발생 아이템 HTML: {item.get_attribute('outerHTML')[:500]}...") # 너무 길면 잘라서 출력
                except:
                    pass
                continue

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
    finally:
        driver.quit()

    return webtoon_data

if __name__ == "__main__":
    print("네이버 월요 웹툰 크롤링을 시작합니다...")
    monday_webtoons = scrape_naver_monday_webtoons()

    if monday_webtoons:
        print(f"\n총 {len(monday_webtoons)}개의 월요 웹툰 정보를 가져왔습니다.")
        for i, webtoon in enumerate(monday_webtoons):
            print(f"\n--- {i+1}번째 웹툰 ---")
            print(f"제목: {webtoon['title']}")
            print(f"작가: {webtoon['author']}")
            print(f"평점: {webtoon['rating']}")
            print(f"썸네일 URL: {webtoon['thumbnail_url']}")
            print(f"웹툰 URL: {webtoon['webtoon_url']}")
    else:
        print("웹툰 정보를 가져오지 못했습니다.")