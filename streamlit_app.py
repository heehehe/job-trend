import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

from utils.graph import job_graph, top_stack_graph

# Construct a BigQuery client object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)
table_name = st.secrets["database"]["table_name"]

st.set_page_config(page_title="JobTrend", page_icon=":chart_with_upwards_trend:")

@st.cache_data      # 여러번호출을 방지함.
def get_unique_job_names():
    query = f"""
    SELECT DISTINCT job_name
    FROM `{table_name}`
    ORDER BY job_name
    """
    result = client.query(query).result().to_dataframe()
    return result['job_name'].tolist()

@st.cache_data
def get_unique_tech_stacks():
    query = f"""
    SELECT DISTINCT tech
    FROM `{table_name}`, 
    UNNEST(tech_list) as tech
    """
    result = client.query(query).result().to_dataframe()
    result['tech'] = result['tech'].str.strip()
    result['tech'] = result['tech'].str.capitalize()
    result = result['tech'].unique()

    return result

def get_openings_by_tech_stack(tech_filter):
    query = f"""
    SELECT COUNT(*) AS num_openings
    FROM `{table_name}`, 
    UNNEST(tech_list) as tech
    WHERE {tech_filter}
    """
    result = client.query(query).result().to_dataframe()
    return result['num_openings'].iloc[0]

def get_openings_by_job_name(job_filter):
    query = f"""
    SELECT COUNT(*) AS num_openings
    FROM `{table_name}`
    WHERE {job_filter}
    """
    result = client.query(query).result().to_dataframe()
    return result['num_openings'].iloc[0]

job_names = get_unique_job_names()
tech_stacks = get_unique_tech_stacks()
def main():
    st.title("JOB TREND for EVERYBODY")
    st.subheader("📊Result")
    # 사이드바
    with st.sidebar:
        col1, col2 = st.columns([6, 3])
        
        with col1:
            st.write("## 👨‍💻Search the JobTrend")
        with col2:
            st.write("")
            search_button = st.button('🔎Search!', key="search_button")

        job_name_selected = st.selectbox("Select job name", ["All"] + job_names)
        tech_stacks_selected = st.multiselect("Select tech stacks", tech_stacks)
        deadline_date = st.date_input("Select a deadline")
    
    # 메인화면
    st.write()
    if search_button:
        # job_name 필터
        job_filter = f"job_name = '{job_name_selected}'" if job_name_selected != "All" else "TRUE"

        # tech_stacks 필터
        if tech_stacks_selected:
            tech_filter = "tech IN ('" + "', '".join(tech_stacks_selected) + "')"
        else:
            tech_filter = "TRUE"
            
        deadline_filter = f"deadline <= '{deadline_date}' OR deadline IS NULL"

        fin_query = f"""
        SELECT company_name, title, job_name, STRING_AGG(tech, ', ') AS tech_stacks,  url, deadline
        FROM `{table_name}`, UNNEST(tech_list) as tech
        WHERE {job_filter}
        AND {tech_filter}
        AND {deadline_filter}
        GROUP BY 
        company_name, 
        title, 
        job_name, 
        url, 
        deadline
        LIMIT 50
        """
        with st.spinner("Loading..."):
            data = client.query(fin_query).result().to_dataframe()
            data['tech_stacks'] = data['tech_stacks'].apply(lambda x: x.split(','))
            # data.to_csv('sample_data.csv', index=False)    # for debugging data...^^;
            
            m1, m2, m3, m4, m5 = st.columns(5)
            m2.metric("Count of Jobs", get_openings_by_job_name(job_filter))
            m3.metric("Count of Tech Stacks", get_openings_by_tech_stack(tech_filter))
            m4.metric("Total Companies", len(data))
            
            tab1, tab2 = st.tabs(["🗃 Data", "📈 Chart"])
            with tab1:
                st.dataframe(data = data,
                            column_config={
                                "url": st.column_config.LinkColumn()
                            })
            with tab2:
                st.info("Working In Progress...😅") 
                st.plotly_chart(top_stack_graph(data['tech_stacks']))
                st.plotly_chart(job_graph(data['job_name']))

if __name__ == "__main__":
    main()
