![image](https://github.com/user-attachments/assets/13e0dd33-1449-49b8-8e93-0b4cbb7adeb6)

# Chatbot con IA Generativa para Escuelas de Bootcamps y Masters

Este proyecto es un chatbot basado en **IA Generativa** que permite a potenciales alumnos obtener información instantánea sobre cursos y programas académicos. Implementamos un sistema **RAG (Retrieval-Augmented Generation)** para optimizar la precisión de las respuestas utilizando documentación de la escuela.

## 🛠️ Tecnologías Utilizadas

- **Frontend:** React, HTML, CSS
- **Backend:** Python + FastAPI
- **Bases de datos:** MySQL (relacional) + Pinecone (vectorial)
- **IA Generativa:** Cohere como LLM
- **Infraestructura:** Docker + Google Cloud Run

## 📌 Características

✅ Chatbot basado en IA generativa para responder preguntas en tiempo real.  
✅ Indexación de información desde PDFs, Excels y Web Scraping con **CrewAI**.  
✅ Sistema RAG que procesa la información en **Pinecone** para mejorar las respuestas.  
✅ Almacenamiento de preguntas y respuestas en **MySQL** para análisis posterior.  
✅ Despliegue escalable en **Google Cloud Run** con contenedores Docker.

## ⚙️ Arquitectura del Sistema

1️⃣ **Usuario pregunta** en el chatbot.  
2️⃣ La pregunta se transforma en embeddings y se busca en la base de datos vectorial (**Pinecone**).  
3️⃣ El modelo **Cohere LLM** procesa la mejor respuesta basada en la información almacenada.  
4️⃣ La pregunta y respuesta se guardan en **MySQL** para mejorar futuras interacciones.  
5️⃣ Se muestra la respuesta al usuario en tiempo real.  

## 🚀 Despliegue

Para ejecutar el chatbot localmene (asegúrate de tener tus Keys necesarias).
Tendras que arrancar el backend (python server.py) y el frontend (npm start)

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/chatbot-educacion.git
cd chatbot-educacion

# Construir y correr con Docker
docker-compose up --build
```

Para desplegar en **Google Cloud Run**, asegúrate de tener configurado tu proyecto y tus Keys necesarias.
Al realizarlo tendras que hacer el deploy primero del backend y sustituirlo su url en el frontend para que pueda llamarlo, en el archivo ActionProvider.js

Si lo prefiere puede consultarmelo y le facilitaré los recursos.
