import json

with open('data.json', 'r') as f:
    data = json.loads("".join(f.readlines()).replace("\n", ""))

print("Jobs with not been executed for 3 month")

for k, v in data.items():
    v['index.json']['']

print("jobs had been disabled")
