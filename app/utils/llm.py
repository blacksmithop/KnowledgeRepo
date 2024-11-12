from os import getenv

PROVIDER = getenv("LLM_PROVIDER")
OLLAMA_URL = getenv("OLLAMA_URL")

if PROVIDER == "ollama":
    from langchain_ollama.embeddings import OllamaEmbeddings
    from langchain_ollama.llms import OllamaLLM

    llm = OllamaLLM(base_url=OLLAMA_URL, model="phi3:latest")
    embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model="nomic-embed-text")

elif PROVIDER == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_huggingface import HuggingFaceEmbeddings

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        api_key=getenv("GOOGLE_API_KEY"),
        temperature=0,
        max_tokens=100,
        timeout=None,
        max_retries=2,
    )

    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

# if __name__ == "__main__":
#     print(len(embeddings.embed_query("Hi")))
#     print(llm.invoke("Hi"))
