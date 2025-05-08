def get_topic_data(topic):
    sample_data = {
        "아르바이트": {
            "최저임금": {
                "내용": "2025년 기준 최저임금은 시급 10,000원입니다.",
                "출처": "https://www.moel.go.kr"
            },
            "계약서 작성": {
                "내용": "근로계약서는 서면으로 작성해야 하며 사본을 받아야 합니다.",
                "출처": "https://www.moel.go.kr"
            }
        },
        "금융": {
            "통장 개설": {
                "내용": "신분증만 있으면 은행에서 통장 개설이 가능합니다.",
                "출처": "https://www.fss.or.kr"
            },
            "청년 지원금": {
                "내용": "청년내일저축계좌, 청년희망적금 등의 제도가 있습니다.",
                "출처": "https://www.gov.kr"
            }
        }
    }
    return sample_data.get(topic, {})

def get_related_news(topic, sub_topic):
    return [
        {"title": f"{topic} 관련 최신 뉴스 1", "url": "https://news.example.com/1"},
        {"title": f"{topic} 관련 최신 뉴스 2", "url": "https://news.example.com/2"},
    ]
