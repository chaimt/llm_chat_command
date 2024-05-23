import json
import logging

from langchain.prompts import ChatPromptTemplate

from llm_chat.chat.chat_commands import available_commands
from llm_chat.chat.chat_flow import DebugLevel
from llm_chat.config import MyConfig
from llm_chat.helper.single_instance_metaclass import SingleInstanceMetaClass

logger = logging.getLogger(__name__)


class ChatRouter(metaclass=SingleInstanceMetaClass):
    classification = """Given the user question below

    respond with a json of the following format:
    {{
        "command_name": COMMAND_NAME,    
        "args": [LIST_OF_ARGS]    
        "debug": yes or no
        "trace": yes or no
    }}
    Do not add any extra information to the response, it should include only a json value object.
    
    The command_name should be either {list_of_commands}, or `Other`.
    {command_descriptions}
    If the word debug is in the text, the debug should be set to yes, otherwise no.
    If the user requests for more information, the debug should be set to yes.
    If the word trace is in the text, the trace should be set to yes, otherwise no.
    If the user requests for as much information as possible, the trace should be set to yes.

    <question>
    {question}
    </question>
    """

    def __init__(self):
        self.supported_commands = {c.name(): c for c in available_commands}
        list_of_commands = [f"'{c}'" for c in self.supported_commands.keys()]
        self.list_of_commands = ", ".join(list_of_commands)
        prompts = []
        for command in self.supported_commands.values():
            prompt = f"""
            In the case of the command {command.name()}, {command.llm_descriptor()}.
            Examples for the command {command.name()} are: {", ".join(command.examples())}
            """
            prompts.append(prompt)
        self.command_descriptions = "\n".join(prompts)

    def get_command(self, question: str) -> dict:
        prompt = ChatPromptTemplate.from_template(template=ChatRouter.classification)
        messages = prompt.format_messages(question=question, list_of_commands=self.list_of_commands, command_descriptions=self.command_descriptions)
        response = MyConfig().chat_llm_4(messages)
        return json.loads(response.content)

    def route_request(self, msg, my_bar) -> bool:
        command = self.get_command(msg)
        command_name = command["command_name"]
        debug = command["debug"]
        trace = command["trace"]
        arguments = command["args"]
        debug_level = DebugLevel.Info
        if debug == "yes":
            # await cl.Message(content="Running in debug mode").send()
            debug_level = DebugLevel.Debug
        if trace == "yes":
            # await cl.Message(content=f"Command is: {command_name}").send()
            debug_level = DebugLevel.Trace
        if command_name in self.supported_commands:
            my_bar.progress(2, text="Running Command: " + command_name)
            return self.supported_commands[command_name](arguments, debug_level).execute(my_bar)
        return False


# if __name__ == "__main__":
#     ChatRouter().get_command("list files from storage")
