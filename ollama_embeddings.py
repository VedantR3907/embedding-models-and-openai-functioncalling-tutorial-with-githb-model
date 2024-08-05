from langchain_ollama import OllamaEmbeddings
import asyncio

embeddings = OllamaEmbeddings(model="llama3.1")

async def generate_embeddings():
    emd = await embeddings.aembed_documents(
        ["This is a content of the document", "This is another document"]
    )

    print(len(emd[0]))

asyncio.run(generate_embeddings())