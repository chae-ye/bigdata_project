print("네이버 맛집 검색")

#blog.py에서 함수를 만들어 모듈을 포함시켜서 활용
#여기에 메인 프로그램 제작
#맛집 검색: 여기메 맛집 입력시 blog함수로 이동해
#결과가 나오는 프로그램 만들기

# main_program.py
from blog2 import search_naver_blog # blog_search_module.py 파일에서 함수 임포트

def main():
    print("네이버 맛집 블로그 검색 프로그램")
    print("-" * 30)

    # 중요: 네이버 개발자 센터에서 발급받은 본인의 Client ID와 Secret으로 변경해야 합니다.
    # 제공해주신 ID와 Secret을 사용합니다.
    client_id = "4adGOKprONP_kdGxk87w"
    client_secret = "6qnNRxAkZ0"

    if client_id == "YOUR_NAVER_CLIENT_ID" or client_secret == "YOUR_NAVER_CLIENT_SECRET": # 초기값 방지
        print("\n[오류] Naver API Client ID와 Secret을 main_program.py 파일 내에서 실제 값으로 설정해주세요.")
        print("네이버 개발자 센터(https://developers.naver.com/apps/#/list)에서 애플리케이션을 등록하고")
        print("Client ID와 Client Secret을 확인하여 코드에 입력해야 정상적으로 작동합니다.")
        return

    search_query_keyword = input("맛집 검색 키워드를 입력하세요 (예: 강남역 파스타): ")

    if not search_query_keyword.strip():
        print("검색어를 입력해주세요. 프로그램을 종료합니다.")
        return

    print(f"\n'{search_query_keyword}' 맛집을 검색합니다...")
    blog_results = search_naver_blog(search_query_keyword, client_id, client_secret, display_count=5) # 최대 5개 결과 요청

    if blog_results is not None: # None이 아닌 경우 (API 호출 성공, 결과가 있거나 없을 수 있음)
        if blog_results: # 결과 리스트에 내용이 있는 경우
            print(f"\n--- '{search_query_keyword}' 검색 결과 ---")
            for i, item in enumerate(blog_results):
                print(f"\n[블로그 {i+1}]")
                print(f"  제목: {item['title']}")
                print(f"  링크: {item['link']}")
        else: # 빈 리스트가 반환된 경우 (검색 결과 없음)
            print(f"\n'{search_query_keyword}'에 대한 블로그 검색 결과가 없습니다.")
    else: # None이 반환된 경우 (API 호출 중 오류 발생)
        print("\n검색 중 오류가 발생했습니다. API 설정을 확인하거나 네트워크 상태를 점검해주세요.")
        print("Client ID와 Secret이 정확한지, API 사용 할당량을 초과하지 않았는지 확인해보세요.")

    print("-" * 30)
    print("프로그램을 종료합니다.")

if __name__ == "__main__":
    main()