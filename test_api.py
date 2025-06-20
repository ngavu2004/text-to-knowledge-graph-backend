# test_api.py
import requests
import json

# Test the API
url = "http://localhost:8001/extract-kg"
data = {
    "text": "John works at Google. Google is a technology company founded by Larry Page and Sergey Brin.",
    "chunk_size": 1000,
    "chunk_overlap": 100
}

response = requests.post(url, json=data)
result = response.json()

print("Result:", json.dumps(result, indent=2))
print("Nodes:", len(result["nodes"]))
print("Relationships:", len(result["relationships"]))
print("Chunks processed:", result["chunks_processed"])