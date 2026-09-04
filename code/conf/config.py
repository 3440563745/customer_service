from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path
ENV_FILE=Path(__file__).parent.parent.parent/".env"
# print(ENV_FILE)
class Settings(BaseSettings):
    #llm
    llm_model:str
    llm_base_url:str
    llm_api_key:str
    #commerce api base
    commerce_api_base_url:str
    #database_url
    database_url:str
    #app
    app_host:str
    app_port:int
    model_config=SettingsConfigDict(env_file=ENV_FILE)
settings=Settings()  #在python中是一个单例对象，
#虽然python各个模块可能多次加载这一个模块，但是模块只会存在一份，
#那么settings对象就只有一份，就是单例对象

if __name__=="__main__":
    print(settings.llm_model)
    print(settings.llm_base_url)
    print(settings.llm_api_key)
    print(settings.commerce_api_base_url)
    print(settings.database_url)
    print(settings.app_host)
    print(settings.app_port)
    print(settings.model_config)

