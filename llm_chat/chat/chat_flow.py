import logging
from abc import ABC
from enum import Enum
from typing import Dict, Union

logger = logging.getLogger(__name__)


class DebugLevel(Enum):
    Error = 40
    Warn = 30
    Info = 20
    Debug = 10
    Trace = 0

    @classmethod
    def from_str(cls, value):
        for enum_value in cls:
            if enum_value.name == value:
                return enum_value
        raise NotImplementedError()


class Action:
    name: str
    value: str
    label: str


class ChatFlow(ABC):
    def __init__(self, debug_level: DebugLevel = DebugLevel.Info):
        self.debug_level = debug_level

    def _display_user_content(self, title: str, content: Union[Dict, str], debug_level: DebugLevel = DebugLevel.Info) -> bool:
        pass

    def show_user_content(self, title: str, content: Union[Dict, str], debug_level: DebugLevel = DebugLevel.Info) -> bool:
        if self.debug_level.value <= debug_level.value:
            self._display_user_content(title, content, debug_level)

    def ask_user(self, question: str) -> str:
        pass

    def ask_action(self, question: str, actions: list[Action]) -> str:
        pass


class LogChatFlow(ChatFlow):
    def _display_user_content(self, title: str, content: Union[Dict, str], debug_level: DebugLevel = DebugLevel.Info) -> bool:
        match debug_level:
            case DebugLevel.Warn:
                logger.warning(f"{title} - {content}")
            case DebugLevel.Info:
                logger.info(f"{title} - {content}")
            case DebugLevel.Debug | DebugLevel.Trace:
                logger.debug(f"{title} - {content}")
        return True

    def ask_user(self, question: str) -> str:
        return input(question + "\n")

    def ask_action(self, question: str, actions: list[Action]) -> str:
        return input(question + "\n")


class VoidChatFlow(ChatFlow):
    def _display_user_content(self, title: str, content: Union[Dict, str], debug_level: DebugLevel = DebugLevel.Info) -> bool:
        return False

    def ask_user(self, question: str) -> str:
        return ""

    def ask_action(self, question: str, actions: list[Action]) -> str:
        return ""
