from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

embeddings = FastEmbedEmbeddings()

document_embeddings = embeddings.embed_documents(
    ["This is a document", "This is some other document"]
)

print(document_embeddings)


query_embeddings = embeddings.embed_query("This is a query")
print("*"*10)
print(query_embeddings)