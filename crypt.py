import json


with open("alice.pub") as public_key_file:
    public_key = json.load(public_key_file)
    print(public_key)
