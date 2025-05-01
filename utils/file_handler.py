from tempfile import NamedTemporaryFile
import streamlit as st

def make_summary_downloadable(summary_text, filename="resumen.txt"):
    """
    Convierte un texto en descargable dentro de Streamlit.
    :param summary_text: Texto del resumen.
    :param filename: Nombre del archivo de descarga.
    """
    st.download_button(
        label="Descargar Resumen",
        data=summary_text,
        file_name=filename,
        mime="text/plain"
    )
