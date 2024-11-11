from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from os import getenv

OLLAMA_URL = getenv("OLLAMA_URL")

llm = OllamaLLM(base_url=OLLAMA_URL, model="phi3:latest")
embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model="nomic-embed-text")

if __name__ == "__main__":
    print(len(embeddings.embed_query("Hi")))
    print(llm.invoke("Hi"))