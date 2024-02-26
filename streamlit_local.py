import ast
import os

import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

from utils.graph import job_graph_pie, sankey_chart, sunburst_chart, top_stack_bar

# Construct a BigQuery client object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)
table_name = st.secrets["database"]["table_name"]
tmp_path = os.path.join('data', 'sampledata.csv')

st.set_page_config(page_title="JobTrend", page_icon=":chart_with_upwards_trend:")

@st.cache_data
def get_all_data() -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM `{table_name}`
    """
    result = client.query(query).result().to_dataframe()
    return result

def get_local_data(tmp_path: str) -> pd.DataFrame:
    df = pd.read_csv(tmp_path)
    for c in df.columns:
        try:
            df[c] = df[c].apply(ast.literal_eval)
        except:
            pass

    return df

@st.cache_data
def get_job_trend_data(limit: int=500) -> pd.DataFrame:
    query = f"""
        SELECT company_name, title, job_name, tech_list,  url, deadline
        FROM `{table_name}`
        LIMIT {limit}
    """
    result = client.query(query).result().to_dataframe()
    result['tech_stacks'] = result['tech_list'].apply(lambda x: [i.strip().capitalize() for i in x])
    result.drop(columns=['tech_list'], inplace=True)
    return result

def main():
    st.title("JOB TREND for EVERYBODY")
    st.subheader("📊Result")
    
    if os.path.exists(tmp_path):
        df = get_local_data(tmp_path)
        df['tech_stacks'] = df['tech_stacks'].apply(lambda x: [i.strip().capitalize() for i in x])
    else:
        df = get_job_trend_data()
        os.makedirs('data', exist_ok=True)
        df.to_csv(tmp_path, index=False)
    
    job_names = df['job_name'].unique().tolist()
    tech_stacks = df['tech_stacks'].explode().unique().tolist()
    companies = df['company_name'].unique().tolist()
    
    # 사이드바
    with st.sidebar:
        col1, col2 = st.columns([6, 3])
        
        with col1:
            st.write("## :technologist: Search the JobTrend")
        with col2:
            st.write("")
            search_button = st.button(':mag_right: Search!', key="search_button")

        job_name_selected = st.selectbox("Select job name", ["All"] + job_names)
        tech_stacks_selected = st.multiselect("Select tech stacks", tech_stacks)
        deadline_date = st.date_input("Select a deadline")
    
    # 메인화면
    if search_button:
        # 필터링 로직
        filtered_df = df.copy()

        if job_name_selected != "All":
            filtered_df = filtered_df[filtered_df['job_name'] == job_name_selected]
        if tech_stacks_selected:
            filtered_df = filtered_df[filtered_df['tech_stacks'].apply(lambda x: any(tech in x for tech in tech_stacks_selected))]
        if deadline_date:
            deadline_filter_date = pd.Timestamp(deadline_date)
            filtered_df = filtered_df[(pd.to_datetime(filtered_df['deadline']) <= deadline_filter_date) | pd.isna(filtered_df['deadline'])]
        
        # 메트릭 표시
        with st.spinner("Loading..."):
            m1, m2, m3, m4, m5 = st.columns(5)
            m2.metric("Count of Jobs", len(job_names))
            m3.metric("Count of Tech Stacks", len(tech_stacks))
            m4.metric("Total Companies", len(companies))
            
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(top_stack_bar(filtered_df['tech_stacks']), use_container_width=True)
            with c2:
                st.plotly_chart(job_graph_pie(filtered_df['job_name']), use_container_width=True)
            
            tab1, tab2 = st.tabs(["🗃 Data", "📈 Chart"])
            with tab1:
                st.dataframe(data = filtered_df,
                            column_config={
                                "url": st.column_config.LinkColumn()
                            })
            with tab2:
                # TODO: chart 뭔가 마음에 안 듦.
                st.plotly_chart(sunburst_chart(df), use_container_width=True)
                st.plotly_chart(sankey_chart(filtered_df), use_container_width=True)

if __name__ == "__main__":
    main()
