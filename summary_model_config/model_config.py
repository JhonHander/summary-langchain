from langchain_groq import ChatGroq
from config import settings

# Crear una instancia centralizada del modelo
model = ChatGroq(
    model="llama3-8b-8192",
    api_key=settings.GROQ_API_KEY
)
