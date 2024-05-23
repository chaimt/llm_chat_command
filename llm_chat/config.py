import os
from datetime import datetime
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from llm_chat.helper.data_class import DataClassYAMLMixinNullRemoval
from llm_chat.helper.single_instance_metaclass import SingleInstanceMetaClass


_ = load_dotenv(dotenv_path=find_dotenv(), override=True)  # read local .env file


class ApplicationState(DataClassYAMLMixinNullRemoval, BaseModel):
    error_count: int = 0
    error_time: Optional[datetime] = None


class MyConfig(metaclass=SingleInstanceMetaClass):
    def __init__(self):
        self.init()

    def init(self):
        self.chat_llm_4_turbo = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.0, request_timeout=60, max_retries=2)
        self.chat_llm_4o = ChatOpenAI(model_name="gpt-4o", temperature=0.0, request_timeout=60, max_retries=2)
        self.chat_llm_4 = ChatOpenAI(model_name="gpt-4", temperature=0.0, request_timeout=60, max_retries=2)
        self.chat_llm_3 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.0, request_timeout=60, max_retries=2)
        self.chat_llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.0, request_timeout=60, max_retries=2)
        self.llm_openai = self.chat_llm_4o
        self.root = os.getcwd()

        self.debug_level = os.getenv("DEBUG_LEVEL", "INFO")
        self.llm_debug_level = os.getenv("LLM_DEBUG_LEVEL", "INFO")

        self.template_path = os.getenv("TEMPLATE_PATH", "/templates")

        self.enable_redis = os.getenv("ENABLE_REDIS", "True") == "True"
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))


        self.state = ApplicationState()


my_config = MyConfig()
