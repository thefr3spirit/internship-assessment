---
title: Sunbird Translator
emoji: 🌍
colorFrom: yellow
colorTo: green
sdk: gradio
sdk_version: "5.29.1"
app_file: app.py
pinned: false
---

# Sunbird AI — Transcribe, Summarise, Translate & Speak

A Generative AI web application powered entirely by the [Sunbird AI API](https://docs.sunbird.ai/introduction). Users provide text or an audio file in English, and the app runs it through a full pipeline: transcription → summarisation → translation into a Ugandan local language → text-to-speech audio output.

---

## Architecture Overview

```
User Input
  ├── Text  ──────────────────────────────────────────┐
  └── Audio ──► /tasks/stt (Speech-to-Text) ──────────┤
                                                       ▼
                                        /tasks/summarise (Summarisation)
                                                       ▼
                                        /tasks/translate (Translation)
                                                       ▼
                                        /tasks/tts (Text-to-Speech)
                                                       ▼
                                 Transcript · Summary · Translation · Audio
```

| Step | Sunbird Endpoint | Description |
|---|---|---|
| Speech-to-Text | `POST /tasks/stt` | Transcribes uploaded/recorded audio to text |
| Summarisation | `POST /tasks/summarise` | Condenses text into a short summary |
| Translation | `POST /tasks/translate` | Translates summary into a Ugandan local language |
| Text-to-Speech | `POST /tasks/tts` | Generates spoken audio from the translated text |

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/thefr3spirit/internship-assessment.git
cd internship-assessment
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your Sunbird AI API token (see [Environment Variables](#environment-variables) below).

### 5. Run the app
```bash
python app.py
```
Open **http://127.0.0.1:7860** in your browser.

---

## Environment Variables

| Variable | Description |
|---|---|
| `SUNBIRD_API_TOKEN` | Your Sunbird AI API access token. Obtain one at [api.sunbird.ai](https://api.sunbird.ai/) |

See `.env.example` for the template.

---

## Usage

### Text Input

Type or paste English text, select a target language, and click **Run Pipeline**.

![Text input with "Hello, I need your help" entered and Ateso selected as target language](https://raw.githubusercontent.com/thefr3spirit/internship-assessment/main/docs/screenshots/text-input.jpg)

The app returns a summary, translated summary, and a playable audio clip of the translation.

![Results showing summary "I require assistance and would like to speak with you", Ateso translation, and audio player](https://raw.githubusercontent.com/thefr3spirit/internship-assessment/main/docs/screenshots/text-results.jpg)

---

### Audio Input

Switch to the **Audio Input** tab, upload an audio file or record via microphone, select a target language, and click **Run Pipeline**.

![Audio input tab with a 3-second audio file uploaded and Acholi selected](https://raw.githubusercontent.com/thefr3spirit/internship-assessment/main/docs/screenshots/audio-input.jpg)

The app transcribes the audio, summarises it, translates it, and generates speech.

![Results showing transcript "oli otya", summary "How are you?", Acholi translation "Itye nining?" and audio player](https://raw.githubusercontent.com/thefr3spirit/internship-assessment/main/docs/screenshots/audio-results.jpg)

---

## Deployed Link

**https://huggingface.co/spaces/thefr3spirit/sunbird-translator**

---

## Known Limitations

- **Processing time**: Each request makes 3–4 sequential API calls. Expect 30–200 seconds depending on input length and API load.
- **Audio duration**: Audio files longer than 5 minutes are rejected. The app enforces this before sending to the API.
- **Supported audio formats**: mp3, wav, ogg, m4a, aac, mp4, webm.
- **Summarisation languages**: The `/tasks/summarise` endpoint only supports English and Luganda input.
- **Translation target languages**: Luganda, Acholi, Ateso, Runyankole, Lugbara.
- **Internet required**: The app makes live calls to the Sunbird API — it does not work offline.
- **Free tier latency**: The Sunbird Free tier may experience cold starts on inference endpoints.

---

## Project Structure

```
internship-assessment/
├── app.py                        # Gradio UI entry point
├── backend/
│   ├── __init__.py
│   ├── sunbird_client.py         # Sunbird API wrapper (STT, summarise, translate, TTS)
│   ├── pipeline.py               # Orchestrates the full pipeline
│   ├── test_sunbird_client.py    # Manual tests for each API function
│   └── test_pipeline.py          # Manual end-to-end pipeline test
├── exercises/
│   └── basics.py                 # Part 1: collatz & distinct_numbers implementations
├── tests/
│   └── test_basics.py            # pytest tests for Part 1
├── docs/screenshots/             # UI screenshots for this README
├── requirements.txt
├── .env.example
└── constants.py
```

This assessment consists of 3 parts:
- Programming exercises.
- Build a simple command line app using the Sunbird AI API.

## Getting started
- Fork this repository to create your own copy. ([More info about forking a repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo))
- Clone your repository to access it locally: `git clone https://github.com/<your-username>/internship-assessment.git`. (Replace `<your-username>` with your Github username.)
- Change directory into the `internship-assessment` folder after cloning the repository.
- Create a python virtual environment: `python -m venv venv`
- Activate the virtual environment: 
  - Linux/Mac: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate.bat`
- Install the required python packages: `pip install -r requirements.txt`
- Run the command `pytest`. (The tests should be failing, it's your task to make them pass. See below for instructions)

## Part 1: Programming exercises
There are 2 programming exercises designed to test your competency with the python programming language. 

You can find the starter code and task descriptions in the `exercises/basics.py` file in this repo.

Run the following command: `pytest`. You will see that all the tests are failing.

Your goal is to implement the 2 functions `collatz` and `distinct_numbers` to make the above failing tests pass.

You can keep running the `pytest` command to see which tests are still failing and fix your code accordingly.

## Part 2: Build a GenAI Application with Sunbird AI

Build a small **Generative AI web application** powered by Sunbird AI's [Sunflower LLM](https://sunflower.sunbird.ai/) and the [Sunbird AI API](https://docs.sunbird.ai/introduction).

The application should let a user provide either **text** or an **audio file**, then run the input through this pipeline:

1. **Input** — accept either typed/pasted text **or** an uploaded audio file.
2. **Transcribe (audio only)** — if the input is audio, transcribe it to text using Sunbird's Speech-to-Text API.
3. **Summarise** — summarise the text (typed input or transcribed text) using the Sunflower LLM.
4. **Translate** — translate the summary into a chosen Ugandan local language (Luganda, Runyankole, Ateso, Lugbara, or Acholi) using the Sunflower LLM.
5. **Synthesise speech** — generate an audio clip of the translated summary using Sunbird's Text-to-Speech API.
6. **Output** — display the original text, the summary, the translated summary, and the generated audio (playable in the UI).

### Tech stack requirements

- **Backend:** Python (you may use FastAPI, Flask, or call the Sunbird API directly from your frontend framework — your choice).
- **Frontend:** one of [Gradio](https://www.gradio.app/), [Streamlit](https://streamlit.io/), or [Next.js](https://nextjs.org/docs).
- **APIs:** all AI capabilities **must** come from Sunbird AI. Do not call OpenAI, Anthropic, or any other model provider for the core pipeline.

### Sunbird AI API references

Read these docs carefully before implementing — they show the exact request/response shapes and authentication you'll need:

- **Speech-to-Text (STT):** https://docs.sunbird.ai/guides/speech-to-text
- **Text-to-Speech (TTS):** https://docs.sunbird.ai/guides/text-to-speech
- **Summarisation & Translation (Sunflower Simple Inference):** https://docs.sunbird.ai/guides/sunflower-chat
- **Full API reference:** https://docs.sunbird.ai/api-reference/introduction

You will need a Sunbird AI API token. Sign up and obtain one from the [Sunbird AI API portal](https://api.sunbird.ai/), then store it in a `.env` file as `SUNBIRD_API_TOKEN` (or equivalent). **Never commit your token to git.**

### Functional requirements

- Input switching: the UI must clearly let the user choose between text input and audio upload.
- Audio constraint: reject audio files longer than **5 minutes** with a clear error message.
- Language picker: allow the user to select the target local language for the translated summary.
- Visible intermediate results: the UI should show the transcript (when audio is used), the summary, the translated summary, and the generated audio player — not just the final audio.
- Sensible error handling: surface API failures to the user instead of silently failing.

### Suggested project layout

```
.
├── app.py                  # entry point (Gradio/Streamlit) OR Next.js app/
├── backend/
│   ├── sunbird_client.py   # thin wrapper around Sunbird API endpoints
│   ├── pipeline.py         # orchestrates STT -> summarise -> translate -> TTS
│   └── ...
├── requirements.txt        # or package.json if Next.js + Python backend
├── .env.example            # document required env vars (no real secrets)
└── README.md               # see Part 3
```

## Part 3: Documentation & Deployment

A working app you can't run isn't a working app. For this part, you must (a) document your project so a reviewer can run it locally, and (b) deploy it publicly so we can try it without setting anything up.

### README requirements

Replace this README (or add a `PROJECT_README.md` next to it) with documentation that includes:

- **Project description** — one paragraph on what the app does.
- **Architecture overview** — a short diagram or bullet list of the pipeline (input → STT → summarise → translate → TTS → output) and which Sunbird endpoints handle each step.
- **Local setup** — exact, copy-pasteable steps to clone, install dependencies, configure environment variables (with a `.env.example` reference), and run the app locally.
- **Environment variables** — list every required variable and what it does.
- **Usage** — a short walkthrough showing the app being used end-to-end (screenshots are encouraged).
- **Deployed link** — a public URL where reviewers can try the app.
- **Known limitations** — anything that doesn't work, or constraints (e.g. 5-minute audio cap, supported languages).

### Deployment

Deploy your app to a free hosting provider that fits your stack. Pick one:

#### Option A — Hugging Face Spaces (recommended for Gradio/Streamlit)

1. Create a free account at https://huggingface.co/join.
2. Create a new Space: https://huggingface.co/new-space — choose **Gradio** or **Streamlit** as the SDK and a public visibility.
3. Add your Sunbird API token as a Space secret: Space settings → **Variables and secrets** → **New secret** → name it `SUNBIRD_API_TOKEN`.
4. Push your code to the Space's git repo:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/<your-space-name>
   git push space main
   ```
5. Hugging Face will build and deploy automatically. Confirm your `requirements.txt` lists every Python dependency and that your entry file matches the SDK convention (`app.py` for both Gradio and Streamlit).

Reference: https://huggingface.co/docs/hub/spaces-overview

#### Option B — Vercel (recommended for Next.js + Python backend)

1. Create a free account at https://vercel.com/signup and install the CLI: `npm i -g vercel@latest`.
2. From your project root, link the project: `vercel link`.
3. Add your Sunbird API token as an environment variable for all environments:
   ```bash
   vercel env add SUNBIRD_API_TOKEN
   ```
   (You'll be prompted to select Development, Preview, and Production — select all that apply.)
4. Pull the env vars locally for development: `vercel env pull .env.local`.
5. Deploy:
   - Preview: `vercel`
   - Production: `vercel --prod`
6. If you have a Python backend (FastAPI/Flask), put it under an `api/` directory or a separate Python service — Vercel runs Python via Fluid Compute. See https://vercel.com/docs/functions/runtimes/python.

Reference: https://vercel.com/docs/getting-started-with-vercel

### Submission

Your final submission must include:

- A pull request (or repository link) with all your code.
- An updated README that meets the requirements above.
- **A working deployed link** that we can open and use end-to-end with at least one test input.

