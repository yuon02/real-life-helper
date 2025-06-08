import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 페이지 설정
st.set_page_config(page_title="실생활 정보 도우미", layout="wide")

# 기본 정보
st.title("🧭 실생활 정보 도우미")
st.markdown("대학생 및 사회초년생을 위한 분야별 실용 정보, 뉴스, 계약서 양식, 영상, 다국어 번역 제공")

# 분야 리스트
topics = ["부동산", "아르바이트", "금융", "세금", "계약"]

# 사용자 선택
selected_topic = st.selectbox("관심 있는 주제를 선택하세요", topics)

# 각 분야별 기본 설명 및 처리
topic_info = {
    "부동산": "부동산 임대차, 전세계약, 중개 관련 정보를 제공합니다.",
    "아르바이트": "근로계약서, 시급, 주휴수당 관련 정보를 확인하세요.",
    "금융": "은행 계좌, 카드, 대출 관련 기초 지식을 제공합니다.",
    "세금": "소득세, 주민세, 연말정산 등에 대한 정보를 안내합니다.",
    "계약": "일상 생활에서 필요한 계약의 기초 개념과 양식을 제공합니다.",
}

st.subheader(f"📌 {selected_topic} 정보")
st.markdown(topic_info[selected_topic])

# ✅ 뉴스 가져오기 기능 (분야별로 다르게 표시)
def get_news(topic):
    try:
        query = f"{topic} 실생활"
        url = f"https://search.naver.com/search.naver?where=news&query={query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = soup.select("a.news_tit")
        news_list = []

        for item in news_items[:5]:
            title = item.get("title")
            link = item.get("href")
            news_list.append((title, link))
        return news_list
    except Exception as e:
        return [("뉴스를 가져오는 중 오류 발생", "#")]

st.markdown("### 📰 관련 뉴스")
news_data = get_news(selected_topic)
for title, link in news_data:
    st.markdown(f"- [{title}]({link})")

# ✅ 계약서 양식 다운로드 기능
def get_contract_forms(topic):
    form_list = {
        "부동산": {
            "주택 임대차 계약서": "https://www.scourt.go.kr/portal/information/form/viewFormFile.do?formFileId=2bfe4b59-dfae-4f8b-9c2a-5793d22b1bd2",
            "상가 임대차 계약서": "https://www.scourt.go.kr/portal/information/form/viewFormFile.do?formFileId=ae3839cb-1406-4ac5-8788-94bb168a5e4f"
        },
        "아르바이트": {
            "근로 계약서": "https://www.moel.go.kr/policy/policyinfo/etcEmp/download/parttime_contract.hwp"
        },
        "금융": {},
        "세금": {},
        "계약": {
            "물품 공급 계약서": "https://www.scourt.go.kr/portal/information/form/viewFormFile.do?formFileId=fedc1dc9-e181-4f7b-b646-74c6c4e1ab26"
        }
    }
    return form_list.get(topic, {})

st.markdown("### 📄 계약서 양식")
forms = get_contract_forms(selected_topic)

if forms:
    for name, link in forms.items():
        st.download_button(
            label=f"{name} 다운로드",
            data=requests.get(link).content,
            file_name=f"{name}.hwp",
            mime="application/haansofthwp"
        )
else:
    st.info("이 주제에 관련된 계약서 양식이 없습니다.")

# ✅ 유튜브 영상 예시 출력
video_links = {
    "부동산": "https://www.youtube.com/watch?v=ecqgFeKkUhU",
    "아르바이트": "https://www.youtube.com/watch?v=PN3oJpfn0lI",
    "금융": "https://www.youtube.com/watch?v=tBvSsPqkzLg",
    "세금": "https://www.youtube.com/watch?v=ZQTDzj7L7xM",
    "계약": "https://www.youtube.com/watch?v=d_P4GGb0K2Y"
}
st.markdown("### 🎥 관련 유튜브 영상")
st.video(video_links.get(selected_topic, ""))

# ✅ 다국어 번역 기능
st.markdown("### 🌐 주요 문장 번역")
default_text = "안녕하세요. 계약서를 작성할 때는 내용을 꼼꼼히 읽어야 합니다."
text_to_translate = st.text_input("번역할 문장을 입력하세요", default_text)

if text_to_translate:
    from googletrans import Translator
    translator = Translator()
    result = translator.translate(text_to_translate, dest='en')
    st.markdown(f"**영어 번역:** {result.text}")

# ✅ 사용자 의견
st.markdown("### ✍️ 의견 보내기")
feedback = st.text_area("이 앱에 대한 개선 사항이나 의견이 있다면 작성해 주세요.")
if st.button("의견 제출"):
    st.success("의견이 제출되었습니다. 감사합니다!")

