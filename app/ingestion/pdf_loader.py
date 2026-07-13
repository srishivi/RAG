from pypdf import PdfReader

def clean_text(text):
    return text.replace("\n", " ").strip()

def load_pdf(file_path: str):
    reader = PdfReader(file_path)

    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        text = clean_text(text)
        if text:  # avoid empty pages
            pages.append({
                "page_number": i + 1,
                "text": text
            })
    print("Pages", pages)
    return pages