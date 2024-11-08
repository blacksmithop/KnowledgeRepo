from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from app import llm

template = """
You are a helpful chatbot. Answer these questions to the best of your understanding
Query: {query}
Response:
"""

prompt = PromptTemplate(
    input_variables=["query"], template=template
)

chat_chain = prompt | llm | StrOutputParser()

# TODO: Use Agent with Tools!