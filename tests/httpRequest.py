import requests
import json

URL = "http://localhost:8000"


def get(resource: str):
    response = requests.get(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"})
    return response

def post(resource: str, data: {}):
    response = requests.post(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response
def delete(resource: str):
    response = requests.delete(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"})
    return response