from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3",
    base_url="http://ollama:11434"
)
