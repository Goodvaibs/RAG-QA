from pydantic import BaseModel
from agents.myagent import ask_question
from agents.myagent import load_data, check_data, data_chunking, generate_vector_store, query_vector_store, load_llm
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["mydata"])

class Query(BaseModel):
    query:str

@router.get('/load-data')
def load_data_api():    # type: ignore
    try:
        result = load_data()
        return {'result': result, 'status': 'success', 'code':200}
    except Exception as e:
        return {'result': e, 'status': 'error', 'code':500}

@router.get('/check-data')
def check_data_api():
    try:
        result = check_data()
        return {'result': result, 'status': 'success', 'code':200}
    except Exception as e:
        return {'result': e, 'status': 'error', 'code':500}

@router.post('/data-chunking')
def data_chunking_api():
    try:
        result = data_chunking()
        return {'result': result, 'status': 'success', 'code':200}
    except Exception as e:
        return {'result': e, 'status': 'error', 'code':500}

@router.post('/generate-vector-store')
def generate_vector_store_api():
    try:
        result = generate_vector_store()
        return {'result': result, 'status': 'success', 'code':200}
    except Exception as e:
        return {'result': e, 'status': 'error', 'code':500}

@router.post('/query-vector-store')
def query_vector_store_api(data: Query):
    try:
        result = query_vector_store(data.query)
        return {'result': result, 'status': 'success', 'code':200}
    except Exception as e:
        return {'result': e, 'status': 'error', 'code':500}

@router.get('/load-llm')
def generate_rag_pipeline_api():
    try:
        result = load_llm()
        return {'result': result, 'status': 'success', 'code':200}
    except Exception as e:
        return {'result': e, 'status': 'error', 'code':500}

@router.post('/ask-question')
def ask_agent(data: Query):
    try:
        print(data.query)
        result = ask_question(data.query)
        return {'result': result, 'status': 'success', 'code':200}
    except Exception as e:
        return {'result': e, 'status': 'error', 'code':500}