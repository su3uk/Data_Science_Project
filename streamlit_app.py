import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib
import io
from PIL import Image

map_img = Image.open("./고령인구지도.png")
bar_img = Image.open("./연령대별온열질환자.png")

# 한글 폰트 설정 (NanumGothic.ttf 포함 직접 지정)
font_path = './NanumGothic.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="폭염 분석 대시보드", layout="wide")

# ------------------------------
# 파이어 데이터 로드
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

# 고령 인구 비율 수동 입력
senior_ratio = {
    "강원도": 25.4,
    "경상북도": 26.0,
    "전라남도": 27.2
}

@st.cache_data
def load_patient_data():
    df = pd.read_excel("./연도별 온열환자 수.xlsx", sheet_name='Sheet1', header=1)
    df = df.rename(columns={"시·도명": "시도"})
    df = df[df["시도"].isin(["강원도", "경상북도", "전라남도"])].copy()
    year_cols = [col for col in df.columns if isinstance(col, int)]
    df["평균 온열환자 수"] = df[year_cols].mean(axis=1).astype(int)
    df["고령 인구 비율"] = df["시도"].map(senior_ratio)
    return df

df_region = load_patient_data()

fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.bar(df_region["시도"], df_region["평균 온열환자 수"], color='salmon', label="평균 온열환자 수")
ax1.set_ylabel("평균 온열환자 수", fontsize=11, fontproperties=font_prop)
ax1.set_xticklabels(df_region["시도"], fontproperties=font_prop)
ax2 = ax1.twinx()
ax2.plot(df_region["시도"], df_region["고령 인구 비율"], color='darkblue', marker='o', label="고령 인구 비율 (%)")
ax2.set_ylabel("고령 인구 비율 (%)", fontsize=11, fontproperties=font_prop)
fig.suptitle("지역별 평균 온열환자 수 vs 고령 인구 비율", fontsize=14, fontproperties=font_prop)
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95), prop=font_prop)
plt.tight_layout()

img_buffer = io.BytesIO()
fig.savefig(img_buffer, format='png')
img_buffer.seek(0)

# ------------------------------
# 파이스트 메뉴
# ------------------------------
st.sidebar.title("☀️ Heat Dashboard")
st.sidebar.markdown("**User:** 김정운, 주현욱, 송준하")
st.sidebar.markdown("Version: `1.0.0`")
st.sidebar.markdown("---")

st.markdown("""
<style>
[data-testid=\"stSidebar\"] .stRadio > div {
    display: flex;
    flex-direction: column;
    row-gap: 0.75rem;
}
[data-testid=\"stSidebar\"] .stRadio > div > label {
    background-color: #f0f2f6;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    border: 1px solid #d0d4dc;
    transition: 0.3s;
    cursor: pointer;
}
[data-testid=\"stSidebar\"] .stRadio > div > label:hover {
    background-color: #e4e8f0;
}
[data-testid=\"stSidebar\"] .stRadio > div > label[data-selected=\"true\"] {
    background-color: #1f77b4;
    color: white;
    font-weight: 600;
    border: 1px solid #1f77b4;
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
# 메뉴 기반 동작
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

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🗺️ 지역별 고령 인구 비율")
        st.image(map_img, caption="전국 시도별 고령 인구 비율 (2024)", use_column_width=True)

    with col2:
        st.markdown("### 📊 연령대별 온열질환자 수")
        st.image(bar_img, caption="연령별 온열질환자 수 및 인구 10만명당 환자수", use_column_width=True)

    st.markdown("### 🔍 고령 인구 비율 vs 온열환자 수 분석")
    st.image(img_buffer, caption="고령 인구 비율과 온열환자 수의 상관 관계", use_column_width=True)

    st.markdown("""
    ### 📌 종합 분석

    - **고령 인구 비율 상위 3개 지역**:
        - 전라남도 (27.2%)
        - 경상북도 (26.0%)
        - 강원도 (25.4%)

    - 이들 지역은 **온열질환자 수 평균 상위 지역**과도 정확히 일치함  
      → **지역 고령 인구 비율이 온열질환자 수와 밀접한 상관관계를 가짐**

    - 또한, **연령대별 통계**에서도 **고령층(특히 70세 이상)** 에서 인구 대비 환자수가 급증함  
      → **폭염 시 고령층이 주요 취약계층**임을 다시 한번 시사

    ### ✅ 정책 제안

    | 항목 | 내용 |
    |------|------|
    | 🧓 고령층 보호 | 무더위 쉼터 설치 확대 및 고령층 대상 안내 문자 발송 강화 |
    | 🏥 응급 대응 | 고온 경보 시 119 연계 및 마을별 응급의료체계 점검 |
    | 📊 데이터 기반 | 고령 인구-기온-질환자 수 기반 대응 시뮬레이션 및 사전 대응 |
    | 📣 홍보 | 마을 방송, 전단, 버스·지하철 홍보 통해 행동 요령 지속 교육 |

    > 🌡️ **폭염 대응의 핵심은 고령자 보호입니다!**
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
    ax.set_ylabel("온열질환수", fontproperties=font_prop)
    st.pyplot(fig)

    st.markdown("## 💡 온열질환 예방 대응 방안")
    with st.container():
        st.markdown("### 📊 고령 인구 비율과 온열환자 수 비교")
        st.image(img_buffer, caption="고령 인구 비율과 온열환자 수의 상관 관계")

        st.markdown("""
        ### 🔍 분석 결과

        - 전국 17개 시도 중 **고령 인구 비율이 가장 높은 지역**은 다음과 같습니다:
            - **전라남도** (27.2%)
            - **경상북도** (26.0%)
            - **강원도** (25.4%)

        - 해당 지역들은 동시에 **평균 온열질환자 수 상위 3개 지역**과도 일치합니다.

        📌 **결론**:
        > 고령 인구 비율이 높은 지역에서 온열질환자 수 또한 높은 경향이 있음을 확인할 수 있었습니다.
        >
        > 이는 곧 **고령층(취약계층)** 이 폭염에 더 취약하다는 점을 시사하며, **무더위 쉼터 설치 및 운영 강화** 등 예방 대책이 절실하다는 결론을 도출할 수 있습니다.
        """)