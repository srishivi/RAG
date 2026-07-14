import os
from typing import List, Dict
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("AZURE_DOC_INTELLIGENCE_ENDPOINT")
KEY = os.getenv("AZURE_DOC_INTELLIGENCE_KEY")

client = DocumentAnalysisClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)


def clean_text(text: str) -> str:
    return text.replace("\n", " ").strip()


def load_pdf(file_path: str) -> List[Dict]:
    print(f"\n📄 Processing with Azure DI: {file_path}")

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-layout",
            document=f
        )

    result = poller.result()

    pages = []

    for page in result.pages:
        lines = []

        for line in page.lines:
            lines.append(line.content)

        text = " ".join(lines)
        text = clean_text(text)

        if text.strip():
            pages.append({
                "page_number": page.page_number,
                "text": text
            })

    if len(pages) == 0:
        raise ValueError("❌ No text extracted from document")

    # ✅ Add source metadata
    file_name = os.path.basename(file_path)
    for page in pages:
        page["source"] = file_name

    print(f"✅ Extracted {len(pages)} pages using Azure DI")

    return pages





# from pypdf import PdfReader

# def clean_text(text):
#     return text.replace("\n", " ").strip()

# def load_pdf(file_path: str):
#     reader = PdfReader(file_path)

#     pages = []
#     for i, page in enumerate(reader.pages):
#         text = page.extract_text()
#         print(f"Page {i+1} raw text:", text)
#         text = clean_text(text)
#         if text:  # avoid empty pages
#             pages.append({
#                 "page_number": i + 1,
#                 "text": text
#             })
#     print("Pages", pages)
#     return pages