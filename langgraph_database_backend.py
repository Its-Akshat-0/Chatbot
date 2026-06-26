from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import TypedDict, Literal,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import sqlite3
import operator
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()

api_key=os.getenv("GROQ_API_KEY")
llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key
)

from langgraph.graph.message import add_messages
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
    
def chat_node(state: ChatState) -> Literal['chat_node']:
    message=state['messages']
    response=llm.invoke(message)
    
    return {'messages': [response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)
graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)
def  retrieve_all_threads():
    
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)