import os
from data_preprocessing import load_all_documents, chunk_text, load_xml_data_from_api
from search_engine import SearchEngine
from query_engine import generate_answer

if __name__ == "__main__":
    pdf_dir = os.path.join("data", "pdfs")
    doc_dir = os.path.join("data", "docs")
    index_path = os.path.join("data", "search_index.pkl")

    # XML API 예시 URL과 태그 경로(실제 환경에 맞게 수정)
    xml_api_url = "https://example.com/dental_insurance_data.xml"
    xml_text_tag_path = "./Documents/Document/Content"  # 예시 경로

    if not os.path.exists(index_path):
        # 로컬 문서 로딩
        docs_raw = load_all_documents(pdf_dir, doc_dir)

        # XML API 데이터 가져오기
        xml_doc = load_xml_data_from_api(xml_api_url, xml_text_tag_path)
        docs_raw.append(xml_doc)

        # 모든 문서 청크화
        chunked_docs = []
        for d in docs_raw:
            chunks = chunk_text(d["text"], chunk_size=1000, overlap=100)
            for i, c in enumerate(chunks):
                chunked_docs.append({
                    "filename": d["filename"],
                    "chunk_index": i,
                    "text": c
                })

        # TF-IDF 인덱스 생성
        se = SearchEngine()
        se.fit(chunked_docs)
        se.save(index_path)
    else:
        se = SearchEngine()
        se.load(index_path)

    # 테스트 질의
    query = "치과보험 청구 시 필요한 서류는 무엇인가요?"
    results = se.search(query, top_k=3)
    answer = generate_answer(query, results)
    print("질문:", query)
    print("답변:", answer)
