import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="기분별 맞춤 음식 추천", page_icon="🍽️")

# 상태(Session State) 초기화: 버튼 클릭 후에도 데이터를 유지하기 위함
if "step" not in st.session_state:
  st.session_state.step = 1
if "status_msg" not in st.session_state:
  st.session_state.status_msg = ""
if "category" not in st.session_state:
  st.session_state.category = ""
if "recommended_food" not in st.session_state:
  st.session_state.recommended_food = ""

# 상황별 음식 데이터베이스
food_db = {
    "스트레스": {
        "상태": "스트레스를 많이 받은 상태입니다.",
        "설명": "엽떡, 불닭볶음면 등 매운 음식",
        "메뉴": ["엽기떡볶이", "불닭볶음면", "매운 갈비찜", "마라탕", "불족발"],
    },
    "우울": {
        "상태": "기분이 가라앉고 위로가 필요한 상태입니다.",
        "설명": "초콜릿, 케이크 등 달달한 디저트나 따뜻한 국물 음식",
        "메뉴": ["초코 케이크", "마카롱", "따뜻한 우동", "소고기 국밥", "팬케이크"],
    },
    "피곤": {
        "상태": "체력이 떨어지고 에너지가 부족한 상태입니다.",
        "설명": "삼겹살, 장어 등 든든한 보양식",
        "메뉴": ["삼겹살", "장어덮밥", "삼계탕", "소고기 스테이크", "돈가스"],
    },
    "행복": {
        "상태": "기분이 아주 좋고 신나는 상태입니다!",
        "설명": "치킨, 피자 등 파티 분위기가 나는 음식",
        "메뉴": ["후라이드 치킨", "페퍼로니 피자", "초밥", "파스타", "타코"],
    },
    "일반": {
        "상태": "평온하고 무난한 상태입니다.",
        "설명": "호불호 없이 맛있게 먹을 수 있는 대중적인 음식",
        "메뉴": ["김치찌개", "제육볶음", "비빔밥", "햄버거", "쌀국수"],
    },
}


# 입력된 문장에서 키워드를 찾아 상태를 분석하는 함수
def analyze_situation(text):
  if any(
      word in text
      for word in ["싸웠", "억울", "화나", "짜증", "열받", "스트레스", "답답"]
  ):
    return "스트레스"
  elif any(word in text for word in ["우울", "슬퍼", "눈물", "힘들", "외로", "지쳐"]):
    return "우울"
  elif any(word in text for word in ["피곤", "졸려", "기운", "배고파", "야근", "시험"]):
    return "피곤"
  elif any(word in text for word in ["행복", "신나", "기뻐", "좋아", "축하", "합격"]):
    return "행복"
  else:
    return "일반"


# --- UI 구성 시작 ---
st.title("🍽️ 상황 & 기분별 맞춤 음식 추천기")
st.write("지금 겪고 있는 상황이나 기분을 자유롭게 적어주세요!")

# [1단계] 사용자 상황 입력
situation_input = st.text_input(
    "현재 상황이나 기분을 입력하세요:",
    placeholder="예: 지금 엄마랑 싸워서 너무 억울하고 화가 나...",
)

if st.button("음식 추천받기", use_container_width=True):
  if situation_input.strip() == "":
    st.warning("상황이나 기분을 먼저 입력해주세요!")
  else:
    category = analyze_situation(situation_input)
    st.session_state.category = category
    st.session_state.status_msg = food_db[category]["상태"]
    st.session_state.recommended_food = random.choice(food_db[category]["메뉴"])
    st.session_state.step = 2  # 다음 단계(결과 및 알레르기 확인)로 이동

# [2단계] 상태 분석 결과 출력 및 알레르기 여부 확인
if st.session_state.step >= 2:
  st.divider()
  cat = st.session_state.category
  st.error(f"🩺 **상태 분석:** {st.session_state.status_msg}")
  st.info(
      f"💡 **추천 카테고리:** {food_db[cat]['설명']}\n\n👉 **오늘의 추천 메뉴:**"
      f" **{st.session_state.recommended_food}**"
  )

  st.write("---")
  st.subheader("🚨 잠깐! 혹시 추천된 음식에 알레르기가 있으신가요?")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("네, 알레르기가 있어요 (다른 음식 추천)", use_container_width=True):
      # 현재 추천된 음식을 제외한 나머지 메뉴 중에서 랜덤 선택
      available_menus = [
          m
          for m in food_db[cat]["메뉴"]
          if m != st.session_state.recommended_food
      ]
      st.session_state.recommended_food = random.choice(available_menus)
      st.session_state.step = 3

  with col2:
    if st.button("아니요, 없어요 (이걸로 결정!)", use_container_width=True):
      st.session_state.step = 4

# [3단계] 알레르기가 있어서 다른 음식을 추천받은 경우
if st.session_state.step == 3:
  st.success(
      f"🔄 알레르기를 피해 새로운 메뉴를 골랐어요! 최종 추천 음식은"
      f" **[{st.session_state.recommended_food}]** 입니다. 맛있게 드세요! 😋"
  )
  st.balloons()

# [4단계] 알레르기가 없어서 기존 음식을 확정한 경우
elif st.session_state.step == 4:
  st.success(
      f"🎉 좋습니다! 최종 추천 음식은 **[{st.session_state.recommended_food}]**"
      " 입니다. 기분 풀고 맛있게 드세요! 😋"
  )
  st.balloons()
