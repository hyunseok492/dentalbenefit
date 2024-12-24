import openai
from config import OPENAI_API_KEY, OPENAI_MODEL
openai.api_key = OPENAI_API_KEY

def generate_answer(query, docs):
    # docs: [{"filename": ..., "chunk_index": ..., "text": ...}, ...]
    context_text = "\n\n".join([f"출처: {d['filename']} (chunk {d.get('chunk_index','N/A')})\n{d['text']}" for d in docs])

    prompt = f"""
당신은 전문 치과보험청구사입니다.
사용자의 질문에 맞게 이 자료를 바탕으로 질문에 중복없이 간결하고 핵심적인 답변만 부탁드립니다. 가독성 좋게 표로 보여줄 수 있으면 표로 보여주고, 출처는 밝히지 말아주세요.

질문: {query}

참고 자료:
{context_text}

답변:
"""
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "당신은 전문 치과보험청구사입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
