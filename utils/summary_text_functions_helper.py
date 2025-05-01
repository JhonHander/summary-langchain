import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime

def load_file(path):
    """
    Carga un archivo basado en su formato y retorna su contenido. Esta función soporta
    archivos con extensiones .txt, .pdf y .docx, utilizando cargadores apropiados para
    cada formato. Si el formato del archivo no es compatible, lanza un ValueError.

    :param path: La ruta del archivo que se desea cargar. Debe terminar en .txt, .pdf o .docx.
    :type path: str
    :raises ValueError: Si el formato del archivo no es compatible.
    :return: El contenido del archivo cargado por el cargador adecuado.
    :rtype: Any
    """
    if path.endswith(".txt"):
        loader = TextLoader(path)
    elif path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".docx"):
        loader = Docx2txtLoader(path)
    else:
        raise ValueError("Formato no soportado. Usa .txt, .pdf o .docx")

    docs = loader.load()
    return docs

def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_texts = splitter.split_documents(documents)
    return split_texts

def save_summary_to_file(summary_text, original_filename, output_folder="summary_outputs"):
    """
    Guarda el resumen generado en un archivo de texto dentro de la carpeta especificada.

    :param summary_text: El texto del resumen que se va a guardar.
    :param output_folder: La carpeta donde se guardará el archivo. Por defecto es @summary_outputs.
    """

    # Crear la carpeta si no existe
    output_path = os.path.join(os.path.dirname(__file__), output_folder)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Obtener la fecha y hora actual
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Formato: AñoMesDía_HoraMinutoSegundo

    # Obtener el nombre base del archivo original (sin extensión)
    file_base_name = os.path.splitext(os.path.basename(original_filename))[0]

    # Ruta del archivo de salida
    output_file_name = f"{file_base_name}_summary_{current_time}.txt"
    output_file = os.path.join(output_path, output_file_name)

    # Guardar el texto en el archivo
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(summary_text)

    print(f"Resumen guardado en: {output_file}")


# def generar_pdf(resumen):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, resumen)  # Agrega el texto del resumen al PDF
#     return pdf.output(dest="S").encode("latin1")  # Devuelve el PDF como bytes

