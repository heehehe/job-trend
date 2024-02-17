import pandas as pd
import streamlit as st

from utils.graph import job_graph_pie, sankey_chart, sunburst_chart, top_stack_bar
from utils.query import get_data

st.set_page_config(
    page_title="JobTrend",
    page_icon=":chart_with_upwards_trend:",
    initial_sidebar_state="expanded",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/heehehe/job-trend/issues",
        "About": "# JobTrend",
    },
)
st.session_state.open_chart = True


def main():
    st.title("JOB TREND for EVERYBODY")

    with st.spinner("Get data..."):
        df = get_data()

    job_names = df["job_name"].unique().tolist()
    tech_stacks = df["tech_stacks"].explode().unique().tolist()
    companies = df["company_name"].unique().tolist()

    # 사이드바
    with st.sidebar:
        col1, col2 = st.columns([6, 3])
        st.title(":technologist: Search the JobTrend")
        # with col1:
        # with col2:
            # st.write("")
            # search_button = st.button(":mag_right: Search!", key="search_button")

        job_name_selected = st.multiselect(
            "Select job name", ["All"] + job_names, "All"
        )
        tech_stacks_selected = st.multiselect(
            "Select tech stacks", ["All"] + tech_stacks, "All"
        )
        # st.button("button", type='primary', use_container_width=True)
        deadline_date = st.date_input("Select a deadline")
        
        check_ongoing = st.checkbox('Exclude ongoing')
        chart_switch = st.checkbox("More chart")
        search_button = st.button(":mag_right: Search!", key="search_button", use_container_width=True)
        print(f"{job_name_selected=}, {tech_stacks_selected=}, {deadline_date=}")

    # 메인화면
    st.subheader('Overview', divider='grey')
    m1, m2, m3, m4, m5 = st.columns(5)
    m2.metric("**Count of Jobs**", len(job_names))
    m3.metric("**Count of Tech Stacks**", len(tech_stacks))
    m4.metric("**Total Companies**", len(companies))

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(top_stack_bar(df["tech_stacks"]), use_container_width=True)
    with c2:
        st.plotly_chart(job_graph_pie(df["job_name"], 0.5), use_container_width=True)

    if search_button:
        st.subheader("🗃 Result", divider="grey")
        # 필터링 로직
        filtered_df = df.copy()

        if job_name_selected != (["All"] or []):
            filtered_df = filtered_df[
                filtered_df["job_name"].apply(
                    lambda x: any(tech in x for tech in job_name_selected)
                )
            ]
        if tech_stacks_selected != (["All"] or []):
            filtered_df = filtered_df[
                filtered_df["tech_stacks"].apply(
                    lambda x: any(tech in x for tech in tech_stacks_selected)
                )
            ]
        if deadline_date:
            deadline_filter_date = pd.Timestamp(deadline_date)
            if check_ongoing:
                filtered_df = filtered_df[
                    (pd.to_datetime(filtered_df["deadline"]) <= deadline_filter_date)
                    & pd.notnull(filtered_df["deadline"])
                ]
            else:
                filtered_df = filtered_df[
                    (pd.to_datetime(filtered_df["deadline"]) <= deadline_filter_date)
                    | pd.isna(filtered_df["deadline"])
                ]

        st.dataframe(
            data=filtered_df, column_config={"url": st.column_config.LinkColumn()},
            use_container_width=True
        )

        if chart_switch:
            st.subheader(":bar_chart: More Charts...", divider="grey")
            with st.spinner("Loading..."):
                with st.expander("**Sunburst chart**"):
                    st.plotly_chart(
                        sunburst_chart(filtered_df), use_container_width=True
                    )
                with st.expander("**Sankey chart**"):
                    st.plotly_chart(sankey_chart(filtered_df), use_container_width=True)


if __name__ == "__main__":
    main()
