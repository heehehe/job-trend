import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# Construct a BigQuery client object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)
table_name = st.secrets["database"]["table_name"]

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
    return result

job_names = get_unique_job_names()
tech_stacks = get_unique_tech_stacks()
def main():
    st.title("JOB TREND for EVERYBODY")

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
    st.write("## 📊Result")
    tab1, tab2 = st.tabs(["🗃 Data", "📈 Chart"])
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
            with tab1:
                data = client.query(fin_query).result().to_dataframe()
                data['tech_stacks'] = data['tech_stacks'].apply(lambda x: x.split(','))
                st.dataframe(data = data,
                            column_config={
                                "url": st.column_config.LinkColumn()
                            })
            with tab2:
                st.write("Working In Progress...😅")

if __name__ == "__main__":
    main()
