import fitz  # PyMuPDF

def extract_pdf(file_path: str) -> str:
    text_parts = []

    try:
        doc = fitz.open(file_path)

        for page in doc:
            text = page.get_text("text")
            if text.strip():
                text_parts.append(text)

        full_text = "\n".join(text_parts).strip()

        return full_text

    except Exception as e:
        raise RuntimeError(f"Ошибка чтения PDF: {e}")