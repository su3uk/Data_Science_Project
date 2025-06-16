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

# 데이터 입력
연령대 = ['0~9', '10~19', '20~29', '30~39', '40~49', '50~59', '60~69', '70~79', '80']
환자수 = [12, 103, 372, 478, 538, 716, 678, 434, 373]
인구10만명당 = [0.4, 2.2, 6.2, 7.8, 6.9, 9.2, 8.7, 10.9, 15.4]

# 그래프 그리기
fig_age, ax1 = plt.subplots(figsize=(8, 5))
bar = ax1.bar(연령대, 환자수, color='gray', label='온열질환자 수')
ax1.set_ylabel('온열질환자 수 (명)', fontproperties=font_prop)
ax1.set_xlabel('연령대', fontproperties=font_prop)
ax1.tick_params(axis='y')

# 이중축
ax2 = ax1.twinx()
line = ax2.plot(연령대, 인구10만명당, color='red', marker='o', label='인구 10만명당 환자 수')
ax2.set_ylabel('인구 10만명당 환자 수', color='red', fontproperties=font_prop)
ax2.tick_params(axis='y', labelcolor='red')

# 타이틀 및 스타일
fig_age.suptitle("연령대별 온열질환자 수 및 인구 10만명당 환자 수", fontsize=14, fontproperties=font_prop)
fig_age.tight_layout()

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

    # 지도 + 연령대 그래프 나란히 표시
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🗺️ 지역별 고령 인구 비율")
        st.image(map_img, caption="2024년 전국 고령 인구 비율", use_container_width=True)
    with col2:
        st.markdown("#### 📊 연령대별 온열질환자 수")
        st.pyplot(fig_age)

    st.markdown("#### 📈 고령 인구 비율 vs 온열환자 수")
    st.image(img_buffer, caption="고령 인구 비율과 온열환자 수의 상관 관계", use_container_width=True)

    # 결론 및 정책 요약
    st.markdown("""
    <br>
    <div style='font-size:17px; line-height:1.6'>
    🔍 <b>결론 요약</b><br>
    - 고령 인구 비율이 높은 지역일수록 온열질환자 수가 많습니다.<br>
    - 연령대별 통계에서도 70대 이상 고령층이 특히 위험합니다.<br>
    - 폭염 대응 정책의 핵심은 <b style='color:#e74c3c'>고령층 보호</b>입니다.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""---""")
    st.markdown("#### ✅ 정책 제안")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 🧓 **고령층 보호**  
          무더위 쉼터 확대, 고령자 대상 문자 발송 강화
          
        - 📊 **데이터 기반 대응**  
          고령 인구·기온·환자 데이터를 활용한 예측 시스템 구축
        """)
    with col2:
        st.markdown("""
        - 🏥 **응급 대응 체계**  
          폭염 시 119 연결 강화, 마을 단위 응급점검

        - 📣 **홍보 및 교육**  
          마을 방송·전단지·대중교통 캠페인 활용
        """)

    st.markdown("""---""")
    st.success("🌡️ 고령자 중심의 폭염 대응이 국민 건강을 지키는 열쇠입니다.")


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

    # 지도 + 연령대 그래프 나란히 표시
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🗺️ 지역별 고령 인구 비율")
        st.image(map_img, caption="2024년 전국 고령 인구 비율", use_container_width=True)
    with col2:
        st.markdown("#### 📊 연령대별 온열질환자 수")
        st.pyplot(fig_age)

    st.markdown("#### 📈 고령 인구 비율 vs 온열환자 수")
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.image(img_buffer, caption="고령 인구 비율과 온열환자 수의 상관 관계")

    # 결론 및 정책 요약
    st.markdown("""
    <br>
    <div style='font-size:17px; line-height:1.6'>
    🔍 <b>결론 요약</b><br>
    - 고령 인구 비율이 높은 지역일수록 온열질환자 수가 많습니다.<br>
    - 연령대별 통계에서도 70대 이상 고령층이 특히 위험합니다.<br>
    - 폭염 대응 정책의 핵심은 <b style='color:#e74c3c'>고령층 보호</b>입니다.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""---""")
    st.markdown("#### ✅ 정책 제안")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 🧓 **고령층 보호**  
          무더위 쉼터 확대, 고령자 대상 문자 발송 강화
          
        - 📊 **데이터 기반 대응**  
          고령 인구·기온·환자 데이터를 활용한 예측 시스템 구축
        """)
    with col2:
        st.markdown("""
        - 🏥 **응급 대응 체계**  
          폭염 시 119 연결 강화, 마을 단위 응급점검

        - 📣 **홍보 및 교육**  
          마을 방송·전단지·대중교통 캠페인 활용
        """)

    st.markdown("""---""")
    st.success("🌡️ 고령자 중심의 폭염 대응이 국민 건강을 지키는 열쇠입니다.")