import streamlit as st
from utils.helper import get_topic_data, get_related_news
from googletrans import Translator
import requests
import json

st.set_page_config(page_title="청년 실생활 정보 가이드", layout="wide")

st.title(":books: 청년 실생활 정보 도우미")
st.markdown("청년, 대학생, 사회초년생을 위한 맞춤 정보 플랫폼입니다!")

# 언어 선택
lang = st.selectbox("언어를 선택하세요", ["한국어", "English"])
translator = Translator()
translate = lambda text: translator.translate(text, dest="en").text if lang == "English" else text

# 사용자 주제 선택
main_topic = st.selectbox(translate("궁금한 주제를 선택하세요 ⬇"), [
    "아르바이트",
    "부동산",
    "금융",
    "계약서"
])

def get_youtube_video_info(query):
    search_url = f"https://www.googleapis.com/youtube/v3/search"
    video_url = f"https://www.googleapis.com/youtube/v3/videos"
    api_key = st.secrets["YOUTUBE_API_KEY"]

    # 검색 API 호출
    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "regionCode": "KR",
        "maxResults": 5,
        "key": api_key
    }
    search_response = requests.get(search_url, params=search_params)
    search_results = search_response.json().get("items", [])

    # 조회수 높은 영상 조회
    video_ids = [item["id"]["videoId"] for item in search_results]
    if not video_ids:
        return None

    video_params = {
        "part": "snippet,statistics",
        "id": ",".join(video_ids),
        "key": api_key
    }
    video_response = requests.get(video_url, params=video_params)
    video_items = video_response.json().get("items", [])

    # 한국어 채널 필터링 및 조회수 기준 정렬
    korean_videos = [v for v in video_items if v["snippet"].get("defaultAudioLanguage") == "ko"]
    if not korean_videos:
        korean_videos = video_items
    top_video = sorted(korean_videos, key=lambda x: int(x["statistics"].get("viewCount", 0)), reverse=True)[0]
    return {
        "videoId": top_video["id"],
        "title": top_video["snippet"]["title"],
        "thumbnail": top_video["snippet"]["thumbnails"]["high"]["url"]
    }

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

    if main_topic in ["계약서", "아르바이트"]:
        st.markdown("---")
        st.subheader(translate(":page_with_curl: 계약서 예시/양식 보기"))
        st.image("https://img.law.go.kr/image2/2020/05/14/LB00120200514165513875.jpg", caption=translate("표준 근로계약서 예시"))
        st.image("https://img.law.go.kr/image2/2020/05/14/LB00120200514165606448.jpg", caption=translate("임대차 계약서 예시"))

    if main_topic == "부동산":
        st.markdown("---")
        st.subheader(translate(":house: 관련 공식 사이트 안내"))

        st.markdown(f"- [{translate('청약홈 (LH 공사)')}](https://www.applyhome.co.kr)")
        st.markdown(f"- [{translate('부동산 계약 절차 가이드 - 국토교통부')}](https://www.molit.go.kr)")
        st.markdown(f"- [{translate('주택도시기금 - 버팀목 대출')}](https://nhuf.molit.go.kr)")

        st.info(translate("청약 신청, 임대차 보호법, 대출 상품 등을 제공하는 공식 사이트입니다. 꼭 참고하세요."))

    st.markdown("---")
    st.subheader(translate(":newspaper: 관련 네이버 뉴스 보기"))
    if main_topic and sub_topic:
        naver_news_url = f"https://search.naver.com/search.naver?where=news&query={main_topic}+{sub_topic}"
        st.markdown(f"[{translate(main_topic + ' ' + sub_topic)} 관련 네이버 뉴스 보기]({naver_news_url})")

    st.markdown("---")
    st.subheader(translate(":tv: 관련 유튜브 영상 보기"))
    youtube_info = get_youtube_video_info(f"{main_topic} {sub_topic}")
    if youtube_info:
        st.image(youtube_info["thumbnail"], caption=translate(youtube_info["title"]))
        st.markdown(f"[YouTube에서 영상 보기](https://www.youtube.com/watch?v={youtube_info['videoId']})")
    else:
        st.info(translate("관련 유튜브 영상을 찾을 수 없습니다."))

    st.markdown("---")
    st.info(translate("원하는 정보가 부족하다면 아래에 의견을 남겨주세요!"))
    feedback = st.text_area(translate("궁금한 점이나 요청하고 싶은 내용을 적어주세요"))
    if st.button(translate("제출")):
        st.success(translate("소중한 의견 감사합니다! 빠른 시일 내 반영하겠습니다."))
