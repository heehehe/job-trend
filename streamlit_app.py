import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# Construct a BigQuery client object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

@st.cache_data      # 여러번호출을 방지함.
def get_unique_job_names():
    query = """
    SELECT DISTINCT job_name
    FROM `recruit-notice.test.jumpit`
    ORDER BY job_name
    """
    result = client.query(query).result().to_dataframe()
    return result['job_name'].tolist()

@st.cache_data
def get_unique_tech_stacks():
    query = """
    SELECT DISTINCT tech
    FROM `recruit-notice.test.jumpit`, 
    UNNEST(tech_list) as tech
    """
    result = client.query(query).result().to_dataframe()
    return result

job_names = get_unique_job_names()
tech_stacks = get_unique_tech_stacks()
def main():
    st.title("JOB TREND for EVERYBODY")
    job_name_selected = st.selectbox("Select job name", ["All"] + job_names)
    tech_stacks_selected = st.multiselect("Select tech stacks(not working)", tech_stacks)
    
    if st.button('🔎Search!'):
        job_filter = f"job_name = '{job_name_selected}'" if job_name_selected != "All" else "TRUE"
        tech_filter = None      # TODO:tech_filter 추가하기

        query = f"""
        SELECT company_name, title, job_name, tech_list
        FROM `recruit-notice.test.jumpit`
        WHERE {job_filter}
        LIMIT 50
        """

        data = client.query(query).result().to_dataframe()
        st.write(data)

if __name__ == "__main__":
    main()