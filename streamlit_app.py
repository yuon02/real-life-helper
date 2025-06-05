import streamlit as st
from utils.helper import get_topic_data
from googletrans import Translator
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import re

# 페이지 설정
st.set_page_config(page_title="청년 실생활 정보 가이드", layout="wide")

# ✅ 로고 이미지 상단에 표시
st.image("https://raw.githubusercontent.com/yuon02/real-life-helper/main/logo.png", width=120)
st.markdown("<h1 style='color:#3F72AF;'>청년 실생활 정보 도우미</h1>", unsafe_allow_html=True)
st.caption("모바일처럼 편리하게, 필요한 생활 정보를 한눈에 확인하세요.")

# 언어 설정
lang = st.selectbox("🌐 언어 선택", ["한국어", "English"])
translator = Translator()
translate = lambda text: translator.translate(text, dest="en").text if lang == "English" else text

# 주제 선택
main_topic = st.selectbox("📌 주제를 선택하세요", ["아르바이트", "부동산", "금융", "계약서"])

# 유튜브 크롤링 함수
def get_youtube_video_info(query):
    headers = {"User-Agent": "Mozilla/5.0"}
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
                    print("파싱 오류:", e)
    return None

# 뉴스 미리보기 함수
def get_news_snippets(query):
    try:
        search_query = urllib.parse.quote(query)
        url = f"https://search.naver.com/search.naver?where=news&query={search_query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".news_wrap.api_ani_send")
        news = []
        for item in items[:5]:
            title_tag = item.select_one(".news_tit")
            summary_tag = item.select_one(".dsc_wrap")
            if title_tag and summary_tag:
                news.append({
                    "title": title_tag.get("title"),
                    "link": title_tag.get("href"),
                    "summary": summary_tag.get_text()
                })
        return news
    except Exception as e:
        return []

# 주제별 정보 가져오기
if main_topic:
    topic_data = get_topic_data(main_topic)
    if topic_data:
        sub_topic = st.radio(translate("세부 항목을 골라보세요"), list(topic_data.keys()))

        # ✅ 탭 구조 (모바일 스타일)
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            translate("📖 정보 보기"),
            translate("📰 관련 뉴스"),
            translate("📄 계약서 양식"),
            translate("🎬 유튜브 영상"),
            translate("💬 의견 남기기")
        ])

        # 🟦 탭 1: 정보 보기
        with tab1:
            st.subheader(translate("📖 선택한 정보"))
            item = topic_data.get(sub_topic, {})
            if isinstance(item, dict):
                content = item.get("내용", "정보 없음")
                source = item.get("출처", "")
                st.success(translate(content))
                if source:
                    st.markdown(f"🔗 출처: [{source}]({source})")
            else:
                st.success(translate(item))

        # 🟦 탭 2: 뉴스
        with tab2:
            st.subheader(translate("📰 관련 뉴스 보기"))
            news_items = get_news_snippets(f"{main_topic} {sub_topic}")
            if news_items:
                for news in news_items:
                    st.markdown(f"**[{news['title']}]({news['link']})**")
                    st.caption(news['summary'])
            else:
                st.warning(translate("관련 뉴스를 찾을 수 없습니다."))

        # 🟦 탭 3: 계약서 예시
        with tab3:
            if main_topic in ["계약서", "아르바이트"]:
                st.subheader(translate("📄 계약서 예시 및 다운로드"))
                pdf_url = "https://inpyeonglaw.com/wp-content/uploads/2025/03/%EA%B0%9C%EC%A0%95-%ED%91%9C%EC%A4%80%EC%B7%A8%EC%97%85%EA%B7%9C%EC%B9%992025%EB%85%84-%EB%B0%B0%ED%8F%AC.pdf"
                st.markdown(f"[📎 표준 근로계약서 PDF 열기]({pdf_url})")
                st.image("static/sample_contract.png", caption="법무부 계약서 예시")
                st.markdown("[👉 전체 계약서 보기](https://viewer.moj.go.kr/skin/doc.html?rs=/result/bbs/118&fn=temp_1681802272120100)")
            else:
                st.info(translate("계약서 관련 항목에서만 양식이 제공됩니다."))

        # 🟦 탭 4: 유튜브 영상
        with tab4:
            st.subheader(translate("🎬 유튜브 영상"))
            video = get_youtube_video_info(f"{main_topic} {sub_topic}")
            if video:
                st.image(video["thumbnail"], caption=translate(video["title"]))
                st.markdown(f"[🔗 영상 보기](https://www.youtube.com/watch?v={video['videoId']})")
            else:
                st.warning(translate("유튜브 영상을 찾을 수 없습니다."))

        # 🟦 탭 5: 의견 남기기
        with tab5:
            st.subheader(translate("💬 의견 남기기"))
            feedback = st.text_area(translate("궁금한 점이나 요청하고 싶은 내용을 적어주세요"))
            if st.button(translate("제출")):
                st.success(translate("소중한 의견 감사합니다! 빠른 시일 내 반영하겠습니다."))
    else:
        st.warning(translate("선택한 주제에 대한 정보가 없습니다."))
