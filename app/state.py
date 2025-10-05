import os
from typing import TypedDict, Literal, Optional
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI


class state(TypedDict):
    parts:list[str]
    action:Literal["add_part", "summarize_all"]
    new_parts:Optional[str]
    style:Optional[str]
    sentence:Optional[str]
    summary:Optional[str]
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
sum_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant that writes faithful, neutral summaries."),
    ("human", "Summarize the following combined text in {style} style, ~{sentence} sentence.\n\nTEXT:\n{all_text}")
])