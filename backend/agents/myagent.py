from models.mymodel import (
    load_data_model,
    check_data_model,
    data_chunking_model,
    generate_vector_store_model,
    query_vector_store_model,
    load_llm_model,
    generate_rag_pipeline_model
)


def load_data():
    return load_data_model()

def check_data():
    return check_data_model()

def data_chunking():
    return data_chunking_model()

def generate_vector_store():
    return generate_vector_store_model()

def query_vector_store(query: str):
    return query_vector_store_model(query)

def load_llm():
    return load_llm_model()

def ask_question(query: str) -> str:
    return generate_rag_pipeline_model(query)
