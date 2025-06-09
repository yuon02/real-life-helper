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
 
