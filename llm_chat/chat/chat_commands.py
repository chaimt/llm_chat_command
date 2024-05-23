import logging

import streamlit as st

from llm_chat.chat.chat_flow import DebugLevel
from llm_chat.chat.commands.base_command import ChatCommand
from llm_chat.chat.commands.sample_graph import SampleGraphCommand

logger = logging.getLogger(__name__)


class ListAvailableCommand(ChatCommand):
    @classmethod
    def name(cls):
        return "available_commands"

    @classmethod
    def llm_descriptor(cls) -> str:
        return "In the case of available_commands there will be no LIST_OF_ARGS."

    @classmethod
    def examples(cls) -> list[str]:
        return ["list available commands", "show commands", "list commands", "show help"]

    def execute(self, my_bar) -> bool:
        commands = {}
        if self.debug_level == DebugLevel.Debug:
            for command in available_commands:
                commands[command.name()] = {}
                commands[command.name()]["examples"] = command.examples()
                commands[command.name()]["expected_params"] = command.expected_params()
                commands[command.name()]["llm_descriptor"] = command.llm_descriptor()
        else:
            for command in available_commands:
                commands[command.name()] = {}
                commands[command.name()]["examples"] = command.examples()
                commands[command.name()]["expected_params"] = command.expected_params()
        st.json(commands)
        # await cl.Message(content=commands).send()
        return True


available_commands = [
    ListAvailableCommand,
    SampleGraphCommand,
]
