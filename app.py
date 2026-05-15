#app.py
#Builds the UI and connescts to the pipeline. 
# Entry point of the web app

import gradio as gr
import requests
import tempfile
import os
from mutagen import File as MutagenFile  # reads audio metadata (duration, format) locally

from backend import pipeline

#Languages matching keys in SPEAKER_IDS and lANGUAGE_CODES
LANGUAGES = ['Acholi', 'Ateso', 'Luganda', 'Lugbara', 'Runyankole']


def check_audio_duration(audio_path: str) -> None:
    """
    Reads the audio file's metadata and raises a ValueError if it exceeds 5 minutes.
    This check runs LOCALLY before any API call is made — fast and cheap.
    Raises ValueError with a human-readable message so the caller can surface it in the UI.
    """
    audio = MutagenFile(audio_path)  # reads metadata from file header without decoding audio

    if audio is None:
        # mutagen returns None when it can't recognise the file format
        raise ValueError(
            "Could not read audio file. Please upload a supported format: mp3, wav, ogg, m4a, webm."
        )

    # audio.info.length is duration in seconds as a float
    duration_seconds = audio.info.length
    max_seconds = 5 * 60  # 5 minutes = 300 seconds

    if duration_seconds > max_seconds:
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        raise ValueError(
            f"Audio is too long ({minutes}m {seconds}s). Maximum allowed duration is 5 minutes."
        )


def process_text(text: str, language: str):
    """
    called by gradio when user inputs text
    Returns 4 values: Gradio maps them to the 4 output components in order"""
    try:
        # Validate input is not empty before calling the API
        if not text or not text.strip():
            raise ValueError("Please enter some text before running the pipeline.")

        result = pipeline.run(
            input_type='text',
            text_input=text,
            audio_path='',
            target_language=language
        )

        #download audio and return as a local path
        audio_path = _download_audio(result['audio_url'])

        return result['transcript'], result['summary'], result['translation'], audio_path

    except ValueError as e:
        # User input error (empty text, etc.) — show clean message in UI
        raise gr.Error(str(e))

    except requests.exceptions.ConnectionError:
        # No internet or Sunbird API unreachable
        raise gr.Error("Connection error: could not reach Sunbird API. Please check your internet connection.")

    except requests.exceptions.HTTPError as e:
        # API returned a 4xx or 5xx status code
        raise gr.Error(f"Sunbird API error: {e}")

    except Exception as e:
        # Catch-all for anything unexpected — still shows a clean message, not a traceback
        raise gr.Error(f"Unexpected error: {e}")


def process_audio(audio_path: str, language: str):
    """
    called by gradio when user enters audio
    audio_path: Gradio automatically saves the uploaded file and passes its path here
    """
    try:
        if not audio_path:
            raise ValueError("Please upload or record an audio file before running the pipeline.")

        # Check duration BEFORE sending to the API — avoids wasting an API call
        check_audio_duration(audio_path)

        result = pipeline.run(
            input_type='audio',
            text_input='',
            audio_path=audio_path,
            target_language=language
        )
        output_audio = _download_audio(result['audio_url'])

        return result["transcript"], result["summary"], result["translation"], output_audio

    except ValueError as e:
        raise gr.Error(str(e))

    except requests.exceptions.ConnectionError:
        raise gr.Error("Connection error: could not reach Sunbird API. Please check your internet connection.")

    except requests.exceptions.HTTPError as e:
        raise gr.Error(f"Sunbird API error: {e}")

    except Exception as e:
        raise gr.Error(f"Unexpected error: {e}")

def _download_audio(url: str) -> str:
    """
    downloads the audio from the temporary sunbird url 
    and saves locally, returns path
    """
    response = requests.get(url)
    response.raise_for_status()

    #create temp file in os temp folder
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tmp.write(response.content) #write the raw audio bytes
    tmp.close()

    return tmp.name


######UI Layout
with gr.Blocks(title='Sunbird AI Pipeline') as app:
    gr.Markdown("# Sunbird AI — Transcribe, Summarise, Translate & Speak")
    gr.Markdown("Enter text or upload audio, choose a language, and run the full pipeline.")

    #gr.Tabs() creates a tabbed interface
    with gr.Tabs():
        #Tab1: text input
        with gr.Tab('Text Input'):
            with gr.Row():
                text_input = gr.Textbox(
                    label="Enter text",
                    placeholder='Type or paste text here',
                    lines=5
                )
                text_language = gr.Dropdown(
                    choices=LANGUAGES,
                    label='Target language',
                    value='Acholi'
                )
            text_btn = gr.Button('Run Pipeline', variant='primary')
        
        #Tab2: AUdio input
        with gr.Tab('Audio Input'):
            with gr.Row():
                audio_input = gr.Audio(
                    label='Upload audio file',
                    type='filepath'
                )
                audio_language = gr.Dropdown(
                    choices=LANGUAGES,
                    label='Target language',
                    value='Acholi'
                )
            audio_btn = gr.Button('Run Pipeline', variant='primary')

    ###outputs, for both tabs
    gr.Markdown('## Results')

    with gr.Row():
        out_transcript = gr.Textbox(label='Transcript (audio input only)')
        out_summary = gr.Textbox(label='Summary')

    with gr.Row():
        out_translation = gr.Textbox(label='Translated Summary')
        out_audio = gr.Audio(label='Generated Speech')

    #wire buttons to functions
    text_btn.click(
        fn=process_text,
        inputs=[text_input, text_language],
        outputs=[out_transcript, out_summary, out_translation, out_audio]
    )

    audio_btn.click(
        fn=process_audio,
        inputs=[audio_input, audio_language],
        outputs=[out_transcript, out_summary, out_translation, out_audio]
    )

#launch the app

if __name__ == '__main__':
    app.launch(server_name="0.0.0.0", server_port=7860)
