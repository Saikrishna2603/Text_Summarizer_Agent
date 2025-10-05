import os
from typing import TypedDict, Literal, Optional
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI


class state(TypedDict):
    parts:list[str]
    action:Literal["add_part", "summarize_all"]
    new_part:Optional[str]
    style:Optional[str]
    sentence:Optional[str]
    summary:Optional[str]

    #Handeling Large Inputs
    chunk_size:Optional[str]
    chunk_overlap:Optional[str]
    map_sentences:Optional[str]
    reduce_sentences:Optional[str]

#Load .env file
load_dotenv()

# ---- Azure OpenAI config pulled from env ----
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
llm = AzureChatOpenAI(
    azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT,  # your Azure deployment name for gpt-4o
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0,
)

#This is for validating the prompt

MAP_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a faithful, neutral note-taker. Summarize this chunk accurately."),
    ("human",
     "Write a {style} summary of the CHUNK in about {sentences} sentences.\n\nCHUNK:\n{chunk}")
])

REDUCE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a concise synthesizer that merges multiple summaries into one cohesive whole."),
    ("human",
     "Combine the following bullet summaries into a single {style} summary of ~{sentences} sentences.\n\n"
     "BULLET SUMMARIES:\n{bullets}")
])