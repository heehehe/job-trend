import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# Construct a BigQuery client object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)
table_name = st.secrets["database"]["table_name"]

@st.cache_data
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

@st.cache_data
def get_all_data() -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM `{table_name}`
    """
    result = client.query(query).result().to_dataframe()
    return result

@st.cache_data
def get_data(limit: int=None) -> pd.DataFrame:
    query = f"""
        SELECT company_name, title, job_name, tech_list,  url, deadline
        FROM `{table_name}`
    """
    if limit:
        query += f" LIMIT {limit}"
    result = client.query(query).result().to_dataframe()
    result['tech_stacks'] = result['tech_list'].apply(lambda x: [i.strip().capitalize() for i in x])
    result.drop(columns=['tech_list'], inplace=True)
    return result
