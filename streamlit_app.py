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

# 사이드바 로고 표시
st.sidebar.image("logo.png", use_column_width=True)
st.title(":books: 청년 실생활 정보 도우미")
st.markdown("청년, 대학생, 사회초년생을 위한 맞춤 정보 플랫폼입니다!")
st.caption("모바일처럼 편리하게, 필요한 생활 정보를 한눈에 확인하세요.")
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
      def show_real_estate_procedure():
    st.title("🏡 부동산 계약 절차 안내")

    tab1, tab2 = st.tabs(["전월세 계약 절차", "주택 매매 계약 절차"])

    with tab1:
        st.subheader("📋 전월세 계약 절차")
        steps_lease = [
            "1. **주택 탐색**: 인터넷 부동산 플랫폼 또는 공인중개사 이용",
            "2. **방문 및 확인**: 구조, 시설, 주변환경 확인",
            "3. **계약 전 점검**: 등기부등본 확인 → 집주인 여부, 근저당권 등 확인",
            "4. **계약 체결**: 중개사 입회하에 계약서 작성 → 특약사항 기재",
            "5. **계약금 지급**: 계약금(보통 총액의 10%)을 지급",
            "6. **중도금, 잔금 처리**: 계약 조건에 따라 분할 지급",
            "7. **전입신고 및 확정일자**: 계약서 지참 후 주민센터 신고",
            "8. **열쇠 인수 및 입주**: 잔금 지급 후 입주"
        ]
        for step in steps_lease:
            st.markdown(step)

    with tab2:
        st.subheader("📋 주택 매매 계약 절차")
        steps_sale = [
            "1. **매물 탐색 및 선정**: 실거래가 조회, 매물 정보 확인",
            "2. **방문 및 실물 확인**: 구조, 입지, 하자 여부 직접 점검",
            "3. **권리관계 확인**: 등기부등본, 토지대장, 건축물대장 확인",
            "4. **계약서 작성**: 공인중개사 입회 하에 계약서 작성",
            "5. **계약금 지급**: 매매 대금의 일부를 계약금으로 지급",
            "6. **중도금, 잔금 지급 및 소유권 이전**: 잔금 지급 시 소유권 이전 등기 진행, 취득세 신고 및 납부",
            "7. **입주 및 전입신고**: 실입주 또는 임대 시 전입신고"
        ]
        for step in steps_sale:
            st.markdown(step)
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
