from langchain.prompts import PromptTemplate
from summary_text.summary_model_config.model_config import model
import json

def get_supported_languages():
    """
    Consulta al modelo para obtener la lista de idiomas soportados y los retorna como JSON válido.

    :return: Diccionario de idiomas soportados con nombres y códigos, o None en caso de error.
    """
    prompt = PromptTemplate(
        input_variables=[],
        template=(
            "Proporcióname una lista clara y precisa de todos los idiomas que soportas, "
            "junto con sus códigos ISO (por ejemplo, 'es' para español, 'en' para inglés). "
            "Devuelve este resultado en formato estricto JSON con esta estructura exacta: "
            "{{'idiomas': [{{'nombre': '<Nombre del idioma>', 'codigo': '<código ISO>'}}]}}. "
            "No incluyas ningún texto adicional fuera del formato JSON."
        )
    )

    # Crear flujo de ejecución
    chain = prompt | model

    try:
        result = chain.invoke({})  # Invocar el modelo
        respuesta = result.content  # Obtener contenido de la respuesta
        valid, data = validate_llm_lenguage(respuesta)

        if not valid:
            raise ValueError("La respuesta no contiene un formato JSON válido.")
        return data  # Retorna el JSON correctamente parseado en forma de diccionario

    except Exception as e:
        print(f"Error al obtener o validar los idiomas soportados: {e}")
        return None  # Retornamos None para manejar el error en la interfaz



def validate_llm_lenguage(respuesta):
    """
    Valida una respuesta generada por un modelo LLM verificando su formato y contenido.
    La función asegura que la respuesta esté en formato JSON y contenga una clave
    'idiomas' cuyo valor sea una lista.

    :param respuesta: La cadena en formato JSON a validar.
    :type respuesta: str
    :return: Una tupla que contiene un booleano indicando si la validación fue exitosa
        y un diccionario con los datos decodificados en caso de ser válido, o None de lo contrario.
    :rtype: tuple[bool, dict | None]
    """
    try:
        data = json.loads(respuesta)
        if "idiomas" in data and isinstance(data["idiomas"], list):
            return True, data
        return False, None
    except json.JSONDecodeError:
        return False, None