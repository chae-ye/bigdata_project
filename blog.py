# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
import json

print("네이버 맛집 검색")

# 커밋전에 삭제
client_id = " "
client_secret = " "

encText = urllib.parse.quote("경성대 맛집")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
json_data = ""
if(rescode==200):
    response_body = response.read()
    # print(response_body.decode('utf-8'))
    json_data = response_body.decode('utf-8')
else:
    print("Error Code:" + rescode)

# Parse the JSON data
data = json.loads(json_data)

# Extract the required information from the 'items' list
extracted_list = []
for item in data['items']:
    extracted_item = {
        "title": item.get("title", ""),
        "link": item.get("link", ""),
        "description": item.get("description", ""),
        "bloggername": item.get("bloggername", ""),
        "postdate": item.get("postdate", "")
    }
    extracted_list.append(extracted_item)

# Print the extracted data
for item in extracted_list:
    print("제목:", item['title'])
    print("링크:", item['link'])