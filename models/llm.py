from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import json
from openai import OpenAI
from langchain_openai import ChatOpenAI
import os
import re

import sys
sys.path.append(r"./")

from dotenv import load_dotenv
_ = load_dotenv()

class LLM:
    def __init__(self, model_embedding_name= "hiieu/halong_embedding", openai_model="gpt-4o-mini"):
        self.model_embedding_name = model_embedding_name
        self.openai_model = openai_model
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model_emb = None
        self.docs = None
        self.db = None

    def transform_json_to_documents(self, file_path, chunk_size=100, chunk_overlap=20):
        print("Transform json to documents")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        documents = []
        for item in data:
            texts = text_splitter.split_text(item['text'])
            for text in texts:
                doc = Document(
                    page_content=text,
                    metadata={"frame_start": int(item['start'])}
                )
                documents.append(doc)      
        return documents

    def rewrite_query(self, query):
        prompt = f'Chuyển đổi câu sau thành dạng viết lại có thể thể hiện đầy đủ thông tin của câu gốc: "{query}"'
        client = OpenAI(
            api_key=self.openai_api_key,
        )
        response = client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        return content
    
    def rerank_documents(self, documents, query):
        print("Rerank documents")
        context_str = "\n".join([f"Document {i + 1}:\n{doc.page_content}" for i, doc in enumerate(documents)])
        prompt = f"""
        A list of documents is shown below. Each document has content that is the content of the document. A question is also provided.
        Respond with the numbers of the documents you should consult to answer the question, in order of relevance, as well
        as the relevance score. The relevance score is a number from 1–10 based on how relevant you think the document is to the question.
        Must include all the documents in the answer. The documents in answer must be sorted by relevance scores descending. Not include 'Answer:' in answer.
        Example format:
        Document 1:
        <content of document 1>
        Document 2:
        <content of document 2>
        …
        Document 10:
        <content of document 10>
        Question: <question>
        Answer:
        Doc: 9, Relevance: 7
        Doc: 3, Relevance: 5
        Doc: 7, Relevance: 4
        Doc: 6, Relevance: 4
        Doc: 4, Relevance: 4
        Doc: 10, Relevance: 3
        Doc: 1, Relevance: 2
        Doc: 2, Relevance: 2
        Doc: 5, Relevance: 1
        Doc: 8, Relevance: 1

        Let's try this now:
        {context_str}
        Question: {query}
        Answer:
        """

        client = OpenAI(
            api_key=self.openai_api_key,
        )
        response = client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        return content

    def convert_format(self, result, orig_docs):
        print("Convert format result to ids and scores")
        # Extract doc ids and relevance scores from the result string
        pattern = r"Doc: (\d+), Relevance: (\d+)"
        matches = re.findall(pattern, result)
        res = [(int(doc) - 1, int(relevance)) for doc, relevance in matches]
        # Map doc ids to original documents
        id_score_dict = {}
        for i, score in res:
            frame_start = orig_docs[i].metadata['frame_start']
            if frame_start not in id_score_dict:
                id_score_dict[frame_start] = score
        # Convert the dictionary back to ids and scores lists
        ids = list(id_score_dict.keys())
        scores = list(id_score_dict.values())
        return ids, scores
    
    def create_db(self, index_name, asr_path, chunk_size=100, chunk_overlap=20):
        self.model_emb = HuggingFaceEmbeddings(model_name=self.model_embedding_name)
        self.docs = self.transform_json_to_documents(asr_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.db = FAISS.from_documents(self.docs, self.model_emb)
        self.db.save_local(index_name)

    def load_db(self, index_name, allow_dangerous_deserialization=True):
        self.model_emb = HuggingFaceEmbeddings(model_name=self.model_embedding_name)
        self.db = FAISS.load_local(index_name, self.model_emb, allow_dangerous_deserialization=allow_dangerous_deserialization)

    def retrieve(self, query):
        new_query = self.rewrite_query(query)
        print(new_query)
        relevant_docs = self.db.similarity_search(new_query, k=20)
        # print(relevant_docs)
        rerank_docs = self.rerank_documents(relevant_docs, new_query)
        print(rerank_docs)
        results = self.convert_format(rerank_docs, relevant_docs)
        return results
    
    def retrival_QA(self, question):
        # Build prompt
        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. 
        {context}
        Question: {question}
        Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
        
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0)
        qa_chain = RetrievalQA.from_chain_type(
                        llm,
                        retriever=self.db.as_retriever(),
                        return_source_documents=True,
                        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
                    )
        
        result = qa_chain.invoke({"query": question})
        # print(result)
        rst = result["result"]
        source_document = result["source_documents"]
        return rst, source_document


if __name__ == "__main__":
    
    asr_path = r"D:\THANHSTAR\Projetcs\AIC\DATA\asr\final_asr.json"
    llm = LLM()
    
    index_name = r".\DATA\asr\llm_index"
    
    # ĐẦU TIÊN CHẠY DÒNG DƯỚI NÀY ĐỂ TẠO DATABASE,XONG CHẠY LẦN 2 TRỞ ĐI THÌ CMT NÓ LẠI
    # llm.create_db(index_name, asr_path)
    # CHẠY LẦN ĐẦU CẦN LOAD_MODEL VỚI TẠO DATABASE NÊN HƠI LÂU
    
    
    llm.load_db(index_name)
    # query = "nhà hàng michelin 5 sao"
    # ids, scores = llm.retrieve(query, llm.db, llm.openai_api_key)
    # print(ids)
    # print(scores)
    
    question = "Nhà hàng michelin bắt đầu từ năm nào?"
    # result, source_document = llm.retrival_QA(question)
    # print(result)
    # print(source_document)
