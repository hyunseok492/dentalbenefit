import os
import docx
import PyPDF2
import requests
import xml.etree.ElementTree as ET

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text

def load_all_documents(pdf_dir, doc_dir):
    docs = []
    # PDF 처리
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            docs.append({"filename": pdf_file, "text": text})
    # DOCX 처리
    for doc_file in os.listdir(doc_dir):
        if doc_file.endswith(".docx"):
            doc_path = os.path.join(doc_dir, doc_file)
            text = extract_text_from_docx(doc_path)
            docs.append({"filename": doc_file, "text": text})
    return docs

def chunk_text(text, chunk_size=1000, overlap=30):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            break
        if start >= text_length:
            break
    return chunks

def load_xml_data_from_api(url, xml_text_tag_path):
    """
    XML API 호출 후 특정 태그의 텍스트 수집 예시
    url: XML 데이터를 반환하는 API 엔드포인트
    xml_text_tag_path: 추출할 텍스트 태그 경로 (예: "./Root/Body/Paragraph")

    반환값: {"filename": "api_data.xml", "text": "추출된 텍스트 ..."}
    """
    response = requests.get(url)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    # 예: 특정 노드들의 텍스트를 모두 모음
    texts = []
    for elem in root.findall(xml_text_tag_path):
        if elem.text:
            texts.append(elem.text.strip())
    combined_text = "\n".join(texts)

    return {"filename": "api_data.xml", "text": combined_text}
