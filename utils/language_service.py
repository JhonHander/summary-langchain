from summary_text.utils.get_languages import get_supported_languages, validate_llm_lenguage
import streamlit as st

def fetch_and_validate_languages():
    """
    Obtiene la lista de idiomas desde el modelo y valida su formato. Además, almacena el resultado en
    `st.session_state` para evitar duplicación de cálculos.

    :return: Diccionario de idiomas con nombres y códigos, o lanza mensajes de error si hay problemas.
    """
    # Verificar si los idiomas ya están en `st.session_state`
    if "idiomas" in st.session_state and st.session_state.idiomas is not None:
        return st.session_state.idiomas

    # Obtener los idiomas soportados
    idiomas_response = get_supported_languages()
    if not idiomas_response:
        st.error("No se pudo obtener una respuesta válida del modelo.")
        return None

    try:
        # Validar el formato de la respuesta
        if isinstance(idiomas_response, str):  # Si es una cadena JSON
            valid, idiomas_dict = validate_llm_lenguage(idiomas_response)
        elif isinstance(idiomas_response, dict):  # Si ya viene en formato dict Python
            valid, idiomas_dict = True, idiomas_response
        else:
            raise TypeError("El formato de la respuesta del modelo no es compatible.")

        # Validar la estructura esperada
        if not valid or "idiomas" not in idiomas_dict:
            raise ValueError("La respuesta no contiene el formato adecuado o esperado.")

        # Crear el diccionario de idiomas {nombre: código}
        idiomas = {idioma["nombre"]: idioma["codigo"] for idioma in idiomas_dict["idiomas"]}

        # Guardar en `st.session_state` para reutilizarlo
        st.session_state.idiomas = idiomas
        return idiomas

    except Exception as e:
        # Manejar los errores y proporcionar mensajes descriptivos para depuración
        st.error("Ocurrió un error al procesar la lista de idiomas.")
        st.error(f"Detalles del error: {str(e)}")
        return None