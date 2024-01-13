import meilisearch
import json
client = meilisearch.Client('https://edge.meilisearch.com', 'bc61b7bb01eb45353ed231d2f88750729ddbbac9')

# An index is where the documents are stored.

# json_file = open('new_file.json', encoding='utf-8')
# movies = json.load(json_file)
# client.index('test').add_documents(movies)

result = client.index("test").search(
    "Khai mạc lễ hội tết việt quý mão 2023",{"limit": 3}
)["hits"]
print(result)