import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="폭염과 온열질환 분석", layout="wide")
st.title("폭염일수 증가가 온여질환자 수에 미치는 영향")
st.markdown("""
### 텍스트 보고서
- 투자: 김정우, 주현욱, 송준하  
- 보고제목: 폭염의 증가가 온여질환자 수에 미치는 영햠를 분석하고 대응방안 제안
""")

# Load pre-processed data
@st.cache_data
def load_data():
    return pd.DataFrame({
        '연도': [2015, 2016, 2017, 2018, 2019],
        '폭염일수': [8, 24, 13, 35, 15],
        '온열환자수': [13434, 15322, 13583, 25047, 17509]
    })

df = load_data()

# 시각화 1: 연도별 추이
st.subheader(":bar_chart: 연도별 폭염일수 및 온열환자수")
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.plot(df['연도'], df['폭염일수'], 'r-o', label='폭염일수')
ax2.plot(df['연도'], df['온열환자수'], 'b-s', label='온열환자수')
ax1.set_xlabel('연도')
ax1.set_ylabel('폭염일수', color='red')
ax2.set_ylabel('온열환자수', color='blue')
fig.tight_layout()
st.pyplot(fig)

# 시각화 2: 산점도 + 회귀선
st.subheader(":chart_with_upwards_trend: 폭염일수와 온열환자수 상관 분석")
sns.set(style="whitegrid")
fig2, ax = plt.subplots(figsize=(7, 5))
sns.regplot(x='폭염일수', y='온열환자수', data=df, ax=ax, ci=None)
plt.xlabel("폭염일수")
plt.ylabel("온열환자수")
st.pyplot(fig2)

# 분석 결과
st.subheader(":mag: 회귀 분석 결과")
X = df[['폭염일수']]
y = df['온열환자수']
model = LinearRegression()
model.fit(X, y)
coef = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)

st.markdown(f"""
- **회귀식**: 온열환자수 = {coef:.2f} × 폭염일수 + {intercept:.2f}  
- **설명력 (R²)**: {r2:.4f}  
- 해석: 폭염일수가 하루 증가할 때 온열환자수가 평균적으로 **{coef:.0f}명** 증가합니다.
""")

# 제언
st.subheader(":bulb: 대응 방안 제안")
st.markdown("""
1. 폭염 예보 시 **예방 메시지 및 문자 발송 시스템 강화**
2. **고령자 대상 실내 냉방센터 운영 확대**
3. 폭염 취약지역 우선 모니터링 및 응급대응반 배치
""")