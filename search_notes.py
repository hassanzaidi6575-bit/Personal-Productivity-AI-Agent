from app.vectorstore.search import semantic_search


def search_notes(
    query,
    category=None,
    date_range=None
):

    results = semantic_search(query)


    return {

        "query": query,

        "category": category,

        "date_range": date_range,

        "results": results,

        "message": "Relevant notes retrieved successfully"

    }