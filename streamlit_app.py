import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import json
from googletrans import Translator

# ✅ 반드시 첫 번째 Streamlit 명령어로 위치시킴
st.set_page_config(page_title="청년 실생활 정보 가이드", layout="wide")

# ✅ 그 이후에 다른 코드 작성
st.image("logo.png", width=150)

# 타이틀 및 설명
st.title(":books: 청년 실생활 정보 도우미")
st.markdown("청년, 대학생, 사회초년생을 위한 맞춤 정보 플랫폼입니다!")
# 언어 선택
lang = st.selectbox("언어를 선택하세요", ["한국어", "English"])
translator = Translator()
translate = lambda text: translator.translate(text, dest="en").text if lang == "English" else text
# 주제 선택
main_topic = st.selectbox(translate("궁금한 주제를 선택하세요 ⬇"), ["아르바이트", "부동산", "금융", "계약서"])
# 유튜브 영상 정보 크롤링 함수 (API 없이 동작)
def get_youtube_video_info(query):
   headers = {
       "User-Agent": "Mozilla/5.0"
   }
   search_query = urllib.parse.quote(query)
   url = f"https://www.youtube.com/results?search_query={search_query}"
   response = requests.get(url, headers=headers)
   soup = BeautifulSoup(response.text, "html.parser")
   for script in soup.find_all("script"):
       if "var ytInitialData" in script.text:
           match = re.search(r'var ytInitialData = ({.*?});', script.string or "", re.DOTALL)
           if match:
               try:
                   data = json.loads(match.group(1))
                   items = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
                   for item in items:
                       if "videoRenderer" in item:
                           video = item["videoRenderer"]
                           title = video["title"]["runs"][0]["text"]
                           video_id = video["videoId"]
                           thumbnail = video["thumbnail"]["thumbnails"][-1]["url"]
                           return {
                               "videoId": video_id,
                               "title": title,
                               "thumbnail": thumbnail
                           }
               except Exception as e:
                   print("파싱 에러:", e)
   return None
# 본문 실행
if main_topic:
   topic_data = get_topic_data(main_topic)
   sub_topic = st.radio(translate(":mag: 세부 항목을 골라보세요"), list(topic_data.keys()))
   st.markdown("---")
   st.subheader(translate(":bulb: 관련 정보"))
   item = topic_data.get(sub_topic, {})
   if isinstance(item, dict):
       content = item.get("내용", "정보 없음")
       source = item.get("출처", "")
       st.success(translate(content))
       if source:
           st.markdown(f"\n출처: [{source}]({source})")
   else:
       st.success(translate(item))
   # ✅ 계약서 및 아르바이트 관련 양식 표시
   if main_topic in ["계약서", "아르바이트"]:
       st.markdown("---")
       st.subheader(translate(":page_with_curl: 계약서 예시/양식 보기"))
       # ✅ 외부 PDF 링크로 제공 (2025년 PDF)
       pdf_url = "https://inpyeonglaw.com/wp-content/uploads/2025/03/%EA%B0%9C%EC%A0%95-%ED%91%9C%EC%A4%80%EC%B7%A8%EC%97%85%EA%B7%9C%EC%B9%992025%EB%85%84-%EB%B0%B0%ED%8F%AC.pdf"
       st.markdown(f"[📄 표준 근로계약서 PDF 열기]({pdf_url})")
       # ✅ 계약서 예시 이미지 및 사이트 링크
       st.image("https://viewer.moj.go.kr/images/sub/skin/skinDoc_01.gif", caption="법무부 계약서 예시 이미지")
       st.markdown("[👉 법무부 계약서 전체 보기](https://viewer.moj.go.kr/skin/doc.html?rs=/result/bbs/118&fn=temp_1681802272120100)")
             # ✅ 서울법원 계약서 목록 출력
       st.markdown("---")
       st.subheader(translate("📚 서울법원 계약서 양식 모음"))
       contracts = get_seoulcourt_contracts()
       if contracts:
           for name, link in contracts:
               st.markdown(f"- [{translate(name)}]({link})")
       else:
           st.warning(translate("서울법원 계약서 목록을 불러올 수 없습니다."))

   # ✅ 부동산 관련 사이트 안내
   if main_topic == "부동산":
       st.markdown("---")
       st.subheader(translate(":house: 관련 공식 사이트 안내"))
       st.markdown(f"- [{translate('청약홈 (LH 공사)')}](https://www.applyhome.co.kr)")
       st.markdown(f"- [{translate('부동산 계약 절차 가이드 - 국토교통부')}](https://www.molit.go.kr)")
       st.markdown(f"- [{translate('주택도시기금 - 버팀목 대출')}](https://nhuf.molit.go.kr)")
       st.info(translate("청약 신청, 임대차 보호법, 대출 상품 등을 제공하는 공식 사이트입니다. 꼭 참고하세요."))
       # ✅ 부동산 뉴스 링크 추가
       st.markdown("---")
       st.subheader(translate(":newspaper: 부동산 관련 뉴스 보기"))
       st.markdown("[네이버 뉴스 검색 결과 보기](https://search.naver.com/search.naver?where=news&query=부동산)")
   # ✅ 네이버 뉴스 링크 (모든 항목 공통)
   st.markdown("---")
   st.subheader(translate(":newspaper: 관련 네이버 뉴스 보기"))
   naver_news_url = f"https://search.naver.com/search.naver?where=news&query={main_topic}+{sub_topic}"
   st.markdown(f"[{translate(main_topic + ' ' + sub_topic)} 관련 뉴스 보기]({naver_news_url})")
   # ✅ 유튜브 영상 출력
   st.markdown("---")
   st.subheader(translate(":tv: 관련 유튜브 영상 보기"))
   youtube_info = get_youtube_video_info(f"{main_topic} {sub_topic}")
   if youtube_info:
       st.image(youtube_info["thumbnail"], caption=translate(youtube_info["title"]))
       st.markdown(f"[YouTube에서 영상 보기](https://www.youtube.com/watch?v={youtube_info['videoId']})")
   else:
       st.info(translate("관련 유튜브 영상을 찾을 수 없습니다."))
   # ✅ 사용자 의견 입력
   st.markdown("---")
   st.info(translate("원하는 정보가 부족하다면 아래에 의견을 남겨주세요!"))
   feedback = st.text_area(translate("궁금한 점이나 요청하고 싶은 내용을 적어주세요"))
   if st.button(translate("제출")):
       st.success(translate("소중한 의견 감사합니다! 빠른 시일 내 반영하겠습니다."))
 
import streamlit as st
# ✅ 페이지 설정
st.set_page_config(page_title="청년 실생활 정보 가이드", layout="wide")
from utils.helper import get_topic_data
from googletrans import Translator
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import re
# 타이틀 및 소개
st.title(":books: 청년 실생활 정보 도우미")
st.markdown("청년, 대학생, 사회초년생을 위한 맞춤 정보 플랫폼입니다!")
# 언어 선택
lang = st.selectbox("언어를 선택하세요", ["한국어", "English"])
translator = Translator()
translate = lambda text: translator.translate(text, dest="en").text if lang == "English" else text
# 주제 선택
main_topic = st.selectbox(translate("궁금한 주제를 선택하세요 ⬇"), ["아르바이트", "부동산", "금융", "계약서"])
# 유튜브 영상 검색 함수
def get_youtube_video_info(query):
   headers = {
       "User-Agent": "Mozilla/5.0"
   }
   search_query = urllib.parse.quote(query)
   url = f"https://www.youtube.com/results?search_query={search_query}"
   response = requests.get(url, headers=headers)
   soup = BeautifulSoup(response.text, "html.parser")
   for script in soup.find_all("script"):
       if "var ytInitialData" in script.text:
           match = re.search(r'var ytInitialData = ({.*?});', script.string or "", re.DOTALL)
           if match:
               try:
                   data = json.loads(match.group(1))
                   items = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
                   for item in items:
                       if "videoRenderer" in item:
                           video = item["videoRenderer"]
                           title = video["title"]["runs"][0]["text"]
                           video_id = video["videoId"]
                           thumbnail = video["thumbnail"]["thumbnails"][-1]["url"]
                           return {
                               "videoId": video_id,
                               "title": title,
                               "thumbnail": thumbnail
                           }
               except Exception as e:
                   print("파싱 에러:", e)
   return None
# 메인 로직
if main_topic:
   topic_data = get_topic_data(main_topic)
   sub_topic = st.radio(translate(":mag: 세부 항목을 골라보세요"), list(topic_data.keys()))
   st.markdown("---")
   st.subheader(translate(":bulb: 관련 정보"))
   item = topic_data.get(sub_topic, {})
   if isinstance(item, dict):
       content = item.get("내용", "정보 없음")
       source = item.get("출처", "")
       st.success(translate(content))
       if source:
           st.markdown(f"\n출처: [{source}]({source})")
   else:
       st.success(translate(item))
   # ✅ 계약서 및 아르바이트 관련 파일/이미지
   if main_topic in ["계약서", "아르바이트"]:
       st.markdown("---")
       st.subheader(translate(":page_with_curl: 계약서 예시/양식 보기"))
       # ✅ 외부 PDF 링크 (2025년)
       pdf_url = "https://inpyeonglaw.com/wp-content/uploads/2025/03/%EA%B0%9C%EC%A0%95-%ED%91%9C%EC%A4%80%EC%B7%A8%EC%97%85%EA%B7%9C%EC%B9%992025%EB%85%84-%EB%B0%B0%ED%8F%AC.pdf"
       st.markdown(f"[📄 표준 근로계약서 PDF 열기]({pdf_url})")
       # ✅ 법무부 예시 이미지 및 링크
       st.image("https://viewer.moj.go.kr/images/sub/skin/skinDoc_01.gif", caption="법무부 계약서 예시 이미지")
       st.markdown("[👉 법무부 계약서 전체 보기](https://viewer.moj.go.kr/skin/doc.html?rs=/result/bbs/118&fn=temp_1681802272120100)")
   # ✅ 부동산 관련 공식 정보 및 뉴스 추가
   if main_topic == "부동산":
       st.markdown("---")
       st.subheader(translate(":house: 관련 공식 사이트 안내"))
       st.markdown(f"- [{translate('청약홈 (LH 공사)')}](https://www.applyhome.co.kr)")
       st.markdown(f"- [{translate('부동산 계약 절차 가이드 - 국토교통부')}](https://www.molit.go.kr)")
       st.markdown(f"- [{translate('주택도시기금 - 버팀목 대출')}](https://nhuf.molit.go.kr)")
       st.info(translate("청약 신청, 임대차 보호법, 대출 상품 등을 제공하는 공식 사이트입니다. 꼭 참고하세요."))
       # ✅ 부동산 뉴스 (집값 + 정책)
       st.markdown("---")
       st.subheader(translate(":newspaper: 부동산 관련 뉴스 보기"))
       st.markdown("[📈 집값 관련 뉴스 보기](https://search.naver.com/search.naver?where=news&query=집값)")
       st.markdown("[🏛️ 부동산 정책 관련 뉴스 보기](https://search.naver.com/search.naver?where=news&query=부동산+정책)")
   # ✅ 공통 뉴스 섹션
   st.markdown("---")
   st.subheader(translate(":newspaper: 관련 네이버 뉴스 보기"))
   naver_news_url = f"https://search.naver.com/search.naver?where=news&query={main_topic}+{sub_topic}"
   st.markdown(f"[{translate(main_topic + ' ' + sub_topic)} 관련 뉴스 보기]({naver_news_url})")
   # ✅ 유튜브 영상 표시
   st.markdown("---")
   st.subheader(translate(":tv: 관련 유튜브 영상 보기"))
   youtube_info = get_youtube_video_info(f"{main_topic} {sub_topic}")
   if youtube_info:
       st.image(youtube_info["thumbnail"], caption=translate(youtube_info["title"]))
       st.markdown(f"[YouTube에서 영상 보기](https://www.youtube.com/watch?v={youtube_info['videoId']})")
   else:
       st.info(translate("관련 유튜브 영상을 찾을 수 없습니다."))
   # ✅ 사용자 피드백 입력
   st.markdown("---")
   st.info(translate("원하는 정보가 부족하다면 아래에 의견을 남겨주세요!"))
   feedback = st.text_area(translate("궁금한 점이나 요청하고 싶은 내용을 적어주세요"))
   if st.button(translate("제출")):
       st.success(translate("소중한 의견 감사합니다! 빠른 시일 내 반영하겠습니다."))
