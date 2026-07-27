from embedding import create_embedding


text = "Complete AI internship assignment"

vector = create_embedding(text)

print(vector)
print("Vector length:", len(vector))