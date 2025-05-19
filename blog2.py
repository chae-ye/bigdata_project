# blog_search_module.py
import urllib.request
import json

def search_naver_blog(query, client_id, client_secret, display_count=10):
    """
    Naver Blog API를 사용하여 검색 결과를 반환하는 함수

    Args:
        query (str): 검색할 키워드
        client_id (str): Naver API Client ID
        client_secret (str): Naver API Client Secret
        display_count (int): 한 번에 표시할 검색 결과 개수 (기본값: 10)

    Returns:
        list: 검색 결과 아이템 리스트. 각 아이템은 title, link, description,
              bloggername, postdate를 포함하는 딕셔너리.
              에러 발생 시 또는 결과가 없을 시 None 또는 빈 리스트를 반환.
    """
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display_count}" # JSON 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            json_data = response_body.decode('utf-8')
            data = json.loads(json_data)

            extracted_list = []
            if 'items' in data and data['items']: # items가 존재하고, 비어있지 않은 경우
                for item in data['items']:
                    extracted_item = {
                        "title": item.get("title", "제목 없음").replace("<b>", "").replace("</b>", ""), # HTML 태그 제거
                        "link": item.get("link", ""),
                        "description": item.get("description", "").replace("<b>", "").replace("</b>", ""), # HTML 태그 제거
                        "bloggername": item.get("bloggername", ""),
                        "postdate": item.get("postdate", "")
                    }
                    extracted_list.append(extracted_item)
                return extracted_list
            else:
                return [] # 검색 결과가 없는 경우 빈 리스트 반환
        else:
            print(f"API Error Code: {rescode}")
            return None # API 에러 시 None 반환
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # --- 모듈 테스트용 코드 ---
    # 이 코드는 blog_search_module.py를 직접 실행했을 때만 동작합니다.
    print("네이버 맛집 검색 모듈 테스트")

    # !!! 실제 테스트 시에는 아래 ID와 Secret을 본인의 유효한 값으로 교체해야 합니다. !!!
    # 제공해주신 ID와 Secret을 테스트용으로 사용합니다.
    test_client_id = "4adGOKprONP_kdGxk87w"
    test_client_secret = "6qnNRxAkZ0"

    if test_client_id == "YOUR_ACTUAL_CLIENT_ID" or test_client_secret == "YOUR_ACTUAL_CLIENT_SECRET":
        print("테스트를 위해서는 실제 Naver API Client ID와 Secret을 입력해야 합니다.")
    else:
        search_query = "경성대 맛집" # 테스트 검색어
        results = search_naver_blog(search_query, test_client_id, test_client_secret, display_count=3)

        if results is not None: # None이 아닌 경우 (빈 리스트 포함)
            if results: # 결과가 있는 경우
                print(f"\n--- '{search_query}' 검색 결과 (상위 {len(results)}개) ---")
                for i, item in enumerate(results):
                    print(f"\n[결과 {i+1}]")
                    print(f"  제목: {item['title']}")
                    print(f"  링크: {item['link']}")
                    # print(f"  요약: {item['description']}") # 필요시 주석 해제
                    # print(f"  블로거: {item['bloggername']}") # 필요시 주석 해제
                    # print(f"  날짜: {item['postdate']}")   # 필요시 주석 해제
            else: # 빈 리스트인 경우 (검색 결과 없음)
                print(f"'{search_query}'에 대한 검색 결과가 없습니다.")
        else: # None인 경우 (오류 발생)
            print(f"'{search_query}' 검색 중 오류가 발생했습니다.")