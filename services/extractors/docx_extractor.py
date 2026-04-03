from docx import Document

def extract_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text_parts = [p.text for p in doc.paragraphs if p.text.strip()]

        return "\n".join(text_parts).strip()

    except Exception as e:
        raise RuntimeError(f"Ошибка чтения DOCX: {e}")