from flask import Flask, request, jsonify
import os
from search_engine import SearchEngine
from query_engine import generate_answer

app = Flask(__name__)

# API 키 및 검색엔진 로드
index_path = os.path.join("data", "search_index.pkl")
se = SearchEngine()
se.load(index_path)

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "Dental API is running!"})

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    # 검색 및 답변 생성
    results = se.search(user_query, top_k=3)
    answer = generate_answer(user_query, results)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
