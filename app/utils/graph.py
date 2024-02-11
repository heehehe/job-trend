from collections import Counter

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def top_stack_bar(stacks):
    techs = [t.strip().capitalize() for t in sum(stacks, [])]
    group_techs = Counter(techs)
    tech_df = pd.DataFrame(
        list(group_techs.items()), columns=["Technology", "Count"]
    ).sort_values(by="Count", ascending=False)
    tech_df = tech_df.iloc[:20]
    fig = px.bar(tech_df, x="Technology", y="Count")
    fig.update_layout(title_text="Top 20 Technologies", width=800)
    return fig


def job_graph_pie(jobs, other_ratio: float=1.0):
    group_jobs = Counter(jobs)
    job_df = pd.DataFrame(
        list(group_jobs.items()), columns=["Job", "Count"]
    ).sort_values(by="Count", ascending=False)
    
    # 1% 미만 처리
    total_count = job_df["Count"].sum()
    job_df["Percentage"] = round(job_df["Count"] / total_count * 100, 3)
    others = job_df[job_df["Percentage"] < other_ratio]
    job_df = job_df[job_df["Percentage"] >= other_ratio]
    others_sum = others["Count"].sum()
    if others_sum > 0:
        others_row = pd.DataFrame([{"Job": "기타", "Count": others_sum}])
        job_df = pd.concat([job_df, others_row], ignore_index=True)

    fig = px.pie(job_df, names="Job", values="Count", title="Tech Job Ratios", width=800)

    return fig


def sunburst_chart(df):
    df = df.explode("tech_stacks")
    sunburst_data = (
        df.groupby(["job_name", "tech_stacks"]).size().reset_index(name="count")
    )
    total_count = df.shape[0]
    sunburst_data["percentage"] = round(sunburst_data["count"] / total_count * 100, 3)
    # sunburst_data = sunburst_data[sunburst_data['job_name'] == 'SW/솔루션']     # filtered data when it needs

    fig = px.sunburst(
        sunburst_data,
        path=["job_name", "tech_stacks"],
        values="percentage",
    )
    fig.update_layout(
        title_text="Sunburst Chart of Jobs and Tech Stacks",
        width=800,
        height=800,
    )
    return fig


def sankey_chart(df, column_for_jobs="job_name", column_for_techs="tech_stacks"):
    # TODO: 수정해야 함.
    # 각 노드에 대한 라벨 생성
    df = df.explode("tech_stacks")
    job_labels = df[column_for_jobs].unique().tolist()
    tech_labels = df[column_for_techs].unique().tolist()
    labels = job_labels + tech_labels

    # source, target, value 리스트 생성
    source = []
    target = []
    value = []

    for index, row in df.iterrows():
        job_index = job_labels.index(row["job_name"])
        tech_index = tech_labels.index(row["tech_stacks"]) + len(job_labels)

        source.append(job_index)
        target.append(tech_index)
        value.append(1)

    # Sankey 차트 생성
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    # line=dict(color="black", width=0.5),
                    label=labels,
                ),
                link=dict(source=source, target=target, value=value),
            )
        ],
    )

    fig.update_layout(
        title_text="Sankey Diagram of Jobs and Tech Stacks",
        width=600,
        height=len(labels) * 20 if len(labels) != 0 else 100,
    )

    return fig
