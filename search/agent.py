import os

from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import BigQueryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


class SearchAgent:
    def __init__(self, args):
        os.environ["OPENAI_API_KEY"] = args["openai_key"]
        self._project_id = args["project_id"]
    
    def _load_data(self):
        BASE_QUERY = """
                SELECT
                *
                FROM `recruit-notice.test.content`
                """
                
        loader = BigQueryLoader(
            BASE_QUERY,
            project=self._project_id,
        )
        
        return loader.load()
    
    def _vectorize(self, data):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        splits = text_splitter.split_documents(data)
        vector_store = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        
        return vector_store.as_retriever()
    
    def _format_docs(self, docs):
        # 검색한 문서 결과를 하나의 문단으로 합쳐줍니다.
        return "\n\n".join(doc.page_content for doc in docs)
    
    def load_rag(self):
        data = self._load_data()
        retriever = self._vectorize(data)
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(temperature=0.1)
        rag_chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        self._rag_chain = rag_chain

    def run(self, question):
        return self._rag_chain.invoke(question)
        