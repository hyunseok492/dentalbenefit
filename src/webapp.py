from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS 추가
import os
from search_engine import SearchEngine
from query_engine import generate_answer

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 CORS 허용

# OpenAI API 키 환경변수에서 가져오기
openai_api_key = os.environ.get("OPENAI_API_KEY")

# 검색 엔진 초기화
index_path = os.path.join("data", "search_index.pkl")
search_engine = SearchEngine()
search_engine.load(index_path)

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "Dental API is running!"})

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # 검색 및 답변 생성
    results = search_engine.search(user_query, top_k=3)
    answer = generate_answer(user_query, results)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
