from abc import ABC, abstractmethod

from llm_chat.chat.chat_flow import DebugLevel


class ChatCommand(ABC):
    def __init__(self, args, debug_level: DebugLevel = DebugLevel.Info):
        self.debug_level = debug_level
        self.args = args

    @classmethod
    def name(cls):
        return None

    @classmethod
    def examples(cls) -> list[str]:
        pass

    @classmethod
    def expected_params(cls) -> list[str]:
        pass

    @classmethod
    def llm_descriptor(cls) -> str:
        pass

    @abstractmethod
    async def execute(self, my_bar) -> bool:
        pass
