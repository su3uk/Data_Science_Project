import streamlit as st
import pandas as pd

# 데이터 정의
data = {
    '연도': [2020, 2021, 2022, 2023, 2024, 2025],
    '1인당_GDP': [31728, 35003, 33591, 33147, 34200, 35500],
    'CPI': [0.5, 2.5, 5.09, 3.8, 2.3, 2.1],
    '소비율': [48.7, 51.3, 54.1, 54.4, 55.0, 55.5]
}
df = pd.DataFrame(data)

# wide 모드 설정
st.set_page_config(page_title="경제 지표 시각화", layout="wide")
st.title("📊 경제 지표 시각화 (2020–2025)")

# 상태 변수 (버튼 누르면 상태 변경)
if "show_combined" not in st.session_state:
    st.session_state.show_combined = False

# 버튼 위치를 중앙에 배치하기 위한 3등분 레이아웃
btn_col1, btn_col2, btn_col3 = st.columns([4, 2, 4])
with btn_col2:
    if st.button("📊 세 그래프 통합해서 보기"):
        st.session_state.show_combined = not st.session_state.show_combined

# 📌 그래프 영역
st.markdown("---")

if not st.session_state.show_combined:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔵 1인당 GDP")
        st.line_chart(df.set_index('연도')['1인당_GDP'], use_container_width=True)

    with col2:
        st.markdown("### 🔴 CPI 상승률")
        st.line_chart(df.set_index('연도')['CPI'], use_container_width=True)

    with col3:
        st.markdown("### 🟢 소비율")
        st.line_chart(df.set_index('연도')['소비율'], use_container_width=True)
else:
    st.markdown("### 📊 통합 비교 그래프")
    st.line_chart(
        df.set_index('연도')[['1인당_GDP', 'CPI', '소비율']],
        use_container_width=True
    )
