from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_first_naver_monday_webtoon():
    """
    네이버 월요 웹툰 목록에서 첫 번째 웹툰의 썸네일, 제목, 작가, 평점을 크롤링합니다.
    """
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    # 웹 드라이버 설정
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        print(f"WebDriver Manager를 통한 드라이버 설정 실패: {e}")
        print("로컬 ChromeDriver를 사용합니다. PATH에 설정되어 있어야 합니다.")
        return None

    # 네이버 웹툰 월요일 목록 페이지 URL
    url = "https://comic.naver.com/webtoon/weekday?week=mon"
    driver.get(url)

    webtoon_data = {}

    try:
        # 첫 번째 웹툰 아이템이 로드될 때까지 최대 10초 대기
        # 네이버 웹툰의 HTML 구조는 동적 클래스명 때문에 자주 변경될 수 있습니다.
        # 좀 더 일반적인 선택자나, 부분 일치 선택자를 사용합니다.
        # 최신 UI 기준 선택자 (예: ul[class^='WeekdayMainView__comics_list'] li[class^='WeekdayMainView__item'])
        # 또는 이전/더 안정적인 구조 선택자 (예: #content div.list_area ul.img_list li)

        # 여기서는 최신 UI를 기준으로 첫 번째 li 아이템을 찾습니다.
        # 더 강력한 대기를 위해 WebDriverWait 사용
        wait = WebDriverWait(driver, 10)
        
        # 리스트 컨테이너가 먼저 로드되기를 기다림
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[class^='WeekdayMainView__comics_list']")))
        
        # 첫 번째 웹툰 아이템 선택
        # find_element (단수) 를 사용하여 첫 번째 일치하는 요소를 가져옵니다.
        first_webtoon_item = driver.find_element(By.CSS_SELECTOR, "ul[class^='WeekdayMainView__comics_list'] > li[class^='WeekdayMainView__item']")

        if not first_webtoon_item:
            print("첫 번째 웹툰 아이템을 찾을 수 없습니다. CSS 선택자를 확인해주세요.")
            # 대체 선택자 시도 (이전 UI 구조)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content div.list_area ul.img_list li")))
                first_webtoon_item = driver.find_element(By.CSS_SELECTOR, "#content div.list_area ul.img_list li")
            except:
                 print("대체 선택자로도 첫 번째 웹툰 아이템을 찾을 수 없습니다.")
                 driver.quit()
                 return None
        
        # 정보 추출
        # 썸네일 이미지 URL
        # 이전 구조: first_webtoon_item.find_element(By.CSS_SELECTOR, "div.thumb img").get_attribute("src")
        thumbnail_img_element = first_webtoon_item.find_element(By.CSS_SELECTOR, "img[class*='Thumbnail__image']")
        thumbnail_url = thumbnail_img_element.get_attribute("src")
        if not thumbnail_url.startswith("http"):
            thumbnail_url = "https://comic.naver.com" + thumbnail_url

        # 제목
        # 이전 구조: first_webtoon_item.find_element(By.CSS_SELECTOR, "a.title").text
        title_element = first_webtoon_item.find_element(By.CSS_SELECTOR, "[class*='ContentTitle__title']")
        title = title_element.text

        # 작가명
        # 이전 구조: first_webtoon_item.find_element(By.CSS_SELECTOR, "a.author").text
        author_element = first_webtoon_item.find_element(By.CSS_SELECTOR, "[class*='ContentAuthor__author']")
        author = author_element.text.strip()

        # 평점
        # 이전 구조: first_webtoon_item.find_element(By.CSS_SELECTOR, "div.rating_type strong").text
        rating_element = first_webtoon_item.find_element(By.CSS_SELECTOR, "span[class*='Rating__star_area'] span.text")
        rating = rating_element.text.strip()

        webtoon_data = {
            "thumbnail_url": thumbnail_url,
            "title": title,
            "author": author,
            "rating": rating
        }

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        try:
            print(f"오류 발생 당시 페이지 소스 일부:\n {driver.page_source[:1000]}") # 디버깅용
        except:
            pass
        return None # 오류 발생 시 None 반환
    finally:
        driver.quit()

    return webtoon_data

if __name__ == "__main__":
    print("네이버 월요 웹툰 중 첫 번째 웹툰 크롤링을 시작합니다...")
    first_webtoon_info = scrape_first_naver_monday_webtoon()

    if first_webtoon_info:
        print("\n--- 첫 번째 웹툰 정보 ---")
        print(f"제목: {first_webtoon_info['title']}")
        print(f"작가: {first_webtoon_info['author']}")
        print(f"평점: {first_webtoon_info['rating']}")
        print(f"썸네일 URL: {first_webtoon_info['thumbnail_url']}")
    else:
        print("웹툰 정보를 가져오지 못했습니다.")