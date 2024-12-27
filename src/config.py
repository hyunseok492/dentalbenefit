from dotenv import load_dotenv
import os

# 환경변수 혹은 직접 입력
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"  # 혹은 원하는 모델명
EMBEDDING_MODEL = "text-embedding-ada-002"
XML_API_KEY = os.environ.get("XML_API_KEY")
XML_API_URL = os.environ.get("XML_API_URL")
XML_API_URL = "http://apis.data.go.kr/B551182/NdrgStdInfoService"
XML_API_URL = "http://apis.data.go.kr/B551182/drgSeparateCompensationItemListService1"
