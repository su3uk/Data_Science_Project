import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib

# 한글 폰트 설정 (한글 깨짐 방지)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="폭염 분석 대시보드", layout="wide")

# ------------------------------
# 📌 사이드바
# ------------------------------
st.sidebar.title("☀️ Heat Dashboard")
st.sidebar.markdown("**User:** 주현욱")
st.sidebar.markdown("Version: `1.0.0`")
st.sidebar.markdown("---")
menu = st.sidebar.radio("📂 메뉴", ["Dashboard", "Data View", "Model Analysis", "Settings"])

# ------------------------------
# 📊 데이터 로딩
# ------------------------------
@st.cache_data
def load_data():
    return pd.DataFrame({
        '연도': [2015, 2016, 2017, 2018, 2019],
        '폭염일수': [8, 24, 13, 35, 15],
        '온열환자수': [13434, 15322, 13583, 25047, 17509]
    })

df = load_data()
X = df[['폭염일수']]
y = df['온열환자수']
model = LinearRegression()
model.fit(X, y)
coef = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)

# ------------------------------
# 🎯 메뉴 기반 동작 분기
# ------------------------------
if menu == "Dashboard":
    st.title("📊 폭염과 온열질환 분석 대시보드")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📆 평균 폭염일수", value=f"{df['폭염일수'].mean():.1f}일", delta="+3.2일")
    with col2:
        st.metric(label="🧑 온열질환자 평균", value=f"{df['온열환자수'].mean():,.0f}명", delta="+2.4%")
    with col3:
        st.metric(label="📊 상관계수 (R²)", value=f"{r2:.2f}", delta="양의 상관")
    with col4:
        st.metric(label="📈 증가량 예측", value=f"+{coef:.0f}명/일", delta=f"y = {coef:.0f}x + {intercept:.0f}")

    st.markdown("## 📈 연도별 추이 분석")
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### 🔥 폭염일수 변화")
        st.line_chart(df.set_index("연도")[['폭염일수']])
    with col6:
        st.markdown("### 🌡️ 온열질환자 수 변화")
        st.line_chart(df.set_index("연도")[['온열환자수']])

    st.markdown("## 🔍 폭염과 온열질환의 상관 관계")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.regplot(x='폭염일수', y='온열환자수', data=df, ax=ax, ci=None, scatter_kws={"s": 70})
    ax.set_xlabel("폭염일수")
    ax.set_ylabel("온열환자수")
    st.pyplot(fig)

    st.markdown("## 💡 온열질환 예방 대응 방안")
    st.markdown("""
    - 🔔 **폭염 특보 문자 자동 발송 시스템 도입**  
    - 🧓 **폭염 취약계층 대상 냉방쉼터 운영 확대**  
    - 🚑 **지역 기반 실시간 응급의료 모니터링 체계 구축**  
    """)

elif menu == "Data View":
    st.title("📄 데이터 테이블 보기")
    st.dataframe(df)

elif menu == "Model Analysis":
    st.title("📈 회귀 모델 상세 분석")
    st.markdown(f"**회귀식:** y = {coef:.2f}x + {intercept:.2f}")
    st.markdown(f"**설명력 (R²):** {r2:.4f}")
    st.line_chart(df.set_index("연도"))

elif menu == "Settings":
    st.title("⚙️ 설정")
    st.info("현재는 설정 가능한 항목이 없습니다. 추후 업데이트 예정입니다.")
