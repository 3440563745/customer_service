from langchain.chat_models import init_chat_model

from code.conf import config
from code.conf.config import settings

llm=init_chat_model(
    model=settings.llm_model,
    model_provider="openai",
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
    temperature=0,
)
if __name__ == "__main__":
    print(llm.invoke("你好，你是什么模型？").content)
    print(llm.invoke("你好"))