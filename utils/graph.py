from collections import Counter

import pandas as pd
import plotly.express as px


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
    list(group_jobs.items()), columns=['Technology', 'Count']
    ).sort_values(by='Count', ascending=False)
    fig = px.pie(job_df, names='Technology', values='Count')
    
    return fig