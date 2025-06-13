import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 정의
data = {
    '연도': [2020, 2021, 2022, 2023, 2024, 2025],
    '1인당_GDP': [31728, 35003, 33591, 33147, 34200, 35500],
    'CPI': [0.5, 2.5, 5.09, 3.8, 2.3, 2.1],
    '소비율': [48.7, 51.3, 54.1, 54.4, 55.0, 55.5]
}
df = pd.DataFrame(data)

st.title("📊 경제 지표 시각화 (2020–2025)")

show_all = st.checkbox("🔄 3개 그래프를 하나로 통합해서 보기")

if not show_all:
    st.markdown("### 📌 개별 그래프 보기 (나란히)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🔵 1인당 GDP**")
        st.line_chart(df.set_index('연도')['1인당_GDP'])

    with col2:
        st.markdown("**🔴 CPI 상승률**")
        st.line_chart(df.set_index('연도')['CPI'])

    with col3:
        st.markdown("**🟢 소비율**")
        st.line_chart(df.set_index('연도')['소비율'])

else:
    st.markdown("### 📊 통합 비교 그래프")
    fig, ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(df['연도'], df['1인당_GDP'], 'o-', color='blue', label='1인당 GDP (USD)')
    ax1.set_ylabel('1인당 GDP (USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(df['연도'], df['CPI'], 's--', color='red', label='CPI 상승률 (%)')
    ax2.set_ylabel('CPI 상승률 (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax3 = ax1.twinx()
    ax3.spines.right.set_position(("outward", 60))
    ax3.plot(df['연도'], df['소비율'], 'd-.', color='green', label='소비율 (%)')
    ax3.set_ylabel('소비율 (%)', color='green')
    ax3.tick_params(axis='y', labelcolor='green')

    lines = ax1.get_lines() + ax2.get_lines() + ax3.get_lines()
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper left')

    st.pyplot(fig)
