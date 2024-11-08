from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings


llm = OllamaLLM(base_url="http://ollama.abhinavkm.com", model="phi3:latest")
embeddings = OllamaEmbeddings(base_url="http://ollama.abhinavkm.com", model="nomic-embed-text")

if __name__ == "__main__":
    print(len(embeddings.embed_query("Hi")))
    print(llm.invoke("Hi"))