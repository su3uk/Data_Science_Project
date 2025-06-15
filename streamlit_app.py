import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib

# 한글 폰트 설정 (NanumGothic.ttf 포함 직접 지정)
font_path = './NanumGothic.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="폭염 분석 대시보드", layout="wide")

# ------------------------------
# 📌 사이드바
# ------------------------------
st.sidebar.title("☀️ Heat Dashboard")
st.sidebar.markdown("**User:** 김정운, 주현욱, 송준하")
st.sidebar.markdown("Version: `1.0.0`")
st.sidebar.markdown("---")

# ✅ 스타일: 사이드바 메뉴 간격 넓히기
st.markdown(
    """
    <style>
        div[data-baseweb=\"radio\"] > div {
            row-gap: 0.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("""
<style>
    section[data-testid="stSidebar"] .st-radio > div {
        gap: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "📂 메뉴",
    [
        "폭염과 온열질환 분석 대시보드",
        "폭염과 온열질환의 상관 관계",
        "온열질환 예방 대응 방안",
        "전체 보기"
    ],
    index=0,
    key="menu"
)

# ------------------------------
# 📊 데이터 로딩
# ------------------------------
@st.cache_data
def load_data():
    return pd.DataFrame({
        '연도': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        '폭염일수': [8, 24, 13, 35, 15, 2, 5, 8, 11, 10],
        '온열환자수': [13434, 15322, 13583, 25047, 17509, 11333, 10919, 13713, 15543, 17356]
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
if menu == "폭염과 온열질환 분석 대시보드":
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

elif menu == "폭염과 온열질환의 상관 관계":
    st.markdown("## 🔍 폭염과 온열질환의 상관 관계")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.regplot(x='폭염일수', y='온열환자수', data=df, ax=ax, ci=None, scatter_kws={"s": 70})
    ax.set_xlabel("폭염일수", fontproperties=font_prop)
    ax.set_ylabel("온열환자수", fontproperties=font_prop)
    st.pyplot(fig)
    st.dataframe(df)

elif menu == "온열질환 예방 대응 방안":
    st.markdown("## 💡 온열질환 예방 대응 방안")
    with st.container():
        st.markdown("""
        ### ✅ 주요 대응 전략

        | 구분 | 내용 |
        |------|------|
        | 🔔 **경보 시스템** | 폭염 특보 시 대국민 긴급 문자 자동 발송 시스템 구축 |
        | 🧓 **취약계층 보호** | 독거노인, 노숙인 등 폭염 취약계층 대상 냉방쉼터 운영 및 이동형 쉼터 배치 |
        | 🚑 **응급 대응** | 온열질환자 다발 지역에 응급의료팀 상시 대기 및 119 출동 강화 |
        | 📊 **데이터 기반 예측** | 과거 폭염일수-환자수 데이터 기반 선제 대응 정책 수립 |
        | 🏫 **교육 및 홍보** | 학교·직장 대상 폭염 행동 요령 캠페인 시행 및 대국민 매뉴얼 보급 |

        ---
        🔄 **지속적인 모니터링과 지역 맞춤형 정책이 핵심입니다!**
        """)
    

elif menu == "전체 보기":
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
    ax.set_xlabel("폭염일수", fontproperties=font_prop)
    ax.set_ylabel("온열환자수", fontproperties=font_prop)
    st.pyplot(fig)

    st.markdown("## 💡 온열질환 예방 대응 방안")
    with st.container():
        st.markdown("""
        ### ✅ 주요 대응 전략

        | 구분 | 내용 |
        |------|------|
        | 🔔 **경보 시스템** | 폭염 특보 시 대국민 긴급 문자 자동 발송 시스템 구축 |
        | 🧓 **취약계층 보호** | 독거노인, 노숙인 등 폭염 취약계층 대상 냉방쉼터 운영 및 이동형 쉼터 배치 |
        | 🚑 **응급 대응** | 온열질환자 다발 지역에 응급의료팀 상시 대기 및 119 출동 강화 |
        | 📊 **데이터 기반 예측** | 과거 폭염일수-환자수 데이터 기반 선제 대응 정책 수립 |
        | 🏫 **교육 및 홍보** | 학교·직장 대상 폭염 행동 요령 캠페인 시행 및 대국민 매뉴얼 보급 |

        ---
        🔄 **지속적인 모니터링과 지역 맞춤형 정책이 핵심입니다!**
        """)