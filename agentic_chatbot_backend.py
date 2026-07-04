from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
load_dotenv()
"""
#llm = ChatGoogleGenerativeAI(
   # model="gemini-2.5-flash",
   # temperature=0,
)
"""
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
)

#Desfining state

from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
    
# defining nodes
def chat_node(state: ChatState):
    # take user query from the state
    messages = state["messages"]
    
    ## send to llm
    response = llm.invoke(messages)
    #response store state
    return {"messages":[response]}
    
    
checkpoint = MemorySaver()

graph = StateGraph(ChatState)

#Adding nodes

graph.add_node('chat_node',chat_node)

## Add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

#Compile the graph
chatbot = graph.compile(checkpointer=checkpoint)
