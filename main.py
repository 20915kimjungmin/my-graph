# 영화 데이터 그래프 도감 1 - 시간
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)
    # 여덟 자리 숫자로 된 날짜 열을 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

# ── 그래프 1. 영화 하나의 흥행 곡선 ──────────────────────────
st.header("1. 한 영화의 흥행 곡선")

# 드롭다운으로 영화를 고릅니다.
movie_list = sorted(df["영화명"].unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = df[df["영화명"] == movie].sort_values("날짜")
fig = px.line(one, x="날짜", y="일관객", markers=True)
fig.update_traces(hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra></extra>")
st.plotly_chart(fig, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 앞으로 그래프 2, 3, 4, 5가 이 아래에 추가됩니다 ──────────
# ── 그래프 2. 흥행 대작들의 곡선 겹쳐 보기 ────────────────────
st.header("2. 흥행 대작 다섯 편의 곡선")
top5 = df.groupby("영화명")["일관객"].sum().nlargest(5).index
five = df[df["영화명"].isin(top5)].sort_values("날짜")
fig2 = px.line(five, x="날짜", y="일관객", color="영화명", markers=True)
st.plotly_chart(fig2, width="stretch")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
# ── 그래프 3. 극장가 전체의 흐름과 봉우리 ─────────────────────
st.header("3. 날짜별 10위권 관객 합계")
daily = df.groupby("날짜", as_index=False)["일관객"].sum()
peak3 = daily.nlargest(3, "일관객")
fig3 = px.area(daily, x="날짜", y="일관객")
fig3.add_scatter(x=peak3["날짜"], y=peak3["일관객"], mode="markers+text",
                 text=peak3["날짜"].dt.strftime("%Y-%m-%d"), textposition="top center",
                 marker=dict(size=10, color="crimson"), name="가장 붐빈 3일")
st.plotly_chart(fig3, width="stretch")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
# ── 그래프 4. 기간 전체 관객 TOP 10 ─────────────────────────
st.header("4. 이 기간 관객이 가장 많았던 열 편")
total = (df.groupby("영화명", as_index=False)
           .agg(관객합계=("일관객", "sum"), 등장일수=("날짜", "count"))
           .nlargest(10, "관객합계"))
fig4 = px.bar(total.sort_values("관객합계"), x="관객합계", y="영화명",
              orientation="h", hover_data=["등장일수"])
st.plotly_chart(fig4, width="stretch")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
