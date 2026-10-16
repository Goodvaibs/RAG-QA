from transformers import pipeline, set_seed
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
# from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain_community.vectorstores import Chroma

generator = pipeline("text-generation",
                     model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                     max_new_tokens=300,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.2
                    )
# set_seed(42)
def generate_response(prompt: str) -> str:
    result = generator(prompt, max_length=300)
    output = result[0]['generated_text']
    return output[len(prompt):].strip()
    