import streamlit as st
from agentic_chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

st.title("Agentic Chatbot with LangGraph")

CONFIG = {
    "configurable": {
        "thread_id": "thread_1"
    }
}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# Display previous messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # Assistant message with streaming
    with st.chat_message("assistant"):

        placeholder = st.empty()
        ai_message = ""

        for event in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="values"
        ):
            if "messages" in event:
                ai_message = event["messages"][-1].content
                placeholder.markdown(ai_message)

    # Save final response
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )