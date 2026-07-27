from embedding import create_embedding
from chroma_db import add_to_vectorstore, search_vectorstore


# Sample task/note
text = "Complete AI internship assignment"


# Create embedding
vector = create_embedding(text)


# Store in ChromaDB
add_to_vectorstore(
    id="task_1",
    text=text,
    embedding=vector
)

print("Data stored successfully!")


# Search similar data
query = "What is my AI work?"

query_vector = create_embedding(query)


results = search_vectorstore(query_vector)


print(results)