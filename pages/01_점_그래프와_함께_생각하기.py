import streamlit as st
import plotly.graph_objects as go
from statistics import median
from collections import Counter


st.set_page_config(page_title="점그래프와 상자그림 비교", page_icon="🔵", layout="wide")

st.title("🔵 점그래프와 상자그림 비교")

st.markdown(
    """
이 페이지에서는 같은 데이터를 **점그래프**와 **기본형 상자그림**으로 나란히 비교합니다.

- **점그래프**: 개별 데이터 값을 직접 보여줍니다.
- **기본형 상자그림**: 최솟값, Q1, 중앙값, Q3, 최댓값으로 데이터를 요약해 보여줍니다.

> 이 페이지의 상자그림은 이상치를 따로 표시하지 않는 **기본형 상자그림**입니다.  
> 따라서 수염의 끝은 각각 **최솟값**과 **최댓값**을 의미합니다.
"""
)


sample_data = {
    "퀴즈 점수": [50, 55, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 81, 86],
    "공부 시간": [45, 48, 50, 52, 53, 55, 56, 58, 60, 63, 67, 72, 80, 90, 105],
    "다른 반의 퀴즈 점수": [30, 40, 48, 55, 60, 64, 66, 68, 70, 72, 76, 81, 88, 96, 100],
}


def five_number_summary(values):
    """중학교 수준 설명에 맞게 중앙값을 제외하고 아래쪽/위쪽 절반의 중앙값을 Q1, Q3로 계산"""
    sorted_values = sorted(values)
    n = len(sorted_values)

    q2 = median(sorted_values)

    if n % 2 == 1:
        lower_half = sorted_values[: n // 2]
        upper_half = sorted_values[n // 2 + 1 :]
    else:
        lower_half = sorted_values[: n // 2]
        upper_half = sorted_values[n // 2 :]

    q1 = median(lower_half)
    q3 = median(upper_half)

    return {
        "최솟값": min(sorted_values),
        "Q1": q1,
        "중앙값": q2,
        "Q3": q3,
        "최댓값": max(sorted_values),
    }


def make_dot_plot(values, title, orientation):
    """점그래프: 같은 값이 반복될 경우 선택한 방향으로 쌓아서 표시"""
    counts = Counter(values)

    x_values = []
    y_values = []

    if orientation == "가로":
        for value in sorted(counts):
            for i in range(counts[value]):
                x_values.append(value)
                y_values.append(i + 1)
        x_title = "값"
        y_title = "빈도"
    else:
        for value in sorted(counts):
            for i in range(counts[value]):
                x_values.append(i + 1)
                y_values.append(value)
        x_title = "빈도"
        y_title = "값"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="markers",
            marker=dict(size=12),
            text=[f"값: {x}" for x in x_values],
            hoverinfo="text",
            name="데이터",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template="plotly_white",
        showlegend=False,
        height=430,
    )

    if orientation == "가로":
        fig.update_yaxes(
            tickmode="linear",
            dtick=1,
            range=[0, max(y_values) + 1],
        )
        fig.update_xaxes(rangemode="tozero")
    else:
        fig.update_xaxes(
            tickmode="linear",
            dtick=1,
            range=[0, max(x_values) + 1],
        )
        fig.update_yaxes(rangemode="tozero")

    return fig


def make_basic_box_plot(values, title, orientation):
    """기본형 상자그림: 수염을 최솟값과 최댓값까지 직접 그림"""
    summary = five_number_summary(values)

    min_v = summary["최솟값"]
    q1 = summary["Q1"]
    q2 = summary["중앙값"]
    q3 = summary["Q3"]
    max_v = summary["최댓값"]

    fig = go.Figure()

    if orientation == "가로":
        y_center = 0
        box_height = 0.5
        cap_height = 0.25

        # 왼쪽 수염: 최솟값 ~ Q1
        fig.add_trace(
            go.Scatter(
                x=[min_v, q1],
                y=[y_center, y_center],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 오른쪽 수염: Q3 ~ 최댓값
        fig.add_trace(
            go.Scatter(
                x=[q3, max_v],
                y=[y_center, y_center],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 최솟값 캡
        fig.add_trace(
            go.Scatter(
                x=[min_v, min_v],
                y=[y_center - cap_height, y_center + cap_height],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 최댓값 캡
        fig.add_trace(
            go.Scatter(
                x=[max_v, max_v],
                y=[y_center - cap_height, y_center + cap_height],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 상자 Q1 ~ Q3
        fig.add_shape(
            type="rect",
            x0=q1,
            x1=q3,
            y0=y_center - box_height / 2,
            y1=y_center + box_height / 2,
            line=dict(width=3),
            fillcolor="rgba(0,0,0,0)",
        )

        # 중앙값 선
        fig.add_trace(
            go.Scatter(
                x=[q2, q2],
                y=[y_center - box_height / 2, y_center + box_height / 2],
                mode="lines",
                line=dict(width=4),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 각 요소 라벨용 점
        fig.add_trace(
            go.Scatter(
                x=[min_v, q1, q2, q3, max_v],
                y=[y_center + 0.45] * 5,
                mode="markers+text",
                text=["최솟값", "Q1", "중앙값", "Q3", "최댓값"],
                textposition="top center",
                marker=dict(size=8),
                hovertext=[
                    f"최솟값: {min_v}",
                    f"Q1: {q1}",
                    f"중앙값: {q2}",
                    f"Q3: {q3}",
                    f"최댓값: {max_v}",
                ],
                hoverinfo="text",
                showlegend=False,
            )
        )

        fig.update_layout(
            title=title,
            xaxis_title="값",
            yaxis=dict(
                showticklabels=False,
                zeroline=False,
                range=[-1, 1.2],
            ),
            template="plotly_white",
            height=430,
            showlegend=False,
        )
        fig.update_xaxes(rangemode="tozero")
    else:
        x_center = 0
        box_width = 0.5
        cap_width = 0.25

        # 아래 수염: 최솟값 ~ Q1
        fig.add_trace(
            go.Scatter(
                x=[x_center, x_center],
                y=[min_v, q1],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 위 수염: Q3 ~ 최댓값
        fig.add_trace(
            go.Scatter(
                x=[x_center, x_center],
                y=[q3, max_v],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 최솟값 캡
        fig.add_trace(
            go.Scatter(
                x=[x_center - cap_width, x_center + cap_width],
                y=[min_v, min_v],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 최댓값 캡
        fig.add_trace(
            go.Scatter(
                x=[x_center - cap_width, x_center + cap_width],
                y=[max_v, max_v],
                mode="lines",
                line=dict(width=3),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 상자 Q1 ~ Q3
        fig.add_shape(
            type="rect",
            x0=x_center - box_width / 2,
            x1=x_center + box_width / 2,
            y0=q1,
            y1=q3,
            line=dict(width=3),
            fillcolor="rgba(0,0,0,0)",
        )

        # 중앙값 선
        fig.add_trace(
            go.Scatter(
                x=[x_center - box_width / 2, x_center + box_width / 2],
                y=[q2, q2],
                mode="lines",
                line=dict(width=4),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # 각 요소 라벨용 점
        fig.add_trace(
            go.Scatter(
                x=[x_center + 0.45] * 5,
                y=[min_v, q1, q2, q3, max_v],
                mode="markers+text",
                text=["최솟값", "Q1", "중앙값", "Q3", "최댓값"],
                textposition="middle right",
                marker=dict(size=8),
                hovertext=[
                    f"최솟값: {min_v}",
                    f"Q1: {q1}",
                    f"중앙값: {q2}",
                    f"Q3: {q3}",
                    f"최댓값: {max_v}",
                ],
                hoverinfo="text",
                showlegend=False,
            )
        )

        fig.update_layout(
            title=title,
            xaxis=dict(
                showticklabels=False,
                zeroline=False,
                range=[-1, 1.2],
            ),
            yaxis_title="값",
            template="plotly_white",
            height=430,
            showlegend=False,
        )
        fig.update_yaxes(rangemode="tozero")

    return fig, summary


with st.sidebar:
    st.header("설정")

    selected_dataset_name = st.selectbox(
        "예시 데이터를 선택하세요",
        list(sample_data.keys()),
    )
    dot_orientation = st.radio(
        "점그래프 방향",
        options=["가로", "세로"],
        horizontal=True,
    )
    box_orientation = st.radio(
        "상자그림 방향",
        options=["가로", "세로"],
        horizontal=True,
    )


selected_values = sample_data[selected_dataset_name]
summary = five_number_summary(selected_values)

st.subheader(f"선택한 데이터: {selected_dataset_name}")

col1, col2 = st.columns(2)

with col1:
    dot_fig = make_dot_plot(
        selected_values,
        title=f"점그래프({dot_orientation}): 개별 데이터 값 확인",
        orientation=dot_orientation,
    )
    st.plotly_chart(dot_fig, use_container_width=True)

with col2:
    box_fig, summary = make_basic_box_plot(
        selected_values,
        title=f"기본형 상자그림({box_orientation}): 다섯 숫자 요약으로 표현",
        orientation=box_orientation,
    )
    st.plotly_chart(box_fig, use_container_width=True)


st.subheader("다섯 숫자 요약")

st.dataframe(
    {
        "구성요소": list(summary.keys()),
        "값": list(summary.values()),
    },
    use_container_width=True,
)


st.markdown(
    """
### 비교하면서 생각해 볼 질문

1. 점그래프에서는 보이지만 상자그림에서는 보이지 않는 정보는 무엇인가요?
2. 상자그림의 상자는 점그래프의 어느 부분을 요약한 것인가요?
3. 수염이 긴 쪽은 점그래프에서 어떻게 보이나요?
4. 같은 중앙값을 가진 자료라도 퍼짐이 다를 수 있나요?
5. 상자그림은 왜 여러 집단을 비교할 때 편리할까요?
"""
)

st.markdown("---")
st.markdown(
        """
<div style="text-align: center; padding: 0.6rem 0 0.3rem 0;">
    <span style="font-size: 0.95rem; color: #6b7280;">Made by Hyowon Wang</span>
    <a href="https://hyowonwang.netlify.app" target="_blank" style="text-decoration: none; margin-left: 0.45rem; font-size: 1.1rem;" title="hyowonwang.netlify.app">🌐</a>
</div>
""",
        unsafe_allow_html=True,
)