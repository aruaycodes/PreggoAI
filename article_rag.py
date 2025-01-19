
from typing import List, Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import os
import pickle

class ArticleRAG:
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.documents = []
        self.vector_store = None
        self.qa_chain = None
        self.summarize_chain = None
        self.initialized = False
    def initialize(self):
        if not self.initialized:
            # Step 1: Scrape articles
            print("Starting article scraping...")
            self.scrape_articles()

            # Step 2: Process documents (split them into chunks)
            print("\nProcessing documents...")
            self.process_documents()

            # Step 3: Create a vector store from the processed documents
            print("\nCreating vector store...")
            self.create_vector_store()

            # Step 4: Setup the QA chain for querying
            print("\nSetting up QA chain...")
            self.setup_qa_chain()

            self.initialized = True
            print("RAG system initialized successfully!")


    def scrape_articles(self) -> None:
        loader = WebBaseLoader(self.urls)
        self.documents = loader.load()
        print(f"Successfully scraped {len(self.documents)} articles")

        for i, doc in enumerate(self.documents):
            print(f"\nDocument {i+1} preview:")
            print(doc.page_content[:200] + "...")

    def process_documents(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        self.splits = text_splitter.split_documents(self.documents)
        print(f"\nCreated {len(self.splits)} text chunks")

        print("\nExample chunks:")
        for i, chunk in enumerate(self.splits[:2]):
            print(f"\nChunk {i+1}:")
            print(chunk.page_content[:200] + "...")

    def create_vector_store(self) -> None:
        print("\nInitializing embeddings model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        print("Creating vector store...")
        self.vector_store = FAISS.from_documents(self.splits, embeddings)
        print("Vector store created successfully")

    def setup_qa_chain(self, temperature: float = 0.1) -> None:
        llm = ChatOpenAI(temperature=temperature, model_name="gpt-3.5-turbo")

        # Create the retriever directly from the vector store
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})  # Limit to top 3 most relevant chunks

        # Create the main QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,  # Pass the retriever here
            return_source_documents=True
        )

        # Create a summarization chain
        summarization_template = """
        Summarize the following text in less than 100 words while maintaining the key information:

        {text}

        Summary:"""

        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain

        self.summarize_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                template=summarization_template,
                input_variables=["text"]
            )
        )

        print("\nQA and summarization chains setup complete")

    def summarize_text(self, text: str) -> str:
        """Summarize text to be under 100 words"""
        summary = self.summarize_chain.run(text)
        return summary.strip()

    def get_unique_sources(self, source_docs: List) -> List:
        """Get up to 3 unique sources from the retrieved documents"""
        unique_sources = []
        seen_urls = set()

        for doc in source_docs:
            url = doc.metadata.get('source', 'Unknown')
            if url not in seen_urls and len(unique_sources) < 3:
                seen_urls.add(url)
                unique_sources.append(doc)

        return unique_sources

    def query(self, question: str) -> Dict:
        """Query the RAG system with limited sources and summarized answers"""
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Run setup_qa_chain() first.")

        print(f"\nProcessing question: {question}")
        result = self.qa_chain(question)

        # Get up to 3 unique sources
        unique_source_docs = self.get_unique_sources(result['source_documents'])

        # Summarize the main answer
        summarized_answer = self.summarize_text(result['result'])

        # Format the response with summarized content for each source
        response = {
            'answer': summarized_answer,
            'sources': []
        }

        # Process each unique source
        for doc in unique_source_docs:
            # Summarize the chunk content
            summarized_chunk = self.summarize_text(doc.page_content)

            response['sources'].append({
                'url': doc.metadata.get('source', 'Unknown'),
                'summary': summarized_chunk
            })

        # Print formatted response
        print("\nSummarized Answer:", response['answer'])
        print("\nSources used:")
        for i, source in enumerate(response['sources'], 1):
            print(f"\nSource {i}:")
            print(f"URL: {source['url']}")
            print(f"Summary: {source['summary']}")

        return response

def save_vector_store(vector_store, filename="faiss_store"):
    vector_store.save_local(filename)
    print(f"\nVector store saved as '{filename}'")

def load_vector_store(filename="faiss_store"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    vector_store = FAISS.load_local(filename, embeddings)
    print(f"\nVector store loaded from '{filename}'")
    return vector_store
def query(self, question):
        if not self.initialized:
            raise ValueError("QA chain not initialized. Run setup_qa_chain() first.")
        
        # Query the system with the provided question and return the response
        response = self.qa_chain.ask(question)
        return response
