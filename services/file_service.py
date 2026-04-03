from services.extractors.pdf_extractor import extract_pdf
from services.extractors.docx_extractor import extract_docx
from services.extractors.txt_extractor import extract_txt

class FileProcessingError(Exception):
    pass

EXTRACTORS = {
    "pdf": extract_pdf,
    "docx": extract_docx,
    "txt": extract_txt,
}

def extract_text_from_file(file_path: str, file_type: str) -> str:
    extractor = EXTRACTORS.get(file_type)

    if not extractor:
        raise FileProcessingError("❌ Неподдерживаемый формат файла")

    try:
        text = extractor(file_path)

        if not text:
            raise FileProcessingError("❌ Файл не содержит текста")

        return text

    except RuntimeError as e:
        raise FileProcessingError(str(e))