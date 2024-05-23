import streamlit as st

from llm_chat.chat.chat_router import ChatRouter
from llm_chat.streamlit.display_container import DisplayContainer

st.set_page_config(page_title="Ask me anything", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.write("Extra Parameters")
    option = st.selectbox("LLM Model?", ("GPT3.5", "GPT4", "GPT4o"))




st.title("Ask Anything")
# with st.chat_message("user"):
with st.container(border=True):
    st.write("Examples: \n")
    st.write("\tHere you write you example of commands the user can use\n")

# Initialize chat history

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], DisplayContainer):
            d = message["content"].get_display()
            if d:
                st.markdown(d)
        elif isinstance(message["content"], tuple):
            for item in message["content"]:
                st.markdown(item)
        else:
            st.markdown(message["content"])

st.session_state.log = []


if prompt := st.chat_input("Say something"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(text="In progress"):
        my_bar = st.progress(0, text="In progress")
        my_bar.progress(1, text="Find Command")
        result = ChatRouter().route_request(prompt, my_bar)
        my_bar.empty()
        if not result:
            st.write(f"Unknown command for: {prompt}")
            st.session_state.messages.append({"role": "assistant", "content": f"Unknown command for: {prompt}"})


with st.expander("See log"):
    table = "<table style='margin: auto;'><tbody>"

    for log in st.session_state.log:
        table += f"<tr><td colspan=2>{log}</td></tr>"
    table += "</table></tbody>"

    st.markdown(table, unsafe_allow_html=True)

