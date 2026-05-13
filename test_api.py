import requests
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("SUNBIRD_API_TOKEN")

response = requests.post(
    "https://api.sunbird.ai/tasks/summarise",
    json={"text": "Hey, I'm Bill. How re you doin"},
    headers={"Authorization": f"Bearer {token}"}
)

print(response.status_code)
print(response.json())