import os
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from transformers import pipeline

doc_name = 'medical_diagnosis_manual.pdf'
doc_path = f'docs/{doc_name}'
pdf_loader = PyMuPDFLoader(doc_path)
documents = None
embedding_model = None
document_chunks = None
vectorstore = None
llm = None

qna_med_system_message = """
  You are a medical assistant whose work is to review the report and provide the appropriate answers from the context.
  User input will have the context required by you to answer user questions.
  This context will begin with the token: ###Context.
  The context contains references to specific portions of a document relevant to the user query.

  User questions will begin with the token: ###Question.

  Please answer only using the context provided in the input. Do not mention anything about the context in your final answer.
  If the answer is not found in the context, respond "I don't know".
"""

qna_system_message = (
    "You are a helpful assistant. Answer the question using only the context below. "
    "Be concise and factual."
)


# LOAD DATA
def load_data_model():
    global documents
    documents = pdf_loader.load()
    return len(documents)


def check_data_model() -> list:
    global documents
    data = []
    for i in range(8, 15):
        data.append(documents[i].page_content)
    return data


# CHUNKING
def data_chunking_model():
    try:
        global pdf_loader, document_chunks
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name='cl100k_base',
            chunk_size=600,
            chunk_overlap=20
        )
        print("Chunking the data...")
        document_chunks = pdf_loader.load_and_split(text_splitter)
        print(f"Chunking completed — {len(document_chunks)} chunks")
        print("Loading embedding model...")
        embed_data_model()
        return len(document_chunks)
    except Exception as e:
        print(f"Error in chunking: {e}")
        return str(e)


# EMBEDDING
def embed_data_model():
    try:
        global embedding_model
        embedding_model = SentenceTransformerEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("Embedding model ready")
        return 'Embedding model set successfully'
    except Exception as e:
        print(f"Error in embedding: {e}")
        return str(e)


# VECTOR STORE
def generate_vector_store_model():
    try:
        global embedding_model, document_chunks, vectorstore
        out_dir = 'data_vector_db'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        vectorstore = Chroma.from_documents(
            document_chunks,
            embedding_model,
            persist_directory=out_dir
        )
        vectorstore = Chroma(persist_directory=out_dir, embedding_function=embedding_model)
        print("Vector store ready")
        return 'Vector store generated successfully'
    except Exception as e:
        print(f"Error generating vector store: {e}")
        return str(e)


# QUERY VECTOR STORE
def query_vector_store_model(query: str):
    try:
        global vectorstore
        return vectorstore.similarity_search(query, k=3)
    except Exception as e:
        print(f"Error querying vector store: {e}")
        return str(e)


# LLM — TinyLlama via transformers (no llama-cpp needed)
def load_llm_model():
    try:
        global llm
        llm = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            max_new_tokens=300,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2
        )
        print("LLM model loaded successfully")
        return 'LLM model loaded successfully'
    except Exception as e:
        print(f"Error loading LLM: {e}")
        return str(e)


# RAG PIPELINE — retrieve context then generate answer
def generate_rag_pipeline_model(query: str):
    try:
        global vectorstore, llm
        if vectorstore is None:
            return 'Vector store not ready. Call /data-chunking then /generate-vector-store first.'
        if llm is None:
            return 'LLM not loaded. Call /generate-rag-pipeline first.'

        docs = vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = (
            f"{qna_system_message}\n\n"
            f"### Context\n{context}\n\n"
            f"### Question\n{query}\n\n"
            f"### Answer:"
        )

        result = llm(prompt, max_new_tokens=300)
        output = result[0]['generated_text']
        return output[len(prompt):].strip()
    except Exception as e:
        print(f"Error in RAG pipeline: {e}")
        return str(e)
