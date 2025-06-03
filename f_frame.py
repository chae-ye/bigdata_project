import random
import csv
import os

# --- 임시 데이터 생성 (검색어 순위) ---
# 실제로는 이 데이터를 API나 데이터베이스에서 가져와야 합니다.
baemin_keywords = [f"배민인기검색어_{i:02d}" for i in range(1, 31)] # 30개 예시 검색어
# 예: ["떡볶이", "치킨", "마라탕", "피자", "족발", ... ] 등으로 실제 데이터 대체 가능
yogiyo_keywords = [f"요기요추천검색어_{i:02d}" for i in range(1, 26)] # 25개 예시 검색어

# --- 프로그램 시작 ---
while True: # 메인 메뉴 루프
    print("\n========= 배달앱 선택 =========")
    print("1. 배달의 민족")
    print("2. 요기요")
    print("3. 종료")
    print("==============================")
    main_choice = input("원하는 번호를 입력해주세요: ")

    if main_choice == '1': # 배달의 민족 선택
        while True: # 배달의 민족 서브 메뉴 루프
            print("\n--- 배달의 민족 ---")
            print("A: 검색 순위 5")
            print("B: 검색 순위 10")
            print("C: 검색 순위 20")
            print("D: 20개의 메뉴 중에 랜덤으로 1개의 메뉴 추천") # 설명 문구 수정
            print("E: 20개의 메뉴를 CSV 파일로 저장")
            print("R: 메인화면으로 돌아가기")
            print("X: 프로그램 종료")
            sub_choice_baemin = input("선택: ").upper()

            if sub_choice_baemin == 'A':
                # --- 검색어순위 5 표시 (배달의 민족) ---
                app_name_bm = "배달의 민족"
                keywords_bm = baemin_keywords
                count_bm = 5
                print(f"\n--- {app_name_bm} 검색어 순위 Top {count_bm} ---")
                if not keywords_bm:
                    print("표시할 검색어 순위 정보가 없습니다.")
                else:
                    actual_count_bm = min(count_bm, len(keywords_bm))
                    if actual_count_bm == 0:
                        print("표시할 검색어 순위 정보가 없습니다.")
                    else:
                        for i in range(actual_count_bm):
                            print(f"{i+1}. {keywords_bm[i]}")
                print("------------------------------")
            
            elif sub_choice_baemin == 'B':
                # --- 검색어순위 10 표시 (배달의 민족) ---
                app_name_bm = "배달의 민족"
                keywords_bm = baemin_keywords
                count_bm = 10
                print(f"\n--- {app_name_bm} 검색어 순위 Top {count_bm} ---")
                if not keywords_bm:
                    print("표시할 검색어 순위 정보가 없습니다.")
                else:
                    actual_count_bm = min(count_bm, len(keywords_bm))
                    if actual_count_bm == 0:
                        print("표시할 검색어 순위 정보가 없습니다.")
                    else:
                        for i in range(actual_count_bm):
                            print(f"{i+1}. {keywords_bm[i]}")
                print("------------------------------")

            elif sub_choice_baemin == 'C':
                # --- 검색어순위 20 표시 (배달의 민족) ---
                app_name_bm = "배달의 민족"
                keywords_bm = baemin_keywords
                count_bm = 20
                print(f"\n--- {app_name_bm} 검색어 순위 Top {count_bm} ---")
                if not keywords_bm:
                    print("표시할 검색어 순위 정보가 없습니다.")
                else:
                    actual_count_bm = min(count_bm, len(keywords_bm))
                    if actual_count_bm == 0:
                        print("표시할 검색어 순위 정보가 없습니다.")
                    else:
                        for i in range(actual_count_bm):
                            print(f"{i+1}. {keywords_bm[i]}")
                print("------------------------------")

            elif sub_choice_baemin == 'D':
                # --- 랜덤 추천 (배달의 민족 검색어) ---
                app_name_bm = "배달의 민족"
                keywords_bm = baemin_keywords
                limit_bm = 20
                # 메뉴 설명에 따라 "20개의 검색어 순위 중"으로 해석하여 로직 유지
                print(f"\n--- {app_name_bm} 랜덤 추천 (상위 {limit_bm}개 검색어 대상) ---")
                if not keywords_bm:
                    print("추천할 검색어 정보가 없습니다.")
                else:
                    target_keywords_bm = keywords_bm[:min(limit_bm, len(keywords_bm))]
                    if not target_keywords_bm:
                        print("추천할 검색어 정보가 없습니다.")
                    else:
                        recommended_bm = random.choice(target_keywords_bm)
                        print(f"오늘의 추천 검색어: {recommended_bm}")
                print("------------------------------")

            elif sub_choice_baemin == 'E':
                # --- CSV 파일로 저장 (배달의 민족 검색어 순위) ---
                app_name_bm = "배달의 민족"
                keywords_bm = baemin_keywords
                filename_prefix_bm = "baemin_keywords" # 파일명 변경
                if not keywords_bm:
                    print(f"\n{app_name_bm}: 저장할 검색어 순위 정보가 없습니다.")
                else:
                    filename_bm = f"{filename_prefix_bm}_rankings_{random.randint(1000,9999)}.csv"
                    try:
                        with open(filename_bm, 'w', newline='', encoding='utf-8-sig') as csvfile_bm:
                            writer_bm = csv.writer(csvfile_bm)
                            writer_bm.writerow(['순위', '검색어']) # CSV 헤더 변경
                            for i, keyword_bm in enumerate(keywords_bm):
                                writer_bm.writerow([i+1, keyword_bm])
                        print(f"\n{app_name_bm}: 검색어 순위가 '{os.path.abspath(filename_bm)}' 파일로 저장되었습니다.")
                    except IOError:
                        print(f"\n{app_name_bm}: 파일 저장 중 오류가 발생했습니다.")
                print("------------------------------")

            elif sub_choice_baemin == 'R':
                print("처음 메뉴로 돌아갑니다.")
                break 
            elif sub_choice_baemin == 'X':
                print("프로그램을 종료합니다.")
                exit() 
            else:
                print("잘못된 입력입니다. 다시 선택해주세요.")
    
    elif main_choice == '2': # 요기요 선택
        while True: # 요기요 서브 메뉴 루프
            print("\n------ 요기요 ------")
            print("a: 검색어순위 5")
            print("b: 검색어순위 10")
            print("c: 검색어순위 20")
            print("d: 20개의 검색어 순위중 랜덤으로 1개 추천") # 설명 문구 수정
            print("e: CSV 파일로 저장")
            print("r: 처음으로 돌아가기")
            print("x: 프로그램 종료")
            sub_choice_yogiyo = input("선택: ").lower()

            if sub_choice_yogiyo == 'a':
                # --- 검색어순위 5 표시 (요기요) ---
                app_name_yg = "요기요"
                keywords_yg = yogiyo_keywords
                count_yg = 5
                print(f"\n--- {app_name_yg} 검색어 순위 Top {count_yg} ---")
                if not keywords_yg:
                    print("표시할 검색어 순위 정보가 없습니다.")
                else:
                    actual_count_yg = min(count_yg, len(keywords_yg))
                    if actual_count_yg == 0:
                        print("표시할 검색어 순위 정보가 없습니다.")
                    else:
                        for i in range(actual_count_yg):
                            print(f"{i+1}. {keywords_yg[i]}")
                print("------------------------------")
            
            elif sub_choice_yogiyo == 'b':
                # --- 검색어순위 10 표시 (요기요) ---
                app_name_yg = "요기요"
                keywords_yg = yogiyo_keywords
                count_yg = 10
                print(f"\n--- {app_name_yg} 검색어 순위 Top {count_yg} ---")
                if not keywords_yg:
                    print("표시할 검색어 순위 정보가 없습니다.")
                else:
                    actual_count_yg = min(count_yg, len(keywords_yg))
                    if actual_count_yg == 0:
                        print("표시할 검색어 순위 정보가 없습니다.")
                    else:
                        for i in range(actual_count_yg):
                            print(f"{i+1}. {keywords_yg[i]}")
                print("------------------------------")

            elif sub_choice_yogiyo == 'c':
                # --- 검색어순위 20 표시 (요기요) ---
                app_name_yg = "요기요"
                keywords_yg = yogiyo_keywords
                count_yg = 20
                print(f"\n--- {app_name_yg} 검색어 순위 Top {count_yg} ---")
                if not keywords_yg:
                    print("표시할 검색어 순위 정보가 없습니다.")
                else:
                    actual_count_yg = min(count_yg, len(keywords_yg))
                    if actual_count_yg == 0:
                        print("표시할 검색어 순위 정보가 없습니다.")
                    else:
                        for i in range(actual_count_yg):
                            print(f"{i+1}. {keywords_yg[i]}")
                print("------------------------------")

            elif sub_choice_yogiyo == 'd':
                # --- 랜덤 추천 (요기요 검색어) ---
                app_name_yg = "요기요"
                keywords_yg = yogiyo_keywords
                limit_yg = 20
                print(f"\n--- {app_name_yg} 랜덤 추천 (상위 {limit_yg}개 검색어 대상) ---")
                if not keywords_yg:
                    print("추천할 검색어 정보가 없습니다.")
                else:
                    target_keywords_yg = keywords_yg[:min(limit_yg, len(keywords_yg))]
                    if not target_keywords_yg:
                        print("추천할 검색어 정보가 없습니다.")
                    else:
                        recommended_yg = random.choice(target_keywords_yg)
                        print(f"오늘의 추천 검색어: {recommended_yg}")
                print("------------------------------")
            
            elif sub_choice_baemin == 'E':
                # --- CSV 파일로 저장 (배달의 민족 검색어 순위) ---
                app_name_bm = "배달의 민족"
                keywords_bm = baemin_keywords
                filename_prefix_bm = "baemin_keywords" # 파일명 변경
                if not keywords_bm:
                    print(f"\n{app_name_bm}: 저장할 검색어 순위 정보가 없습니다.")
                else:
                    filename_bm = f"{filename_prefix_bm}_rankings_{random.randint(1000,9999)}.csv"
                    try:
                        with open(filename_bm, 'w', newline='', encoding='utf-8-sig') as csvfile_bm:
                            writer_bm = csv.writer(csvfile_bm)
                            writer_bm.writerow(['순위', '검색어']) # CSV 헤더 변경
                            for i, keyword_bm in enumerate(keywords_bm):
                                writer_bm.writerow([i+1, keyword_bm])
                        print(f"\n{app_name_bm}: 검색어 순위가 '{os.path.abspath(filename_bm)}' 파일로 저장되었습니다.")
                    except IOError:
                        print(f"\n{app_name_bm}: 파일 저장 중 오류가 발생했습니다.")
                print("------------------------------")

            elif sub_choice_yogiyo == 'r':
                print("처음 메뉴로 돌아갑니다.")
                break 
            elif sub_choice_yogiyo == 'x':
                print("프로그램을 종료합니다.")
                exit() 
            else:
                print("잘못된 입력입니다. 다시 선택해주세요.")

    elif main_choice == '3': # 종료 선택
        print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")
        break 
    else:
        print("잘못된 입력입니다. 1, 2, 3 중에서 선택해주세요.")