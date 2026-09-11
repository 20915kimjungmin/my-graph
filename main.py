import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 제목
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("1년치(365일) 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 변화를 탐색합니다.")

# -----------------------------------------------------------------------------
# 2. 데이터 로드 및 전처리
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 열 이름 확인 및 날짜 변환
    # 데이터셋 열: 날짜, 순위, 영화코드, 영화명, 일관객, 누적관객, 스크린수, 상영횟수
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 3. 데이터 요약 안내 (사이드바 또는 상단)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("📌 데이터 정보")
    st.write(f"- **총 데이터 수**: {len(df):,}개")
    st.write(f"- **기간**: {df['날짜'].min().strftime('%Y-%m-%d')} ~ {df['날짜'].max().strftime('%Y-%m-%d')}")
    st.write(f"- **등록된 영화 수**: {df['영화명'].nunique():,}개")

# -----------------------------------------------------------------------------
# 구역 1: 개별 영화 추이 (시간 흐름 분석)
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("SECTION 1. 영화별 일관객수 시간에 따른 변화")
st.write("원하는 영화를 선택하여 상영 기간 동안의 일별 관객 수 추이를 확인해보세요.")

# 영화 선택 드롭다운 (관객수가 많은 주요 영화 순으로 정렬)
movie_list = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

# 선택한 영화 데이터 필터링
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not movie_df.empty:
    # Plotly 선 그래프 생성
    fig = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"<b>[{selected_movie}]</b> 일별 관객 수 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
        markers=True,
        hover_data={'날짜': '|%Y-%m-%d', '일관객': ':,d', '순위': True}
    )

    # 그래프 스타일 조정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위<extra></extra>",
        line_color='#E50914',
        line_width=2.5
    )
    
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="날짜",
        yaxis_title="일일 관객 수(명)",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True, tickformat=","),
        margin=dict(l=40, r=40, t=60, b=40),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # 알 수 있는 것 안내 박스
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** 개봉 초기 관객 수 폭발력(피크 시점)과 주말/평일 간의 주기적인 관객 수 변동 추이를 한눈에 파악할 수 있습니다."
    )
else:
    st.warning("선택한 영화의 데이터가 없습니다.")

# -----------------------------------------------------------------------------
# 구역 2: 추후 그래프 추가용 예시 공간
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("SECTION 2. (추가 예정) 시간 관련 확장 분석")
st.caption("앞으로 더 다양한 시간 중심의 박스오피스 그래프가 이곳에 추가될 예정입니다.")

# 예시 자리 플레이스홀더
st.info("💡 **이 그래프로 알 수 있는 것:** (새로운 그래프 추가 후 알 수 있는 인사이트가 표시될 공간입니다.)")
)
fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객 수",
    hovermode="x unified"
)

st.plotly_chart(fig1, use_container_width=True)

st.info(f"💡 **이 그래프로 알 수 있는 것:** '{selected_movie}'의 흥행 전개 양상(개봉 초기 화제성, 주말 폭증 패턴, 흥행 유지 기간 및 꺾임 시점)을 직관적으로 파악할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 구역 2: 기간 내 관객수 상위 Top 5 영화의 일관객 추이 비교
# ---------------------------------------------------------
st.header("2. 관객 수 Top 5 영화의 일관객 비교")
st.write("해당 기간 동안 일관객 합계가 가장 큰 상위 5편 영화의 날짜별 관객 수 추이를 한눈에 비교합니다.")

# 1년 간 일관객 합계 상위 5개 영화 도출
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index.tolist()

# Top 5 영화 데이터 필터링
top5_df = df[df['영화명'].isin(top5_movies)].sort_values(['날짜', '영화명'])

# Plotly 다중 선 그래프 생성
fig2 = px.line(
    top5_df,
    x='날짜',
    y='일관객',
    color='영화명',
    title="기간 내 일관객 합계 Top 5 영화의 날짜별 관객 수 변화 비교",
    labels={'날짜': '날짜', '일관객': '일일 관객 수 (명)', '영화명': '영화 제목'},
    markers=False
)

fig2.update_traces(
    hovertemplate="<b>영화:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,.0f}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객 수",
    hovermode="x unified",
    legend_title_text="영화 (클릭하여 켜기/끄기)"
)

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 최고 흥행작 top 5 간의 상영 시기 중첩 여부 및 최고 피크 시 관객 수, 흥행 지속력을 한 번에 비교할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 구역 3: 추후 그래프 추가용 영역 (확장 구역)
# ---------------------------------------------------------
st.header("3. [추가 예정] 시간 관련 분석 구역")
st.write("앞으로 추가될 시계열/시간 관련 다양한 그래프가 들어갈 공간입니다.")

st.info("💡 **이 그래프로 알 수 있는 것:** (그래프 추가 후 알 수 있는 문구가 들어갈 자리입니다.)")
