import streamlit as st
import plotly.graph_objects as go
from statistics import median


st.set_page_config(page_title="두 집단 상자그림 비교", page_icon="📦", layout="wide")

st.title("📦 두 집단 상자그림 비교")

st.markdown(
    """
이 페이지에서는 두 집단의 데이터를 **기본형 상자그림**으로 한 그래프 안에 나란히 비교합니다.

- 두 집단의 **중앙값**을 비교할 수 있습니다.
- 두 집단의 **상자 길이**를 통해 가운데 50% 자료의 퍼짐을 비교할 수 있습니다.
- 두 집단의 **수염 길이**를 통해 전체 자료의 퍼짐을 비교할 수 있습니다.
- 두 상자의 **위치와 겹침**을 통해 분포가 얼마나 비슷하거나 다른지 살펴볼 수 있습니다.

> 이 페이지의 상자그림은 이상치를 따로 표시하지 않는 **기본형 상자그림**입니다.  
> 따라서 수염의 끝은 각각 **최솟값**과 **최댓값**을 의미합니다.
"""
)


comparison_data = {
    "A반과 B반 퀴즈 점수": {
        "A반": [50, 55, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 81, 86],
        "B반": [30, 40, 48, 55, 60, 64, 66, 68, 70, 72, 76, 81, 88, 96, 100],
    },
    "두 학습 방법의 문제 해결 시간": {
        "방법 A": [45, 48, 50, 52, 53, 55, 56, 58, 60, 63, 67, 72, 80, 90, 105],
        "방법 B": [42, 44, 46, 48, 50, 52, 53, 55, 57, 60, 62, 65, 68, 72, 78],
    },
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


def add_basic_box_horizontal(fig, values, label, y_center):
    """가로 기본형 상자그림을 Figure에 추가"""
    summary = five_number_summary(values)

    min_v = summary["최솟값"]
    q1 = summary["Q1"]
    q2 = summary["중앙값"]
    q3 = summary["Q3"]
    max_v = summary["최댓값"]

    box_height = 0.45
    cap_height = 0.22

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

    # hover용 다섯 숫자 점
    fig.add_trace(
        go.Scatter(
            x=[min_v, q1, q2, q3, max_v],
            y=[y_center] * 5,
            mode="markers",
            marker=dict(size=8),
            hovertext=[
                f"{label}<br>최솟값: {min_v}",
                f"{label}<br>Q1: {q1}",
                f"{label}<br>중앙값: {q2}",
                f"{label}<br>Q3: {q3}",
                f"{label}<br>최댓값: {max_v}",
            ],
            hoverinfo="text",
            showlegend=False,
        )
    )

    return summary


def add_basic_box_vertical(fig, values, label, x_center):
    """세로 기본형 상자그림을 Figure에 추가"""
    summary = five_number_summary(values)

    min_v = summary["최솟값"]
    q1 = summary["Q1"]
    q2 = summary["중앙값"]
    q3 = summary["Q3"]
    max_v = summary["최댓값"]

    box_width = 0.45
    cap_width = 0.22

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

    # hover용 다섯 숫자 점
    fig.add_trace(
        go.Scatter(
            x=[x_center] * 5,
            y=[min_v, q1, q2, q3, max_v],
            mode="markers",
            marker=dict(size=8),
            hovertext=[
                f"{label}<br>최솟값: {min_v}",
                f"{label}<br>Q1: {q1}",
                f"{label}<br>중앙값: {q2}",
                f"{label}<br>Q3: {q3}",
                f"{label}<br>최댓값: {max_v}",
            ],
            hoverinfo="text",
            showlegend=False,
        )
    )

    return summary


def make_two_group_box_plot(group_data, orientation):
    """두 집단 기본형 상자그림을 한 Figure에 표시"""
    fig = go.Figure()
    group_names = list(group_data.keys())

    summaries = {}

    if orientation == "가로":
        y_positions = [1, 0]

        for group_name, y_pos in zip(group_names, y_positions):
            summaries[group_name] = add_basic_box_horizontal(
                fig=fig,
                values=group_data[group_name],
                label=group_name,
                y_center=y_pos,
            )

        fig.update_layout(
            title="두 집단 기본형 상자그림 비교",
            xaxis_title="값",
            yaxis=dict(
                tickmode="array",
                tickvals=y_positions,
                ticktext=group_names,
                range=[-0.8, 1.8],
            ),
            template="plotly_white",
            height=520,
            showlegend=False,
        )
        fig.update_xaxes(rangemode="tozero")

    else:
        x_positions = [0, 1]

        for group_name, x_pos in zip(group_names, x_positions):
            summaries[group_name] = add_basic_box_vertical(
                fig=fig,
                values=group_data[group_name],
                label=group_name,
                x_center=x_pos,
            )

        fig.update_layout(
            title="두 집단 기본형 상자그림 비교",
            xaxis=dict(
                tickmode="array",
                tickvals=x_positions,
                ticktext=group_names,
                range=[-0.8, 1.8],
            ),
            yaxis_title="값",
            template="plotly_white",
            height=520,
            showlegend=False,
        )
        fig.update_yaxes(rangemode="tozero")

    return fig, summaries


with st.sidebar:
    st.header("설정")

    selected_case_name = st.selectbox(
        "비교할 예시 데이터를 선택하세요",
        list(comparison_data.keys()),
    )

    orientation = st.radio(
        "상자그림 방향",
        options=["세로", "가로"],
        horizontal=True,
    )


selected_group_data = comparison_data[selected_case_name]

st.subheader(f"선택한 비교 예시: {selected_case_name}")

fig, summaries = make_two_group_box_plot(
    group_data=selected_group_data,
    orientation=orientation,
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("다섯 숫자 요약 비교")

summary_rows = []

for group_name, summary in summaries.items():
    summary_rows.append(
        {
            "집단": group_name,
            "최솟값": summary["최솟값"],
            "Q1": summary["Q1"],
            "중앙값": summary["중앙값"],
            "Q3": summary["Q3"],
            "최댓값": summary["최댓값"],
            "상자의 길이(Q3-Q1)": summary["Q3"] - summary["Q1"],
            "전체 범위": summary["최댓값"] - summary["최솟값"],
        }
    )

st.dataframe(summary_rows, use_container_width=True)


st.markdown(
    """
### 비교하면서 생각해 볼 질문

1. 어느 집단의 중앙값이 더 큰가요?
2. 어느 집단의 상자가 더 긴가요?
3. 상자의 길이가 길다는 것은 무엇을 의미하나요?
4. 어느 집단의 수염이 더 긴가요?
5. 두 집단의 상자는 얼마나 겹치나요?
6. 한 집단의 분포가 다른 집단보다 전체적으로 오른쪽 또는 위쪽에 있나요?
7. 중앙값만 보고 결론을 내려도 될까요?
8. 이 자료의 맥락에서 어느 집단이 더 안정적이라고 볼 수 있나요?
"""
)