from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routers import mydata

app = FastAPI()

class Query(BaseModel):
    query:str

    
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"] 
)

app.include_router(mydata.router)

@app.get('/')
async def listen():
    return 'App loaded'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)