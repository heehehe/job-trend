from collections import Counter

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def top_stack_bar(stacks):
    techs = [t.strip().capitalize() for t in sum(stacks, [])]
    group_techs = Counter(techs)
    tech_df = pd.DataFrame(
        list(group_techs.items()), columns=['Technology', 'Count']
        ).sort_values(by='Count', ascending=False)
    tech_df = tech_df.iloc[:20]
    fig = px.bar(tech_df, x='Technology', y='Count')
    
    return fig

def job_graph_pie(jobs):
    group_jobs = Counter(jobs)
    job_df = pd.DataFrame(
    list(group_jobs.items()), columns=['Job', 'Count']
    ).sort_values(by='Count', ascending=False)
    fig = px.pie(job_df, names='Job', values='Count')
    
    return fig

def sunburst_chart(df):
    df = df.explode('tech_stacks')
    sunburst_data = df.groupby(['job_name', 'tech_stacks']).size().reset_index(name='count')
    total_count = df.shape[0]
    sunburst_data['percentage'] = round(sunburst_data['count'] / total_count * 100, 3)
    # sunburst_data = sunburst_data[sunburst_data['job_name'] == 'SW/솔루션']     # filtered data when it needs
    
    fig = px.sunburst(
        sunburst_data,
        path=['job_name', 'tech_stacks'],
        values = 'percentage'
    )
    
    return fig

def sankey_chart(df, column_for_jobs='job_name', column_for_techs='tech_stacks'):
    #TODO: 수정해야 함.
    # 각 노드에 대한 라벨 생성
    df = df.explode('tech_stacks')
    job_labels = df['job_name'].unique().tolist()
    tech_labels = df['tech_stacks'].str.strip().str.capitalize().unique().tolist()
    labels = job_labels + tech_labels

    # source, target, value 리스트 생성
    source = []
    target = []
    value = []
    
    for index, row in df.iterrows():
        job_index = job_labels.index(row['job_name'])
        tech_index = tech_labels.index(row['tech_stacks']) + len(job_labels)
        
        source.append(job_index)
        target.append(tech_index)
        value.append(1)  

    # Sankey 차트 생성
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            # line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        ))])

    fig.update_layout(title_text='Sankey Diagram of Jobs and Tech Stacks')
    
    return fig
