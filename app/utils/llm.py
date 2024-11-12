from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from os import getenv

PROVIDER = getenv("LLM_PROVIDER")
OLLAMA_URL = getenv("OLLAMA_URL")

if PROVIDER == "ollama":
    llm = OllamaLLM(base_url=OLLAMA_URL, model="phi3:latest")
    embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model="nomic-embed-text")
    
elif PROVIDER == "gemini":
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        api_key=getenv("GOOGLE_API_KEY"),
        temperature=0,
        max_tokens=100,
        timeout=None,
        max_retries=2,
    )

if __name__ == "__main__":
    # print(len(embeddings.embed_query("Hi")))
    print(llm.invoke("Hi"))