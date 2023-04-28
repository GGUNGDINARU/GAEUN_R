#네이버API를 이용하여 뉴스를 크롤링하고 json파일로 결과를 받아보는 프로그램

import os
import sys
import urllib.request
import datetime
import time
import json

#네이버개인애플리케이션 아이디 입력하기
client_id = "yBeCYOpJm4z0LP2glWvo"
client_secret = "1GxLsJ05tP"

#첫 번째 코드 : urllib.request 함수를 통해 url을 받고 클라이언트 아이디 및 시크릿 입력 받기
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#두 번째 코드 : 코드1에 보낼 url을 제작하고
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node #받을 파일 형식 정하기(json)
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)  #첫 번째코드 

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)


#세 번째 코드 : 받고싶은 정보를 변수값에 저장하기
def getPostData(post, jsonResult, cnt):
    title = post['title'] #뉴스제목
    description = post['description'] #메인내용
    org_link = post['originallink'] #뉴스원본링크
    link = post['link'] #뉴스페이지링크

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description,
                       'org_link': org_link, 'link': org_link, 'pDate': pDate})
    return

# [CODE 0]
def main():
    node = 'news'  # 크롤링 할 대상을 결정
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)  #두 번째 코드
    total = jsonResponse['total'] #몇 개의 데이터를 불러왔는지 받는 변수

    #데이터를 하나씩 계속 받는 반복문
    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)  #세 번째 코드

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)  #두 번째 코드

    print('전체 검색 : %d 건' % total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)

        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" % (cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))

#이 파일을 실행시키는곳이 이 파일이랑 동일시할때 실행하는 코드
if __name__ == '__main__':
    main()