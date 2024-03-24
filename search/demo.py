from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import openai
import streamlit as st

from agent import SearchAgent


st.set_page_config(page_title="Job Trend")
st.title("Job Trend")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

# Setup LLM and QA chain
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, streaming=True
)

args = {
    "openai_key": st.secrets["OPENAI_API_KEY"],
    "project_id": st.secrets["BIGQUERY_PROJECT_ID"]
    }

agent = SearchAgent(args)
agent.load_rag()

if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        response = agent.run(user_query)
        st.write(response)