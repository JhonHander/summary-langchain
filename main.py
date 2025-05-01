import os
from summary_text import summary_text
from utils.summary_text_functions_helper import load_file, save_summary_to_file
from summary_text.summary_text import generate_summary

def main():
    """
    Permite al usuario seleccionar un documento y un nivel de resumen,
    y genera un resumen basado en esas selecciones.
    """
    # Mostrar documentos disponibles en la carpeta actual
    folder_path = os.path.join(os.path.dirname(__file__), "summary_inputs")  # Carpeta @summary_inputs
    document_files = [
        file for file in os.listdir(folder_path)
        if file.endswith((".txt", ".pdf", ".docx"))
    ]

    if not document_files:
        print("No hay documentos compatibles en esta carpeta.")
        return

    print("Documentos disponibles:")
    for i, file in enumerate(document_files, start=1):
        print(f"{i}. {file}")

    # Seleccionar un archivo
    try:
        file_choice = int(input("Elige un documento (número): "))
        file_path = os.path.join(folder_path, document_files[file_choice - 1])
    except (ValueError, IndexError):
        print("Opción inválida.")
        return

    # Seleccionar el nivel de resumen
    print("\nElige el nivel de resumen:")
    levels = {"1": "brief", "2": "intermediate", "3": "detailed"}
    print("1. Resumen breve (1-2 frases)")
    print("2. Resumen intermedio (3-5 frases)")
    print("3. Resumen detallado (párrafo completo)")

    level_choice = input("Selecciona el nivel (1-3): ")
    if level_choice not in levels:
        print("Opción de nivel inválida.")
        return

    # Cargar el archivo seleccionado
    try:
        documents = load_file(file_path)
    except ValueError as e:
        print(f"Error al cargar el archivo: {e}")
        return

    if not documents or len(documents) == 0:
        print("El documento está vacío o no se pudo procesar.")
        return

    summary_level = levels[level_choice]
    summary = generate_summary(documents, level=summary_level)

    # Guardar el resumen en un archivo único basado en el nombre del documento y fecha/hora
    save_summary_to_file(summary.content, file_path)

if __name__ == "__main__":
    main()