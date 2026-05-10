import streamlit as st
import plotly.graph_objects as go


st.set_page_config(page_title="상자그림 시각화", page_icon="📦", layout="wide")

st.title("📦 상자그림(Box Plot) 시각화 앱")

st.markdown(
    """
이 앱은 상자그림의 핵심 개념을 빠르게 이해하고,
예시 데이터로 **가로/세로 상자그림**을 비교해 볼 수 있도록 구성되었습니다.

### 상자그림 기본 개념
- **최솟값(Minimum)**: 데이터 중 가장 작은 값
- **Q1(제1사분위수)**: 하위 25% 지점에 해당하는 값
- **중앙값(Median)**: 데이터의 가운데 값
- **Q3(제3사분위수)**: 하위 75% 지점에 해당하는 값
- **최댓값(Maximum)**: 데이터 중 가장 큰 값
- **상자(Box)**: Q1부터 Q3까지의 구간으로, 가운데 50%의 데이터가 포함됨
- **수염(Whisker)**: 상자 밖으로 최솟값과 최댓값까지 이어지는 선
"""
)


sample_data = {
    "퀴즈 점수": [50, 55, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 81, 86],
    "공부 시간": [45, 48, 50, 52, 53, 55, 56, 58, 60, 63, 67, 72, 80, 90, 105],
    "다른 반의 퀴즈 점수": [30, 40, 48, 55, 60, 64, 66, 68, 70, 72, 76, 81, 88, 96, 100],
}

with st.sidebar:
    st.header("설정")
    selected_dataset_name = st.selectbox(
        "예시 데이터를 선택하세요",
        list(sample_data.keys()),
    )
    orientation = st.radio(
        "상자그림 방향",
        options=["세로", "가로"],
        horizontal=True,
    )


selected_values = sample_data[selected_dataset_name]

if orientation == "세로":
    trace = go.Box(
        y=selected_values,
        name=selected_dataset_name,
    )
    x_title = "데이터 항목"
    y_title = "값"
else:
    trace = go.Box(
        x=selected_values,
        name=selected_dataset_name,
        orientation="h",
    )
    x_title = "값"
    y_title = "데이터 항목"


fig = go.Figure(data=[trace])
fig.update_layout(
    title=f"{selected_dataset_name} - {orientation} 상자그림",
    xaxis_title=x_title,
    yaxis_title=y_title,
    xaxis=dict(rangemode="tozero"),
    yaxis=dict(rangemode="tozero"),
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("선택한 데이터 미리보기")
st.write(selected_values)
