import chromadb


# Create ChromaDB client
client = chromadb.PersistentClient(
    path="chroma_storage"
)


# Create or load collection
collection = client.get_or_create_collection(
    name="productivity_memory"
)



def add_to_vectorstore(id, text, embedding, metadata):
    """
    Store text, embedding and metadata in ChromaDB
    """

    collection.add(
        ids=[id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )



def search_vectorstore(query_embedding, limit=3, filter_type=None):
    """
    Search similar information
    """

    query_filter = None


    if filter_type:

        query_filter = {
            "type": filter_type
        }


    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        where=query_filter
    )


    return results