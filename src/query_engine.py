import openai
from config import OPENAI_API_KEY, OPENAI_MODEL
openai.api_key = OPENAI_API_KEY

def generate_answer(query, docs):
    # docs: [{"filename": ..., "chunk_index": ..., "text": ...}, ...]
    context_text = "\n\n".join([f"출처: {d['filename']} (chunk {d.get('chunk_index','N/A')})\n{d['text']}" for d in docs])

    prompt = f"""
당신은 전문 치과보험청구사입니다.
사용자 질문의 의도에 맞게 자료를 바탕으로 중복없이 요약하여 핵심적인 답변을 150자 이내로 부탁드립니다. 
데이터의 내용 출처는 절대 알리지말아주세요. 데이터 내의 정보가 없을 시 해당 질문은 답변하기 어렵다고 해주세요. 추측성 정보는 제공하지말아주세요.

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
