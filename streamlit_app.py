import streamlit as st
st.set_page_config(page_title="청년 실생활 정보 가이드", layout="wide")

from utils.helper import get_topic_data, get_related_news

from googletrans import Translator

import requests

import json

from bs4 import BeautifulSoup

import urllib.parse

import re
  
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

                    contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

                    items = contents[0]["itemSectionRenderer"]["contents"]
 
                    for item in items:

                        if "videoRenderer" in item:

                            video = item["videoRenderer"]

                            title = video["title"]["runs"][0]["text"]

                            video_id = video["videoId"]

                            thumbnail = video["thumbnail"]["thumbnails"][-1]["url"]

                            channel = video["ownerText"]["runs"][0]["text"]

                            if re.search(r'[가-힣]', channel):

                                return {

                                    "videoId": video_id,

                                    "title": title,

                                    "thumbnail": thumbnail

                                }

                except Exception as e:

                    print("파싱 에러:", e)

    return None
 
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

 
import streamlit as st

from utils.helper import get_topic_data

from googletrans import Translator

import requests

import json

from bs4 import BeautifulSoup

import urllib.parse

import re

st.set_page_config(page_title="청년 실생활 정보 가이드", layout="wide")

st.title(":books: 청년 실생활 정보 도우미")

st.markdown("청년, 대학생, 사회초년생을 위한 맞춤 정보 플랫폼입니다!")

# 언어 설정

lang = st.selectbox("언어를 선택하세요", ["한국어", "English"])

translator = Translator()

translate = lambda text: translator.translate(text, dest="en").text if lang == "English" else text

# 주제 선택

main_topic = st.selectbox(translate("궁금한 주제를 선택하세요 ⬇"), ["아르바이트", "부동산", "금융", "계약서"])

# 유튜브 검색 기능 (API 없이)

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

    # 계약서 이미지 보기

    if main_topic in ["계약서", "아르바이트"]:

        st.markdown("---")

        st.subheader(translate(":page_with_curl: 계약서 예시/양식 보기"))

        # 대체 가능한 이미지 예시 (직접 업로드한 이미지로 대체 가능)

        st.image("https://cdn.pixabay.com/photo/2017/09/08/08/40/contract-2729580_1280.jpg", caption=translate("표준 근로계약서 예시"))

        st.image("https://cdn.pixabay.com/photo/2017/01/17/15/19/home-1988086_1280.jpg", caption=translate("임대차 계약서 예시"))

    # 부동산 관련 사이트 링크

    if main_topic == "부동산":

        st.markdown("---")

        st.subheader(translate(":house: 관련 공식 사이트 안내"))

        st.markdown(f"- [{translate('청약홈 (LH 공사)')}](https://www.applyhome.co.kr)")

        st.markdown(f"- [{translate('부동산 계약 절차 가이드 - 국토교통부')}](https://www.molit.go.kr)")

        st.markdown(f"- [{translate('주택도시기금 - 버팀목 대출')}](https://nhuf.molit.go.kr)")

        st.info(translate("청약 신청, 임대차 보호법, 대출 상품 등을 제공하는 공식 사이트입니다. 꼭 참고하세요."))

    # 뉴스 보기 (모든 주제에 대해 공통)

    st.markdown("---")

    st.subheader(translate(":newspaper: 관련 네이버 뉴스 보기"))

    if main_topic and sub_topic:

        naver_news_url = f"https://search.naver.com/search.naver?where=news&query={main_topic}+{sub_topic}"

        st.markdown(f"[{translate(main_topic + ' ' + sub_topic)} 관련 네이버 뉴스 보기]({naver_news_url})")

    # 유튜브 영상 보기

    st.markdown("---")

    st.subheader(translate(":tv: 관련 유튜브 영상 보기"))

    youtube_info = get_youtube_video_info(f"{main_topic} {sub_topic}")

    if youtube_info:

        st.image(youtube_info["thumbnail"], caption=translate(youtube_info["title"]))

        st.markdown(f"[YouTube에서 영상 보기](https://www.youtube.com/watch?v={youtube_info['videoId']})")

    else:

        st.info(translate("관련 유튜브 영상을 찾을 수 없습니다."))

    # 의견 남기기

    st.markdown("---")

    st.info(translate("원하는 정보가 부족하다면 아래에 의견을 남겨주세요!"))

    feedback = st.text_area(translate("궁금한 점이나 요청하고 싶은 내용을 적어주세요"))

    if st.button(translate("제출")):

        st.success(translate("소중한 의견 감사합니다! 빠른 시일 내 반영하겠습니다."))
 
