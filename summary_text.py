from langchain.prompts import PromptTemplate
from summary_text.summary_model_config.model_config import model
from summary_text.utils.summary_text_functions_helper import split_text

def generate_summary(text, level, language):
    """
    Genera un resumen del texto dado según el nivel de detalle y idioma especificados.
    Utiliza plantillas predefinidas para solicitar al modelo resúmenes en diferentes niveles.

    :param text: Texto completo que se desea resumir.
    :param level: Nivel de detalle del resumen. Puede ser uno de los siguientes: brief, intermediate, detailed.
    :param language: Idioma en el que se desea recibir el resumen. Ejemplo: 'es' para español, 'en' para inglés.
    :return: Resumen generado basado en el nivel de detalle y el idioma.
    """
    # Dividir el texto en fragmentos (agregando split_text)
    split_docs = split_text(text)
    combined_text = " ".join([fragment.page_content for fragment in split_docs])

    # Configurar niveles de detalle
    levels = {
        "brief": "Resumen en 1-2 frases cortas.",
        "intermediate": "Resumen en 3-5 frases.",
        "detailed": "Resumen detallado en un párrafo."
    }

    # Crear el prompt con el nivel de detalle y el idioma
    prompt = PromptTemplate(
        input_variables=["text"],
        template=f"Resumir el siguiente texto en el idioma '{language}' conforme al nivel especificado ({levels[level]})."
                 f" Por favor NO incluyas introducciones o notas innecesarias como 'a continuación se presenta' o similares"
                 f"independiente del idioma en el que se te pida el resumen.\n\n{{text}}"
    )
    # Crear flujo de ejecución
    chain = prompt | model

    # Generar el resumen
    result = chain.invoke({"text": combined_text})
    return result