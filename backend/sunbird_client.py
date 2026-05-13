#sunbird_client.py
#This file talks to the Sunbird ai api, and provides functions for other files to import
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SUNBIRD_API_TOKEN")

#base url for all sunbird api endpoints
BASE_URL = "https://api.sunbird.ai"

#speaker IDs for the languages, the TTS API
SPEAKER_IDS = {
    "Acholi": 241,
    "Ateso": 242,
    "Runyankole": 243,
    "Lugbara": 245,
    "Luganda": 248,
}

#codes for the languages, for the translate API
LANGUAGE_CODES = {
    "Acholi": 'ach',
    "Ateso": 'teo',
    "Runyankole": 'nyn',
    "Lugbara": 'lgg',
    "Luganda": 'lug',
}

def _headers() -> dict:
    #returns the authorization header required by every sunbird api
    return {"Authorization": f"Bearer {TOKEN}"}

def transcribe(audio_file_path: str) -> str:
    """
    sends an audio file to STT API
    Returns transcribed text as a plin string
    """
    #open audio file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        #send a POST request
        response = requests.post(
            f"{BASE_URL}/tasks/stt",
            files={"audio": (os.path.basename(audio_file_path), audio_file, "audio/mpeg")},
            headers=_headers()
        )
    #check for server errors
    response.raise_for_status()
    return response.json()["audio_transcription"]


def summarise(text: str) -> str:
    """
    Sends text to sunbird's summarization endpoint
    returns the summary as a plain string
    """
    response = requests.post(
        f"{BASE_URL}/tasks/summarise",
        json={"text": text},
        headers=_headers()
    )
    response.raise_for_status()
    return response.json()["summarized_text"]


def translate(text: str, target_language: str) -> str:
    """
    Transltes text from English to local languages
    returns translated text as plain string
    """
    response = requests.post(
        f"{BASE_URL}/tasks/translate",
        json={
            "text": text,
            "source_language": "eng",
            "target_language": LANGUAGE_CODES[target_language],
        },
        headers= _headers()
    )
    response.raise_for_status()
    return response.json()["output"]["translated_text"]


def text_to_speech(text: str, language: str) -> str:
    """
    Converts text to speech using sunbird's Text-to-Speech API
    returns a temporary URL pointing to the generated audio file"""
    response = requests.post(
        f"{BASE_URL}/tasks/tts",
        json={
            "text": text,
            "speaker_id": SPEAKER_IDS[language],
        },
        headers=_headers()
    )
    response.raise_for_status()
    return response.json()["output"]["audio_url"]