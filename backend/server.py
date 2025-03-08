from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from typing import List, Dict, Optional
from opensearchpy import OpenSearch
import cohere
import logging
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pydantic import BaseModel



# Cargar variables de entorno
load_dotenv()

# Configuración de API Keys y credenciales
CONFIG = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "OPENSEARCH_HOST": os.getenv("OPENSEARCH_HOST"),
    "OPENSEARCH_USERNAME": os.getenv("OPENSEARCH_USERNAME"),
    "OPENSEARCH_PASSWORD": os.getenv("OPENSEARCH_PASSWORD"),
    "COHERE_API_KEY": os.getenv("COHERE_API_KEY"),
    "INDEX_NAME": os.getenv("INDEX_NAME")
}
# Inicializar clientes
cohere_client = cohere.Client(CONFIG["COHERE_API_KEY"])
opensearch_client = OpenSearch(
    hosts=[CONFIG["OPENSEARCH_HOST"]],
    http_auth=(CONFIG["OPENSEARCH_USERNAME"], CONFIG["OPENSEARCH_PASSWORD"])
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función para obtener embeddings con Cohere
def get_question_embedding(question: str):
    """Obtiene el embedding de una pregunta usando SentenceTransformer."""
    return embedding_model.encode(question).tolist()

class QueryRequest(BaseModel):
    message: str  # Cambiado de 'question' a 'message' para coincidir con el frontend

    # Clase del sistema RAG
class RAGSystem:
    def __init__(self):
        logger.info("Inicializando RAGSystem...")
        self.client = opensearch_client
        self.index = CONFIG["INDEX_NAME"]

    def query(self, question: str):
        """Busca la mejor respuesta en OpenSearch y genera una respuesta con OpenAI."""
        logger.info(f"Procesando pregunta: {question}")

        # Obtener embedding
        question_embedding = get_question_embedding(question)

        # Realizar la búsqueda en OpenSearch
        query = {
            "size": 3,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": question_embedding,
                        "k": 3
                    }
                }
            }
        }

        response = self.client.search(index=self.index, body=query)
        
        hits = response.get("hits", {}).get("hits", [])

        if not hits:
            return "No encontré información relevante."

        # Extraer textos relevantes
        retrieved_texts = [hit["_source"]["text_chunk"] for hit in hits]

        # Generar respuesta con OpenAI (por ejemplo, utilizando Cohere, OpenAI o cualquier otro LLM)
        prompt = f"""Eres un asistente experto que responde en español.
        Debes mantener un tono profesional y claro en todas tus respuestas.
        Nunca respondas en inglés.
        Sé conciso y directo, evitando divagar o agregar información no solicitada.

        Basándote en el siguiente resumen, responde la consulta de manera concisa y directa:

        Resumen:
        {response}

        Consulta: {question}

        Instrucciones para la respuesta:
        1. RESPONDE EN ESPAÑOL
        2. Sé conciso y directo (máximo 3-4 frases)
        3. No repitas información
        4. Enfócate en los puntos más relevantes
        5. Si la información no es suficiente, indícalo
        6. No incluyas citas literales del texto
        7. Usa un tono profesional y claro
        8. No divagues ni agregues información no solicitada
        9. Si la consulta es sobre precios, incluye la información de manera clara y estructurada
        10. Si la consulta es sobre módulos, organiza la información de manera lógica"""
        
        # Aquí sería donde usarías un modelo para generar la respuesta basada en el prompt.
        # Este ejemplo es con Cohere, pero puede ser OpenAI o cualquier otro modelo.

        # Suponiendo que uses Cohere:
        response = cohere_client.generate(
            model="command-r-plus",  # Reemplaza por el modelo que estés usando
            prompt=prompt,
            max_tokens=200,
            temperature=0.3
        )
        
        # Devuelves solo el texto generado, que es la respuesta
        return response.generations[0].text.strip() if response.generations else "No se pudo generar una respuesta."


rag = RAGSystem()

# Endpoints
@app.post("/chat")  # Cambiado de '/query' a '/chat' para coincidir con el frontend
async def chat(request: QueryRequest):
    try:
        response = rag.query(request.message)  # Cambiado de question a message
        return {
            "message": response
        }
    except Exception as e:
        logger.error(f"Error en la consulta RAG: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en la consulta RAG: {str(e)}")    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)