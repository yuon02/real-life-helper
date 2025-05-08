import streamlit as st
from utils.helper import get_topic_data, get_related_news
from googletrans import Translator

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

    # 관련 뉴스 출력
    st.markdown("---")
    st.subheader(translate(":newspaper: 최신 관련 기사"))
    news_list = get_related_news(main_topic, sub_topic)
    if news_list:
        for news in news_list:
            st.markdown(f"- [{translate(news['title'])}]({news['url']})")
    else:
        st.info(translate("관련 기사를 찾을 수 없습니다."))

    # 사용자 피드백
    st.markdown("---")
    st.info(translate("원하는 정보가 부족하다면 아래에 의견을 남겨주세요!"))
    feedback = st.text_area(translate("궁금한 점이나 요청하고 싶은 내용을 적어주세요"))
    if st.button(translate("제출")):
        st.success(translate("소중한 의견 감사합니다! 빠른 시일 내 반영하겠습니다."))
