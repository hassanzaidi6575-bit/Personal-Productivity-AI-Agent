from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text):
    """
    Convert text into numerical vector
    """
    embedding = model.encode(text)
    return embedding