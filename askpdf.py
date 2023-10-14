'''
    Author: Arthur Sedek
    Email: Arthur.sedek@gmail.com

    DO NOT REMOVE OR MODIFY THE AUTHOR ATTRIBUTION. 
    This attribution acknowledges the efforts of the original developer. 
    Please respect and retain this information when using, modifying, or sharing this code.

    If you have questions or concerns, you're welcome to reach out via the email provided.

'''
 
import os
import re
import PyPDF2 as pdf
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from typing import List
from langchain.docstore.document import Document

class CustomTextLoader(TextLoader):
    def load(self) -> List[Document]:
        try:
            with open(self.file_path, encoding='utf-8', errors='replace') as f:
                text_content = f.read()
            metadata = {"source": str(self.file_path)}
            return [Document(page_content=text_content, metadata=metadata)]
        except UnicodeDecodeError as e:
            # You can log or print the error here if you'd like
            raise RuntimeError(f"Error loading {self.file_path}") from e
        except Exception as e:
            # Catch other types of errors
            raise RuntimeError(f"Error loading {self.file_path}") from e

class AskPDF:
    def __init__(self, config):
        self.n_sources = config["number_of_references"]
        self.temp = config["temperature"]
        self.model = config["model"]
        self.chain = None
        self.conversation_log = []
        self.tokens_length = config["tokens_length"]
        self.embedding = OpenAIEmbeddings()
        self.PageNum: int = 0
        self.DocumentNum: int = 0
        self.count: int = 0
        self.template = """
                Use the following pieces of context to answer the users question.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                ----------------
                {context}
                """
        self.QA_CHAIN_PROMPT = PromptTemplate.from_template(self.template)

    def __call__(self, pdf_file):
        if self.count==0:
            self.chain = self.query_pdf(pdf_file)
            self.count+=1
        return self.chain
    
    def _validate_config(self, config):
        required_keys = ["number_of_references", "temperature", "tokens_length", "model", "openai_api"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing key in config: {key}")

    def _sanitize_string(self, s):
        return re.sub('[^a-zA-Z]', '', s)

    def _initialize_directories(self, pdf_file):
        current_dir = os.getcwd()
        filename_without_extension = str(os.path.basename(pdf_file[0].name)).split(".pdf")[0]
        txt_base_dir = os.path.join(current_dir, f"{filename_without_extension}_text_base_knowledge")
        db_dir = os.path.join(current_dir, f"{filename_without_extension}_db")
        if not os.path.exists(txt_base_dir):
            os.mkdir(txt_base_dir)
        return txt_base_dir, db_dir

    def _handle_existing_db(self, db_dir):
        vectordb = Chroma(persist_directory=db_dir, embedding_function=self.embedding)
        retriever = vectordb.as_retriever(search_kwargs={"k": self.n_sources})
            
        turbo_llm = ChatOpenAI(
            temperature=self.temp,
            max_tokens=self.tokens_length,
            model_name=self.model
        )
        qa_chain = ConversationalRetrievalChain.from_llm(turbo_llm, retriever=retriever, 
                                                         return_source_documents=True,)
        return qa_chain
    
    def _pdf_to_text(self, file1, txt_base_dir):
        try:
            with open(file1.name, 'rb') as file:
                filename = self._sanitize_string(str(os.path.basename(file1.name)).split(".pdf")[0])
                pdf_reader = pdf.PdfReader(file)
                for i in range(0, len(pdf_reader.pages)):
                    pdf_page = pdf_reader.pages[i]
                    text = pdf_page.extract_text()
                    with open(f"{txt_base_dir}/{filename}_{i}.txt", 'w', encoding='utf-8') as file:
                        file.write(text)
        except IOError:
            raise Exception(f"Failed to read the file: {file1.name}")

    def _embed_texts(self, txt_base_dir, db_dir):
        loader = DirectoryLoader(f'{txt_base_dir}/', glob="./*.txt", loader_cls=CustomTextLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        vectordb = Chroma.from_documents(documents=texts, embedding=self.embedding, 
                                         persist_directory=db_dir)
        vectordb.persist()
        vectordb = None
        vectordb = Chroma(persist_directory=db_dir, embedding_function=self.embedding)
        retriever = vectordb.as_retriever(search_kwargs={"k": self.n_sources})
        qa_chain = ConversationalRetrievalChain.from_llm(OpenAI(), retriever=retriever, 
                                                         return_source_documents=True,)
        return qa_chain

    def query_pdf(self, pdf_files):
        txt_base_dir, db_dir = self._initialize_directories(pdf_files)
        if os.path.exists(db_dir):
            chain = self._handle_existing_db(db_dir)
        else:
            os.mkdir(db_dir)
            for pdf_file in pdf_files:
                self._pdf_to_text(pdf_file, txt_base_dir)
            chain = self._embed_texts(txt_base_dir, db_dir)
        return chain