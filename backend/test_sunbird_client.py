import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import sunbird_client

print("=== summarise ===")
result = sunbird_client.summarise(
    "Hey, Bill testin here"
)
print("Result:", result)
print()



print("=== translate ===")
result = sunbird_client.translate("Hello, how are you?", "Acholi")
print("Result:", result)
print()



print("=== text_to_speech ===")
result = sunbird_client.text_to_speech("Oli otya?", "Luganda")
print("Result:", result)
print()



print("=== transcribe ===")
result = sunbird_client.transcribe("C:\\Users\\HP\Downloads\\20260513113503_1a5c2e8e-cfc7-46b8-8d9f-df3e2f2c5b1f.mp3")
print("Result:", result)