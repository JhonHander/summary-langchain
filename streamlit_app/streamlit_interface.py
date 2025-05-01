import sys
import os

# Agregar la ruta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
import tempfile
from summary_text.summary_text import generate_summary
from summary_text.utils.summary_text_functions_helper import load_file
from summary_text.utils.file_handler import make_summary_downloadable
from summary_text.utils.language_service import fetch_and_validate_languages

st.title("Resumen de Textos con Llama3")

# Abrir el selector de archivos
archivo = st.file_uploader("Sube un archivo", type=["pdf", "docx", "txt"])

if "idiomas" not in st.session_state:
    st.session_state.idiomas = None  # La lista de idiomas inicia como None
if "idioma_seleccionado" not in st.session_state:
    st.session_state.idioma_seleccionado = None  # Idioma seleccionado inicia vacío


if archivo:
    # Comprobar que el nombre del archivo tenga una extensión compatible
    if archivo.name.endswith((".pdf", ".docx", ".txt")):
        st.write("Procesando archivo...")
        try:
            # Crear archivo temporal con tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=archivo.name) as temp_file:
                temp_file.write(archivo.read())  # Guardar contenido en el archivo temporal
                temp_path = temp_file.name  # Obtener la ruta del archivo temporal

            # Procesar el archivo con load_file
            documentos = load_file(temp_path)

            if not documentos or len(documentos) == 0:
                st.warning("El documento está vacío o no se pudo procesar.")
            else:
                try:
                    # Obtener y validar los idiomas desde el modelo
                    idiomas = fetch_and_validate_languages()

                    # Usar los idiomas en el selectbox si están disponibles
                    if idiomas:
                        idioma_seleccionado = st.selectbox(
                            "Elige el idioma del resumen",
                            options=list(idiomas.keys()),
                            key="idioma_seleccionado"
                        )
                        idioma_destino = idiomas.get(idioma_seleccionado)

                        # Mostrar idioma seleccionado como confirmación
                        st.write(f"Has seleccionado el idioma: {idioma_seleccionado} (Código: {idioma_destino})")

                except Exception as e:
                    # Manejar errores durante la carga de idiomas
                    st.error("Error al obtener la lista de idiomas soportados.")
                    st.error(f"Detalles del error: {e}")

                    # Cargar opciones predeterminadas si ocurre un error
                    if st.session_state.idiomas is None:
                        st.session_state.idiomas = {"Español": "es", "Inglés": "en"}  # Idiomas básicos
                    idioma_seleccionado = st.selectbox(
                        "Elige el idioma del resumen (opciones predeterminadas)",
                        list(st.session_state.idiomas.keys()),
                        key="idioma_seleccionado"
                    )
                    idioma_destino = st.session_state.idiomas.get(idioma_seleccionado)

                    # Mostrar opciones elegidas por defecto
                    st.write(f"Idioma predeterminado seleccionado: {idioma_seleccionado} (Código: {idioma_destino})")

                # Seleccionar nivel de resumen
                niveles = {"Resumen breve": "brief",
                           "Resumen intermedio": "intermediate",
                           "Resumen detallado": "detailed"}

                nivel_seleccionado = st.selectbox("Elige el nivel de resumen",
                                                  list(niveles.keys()))

                # Generar resumen
                if st.button("Generar resumen"):

                    # Llamar a la función generate_summary con nivel e idioma
                    resumen = generate_summary(documentos, level=niveles[nivel_seleccionado],
                                               language=idiomas[idioma_seleccionado])

                    # Mostrar el resumen generado
                    st.subheader("Resumen generado:")
                    st.write(resumen.content)

                    # Hacer el resumen descargable
                    resumen_txt = resumen.content  # Extraer el texto del resumen

                    # Descargar el resumen
                    make_summary_downloadable(summary_text=resumen_txt)


        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

        finally:
            # Eliminar el archivo temporal después de procesarlo
            if os.path.exists(temp_path):
                os.remove(temp_path)  # Limpieza manual del archivo temporal
    else:
        st.warning("El tipo de archivo subido no es compatible. Por favor, suba un archivo PDF, DOCX o TXT.")
else:
    st.warning("No se subió ningún archivo.")



# streamlit run C:\Users\jhonh\PycharmProjects\langchain-projects\summary_text\streamlit_app\streamlit_interface.py
#    En Windows (PowerShell)
#    $env:PYTHONPATH="C:\Users\jhonh\PycharmProjects\langchain-projects"
#
