import json

data = {
    "price": "3600",
    "status": "test_success"
}

with open('gold_data.json', 'w') as f:
    json.dump(data, f)

print("File Created Successfully!")
