from app.vectorstore.chroma_db import collection
from app.vectorstore.embedding import create_embedding



def semantic_search(query, limit=3):


    query_embedding = create_embedding(query)


    query_filter = None


    # Detect if user wants notes
    if "note" in query.lower():

        query_filter = {
            "type": "note"
        }


    # Detect if user wants tasks
    elif "task" in query.lower():

        query_filter = {
            "type": "task"
        }



    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        where=query_filter
    )



    documents = results.get(
        "documents",
        [[]]
    )[0]



    if not documents:

        return "No relevant information found."



    return "\n\n".join(documents)