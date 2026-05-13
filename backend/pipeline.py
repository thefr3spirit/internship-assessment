from backend import sunbird_client

def run(input_type: str, text_input: str, audio_path: str, target_language: str) -> dict:
    """
    Runs the full pipeline and returns all intermediary results
    
    input_type: text or audio
    text_input: typed/pasted text, for input type='text'
    audio_path: path to uploaded file, for input_type= 'audio'
    """
    transcript = '' #for when audio is transcribed

    #step 1: get text
    if input_type == 'audio':
        transcript = sunbird_client.transcribe(audio_path)
        text = transcript
    else:
        text = text_input

    #step 2: summarize
    summary = sunbird_client.summarise(text)

    #step 3: translate
    translation = sunbird_client.translate(summary, target_language)

    #step 4: Text to speech
    audio_url = sunbird_client.text_to_speech(translation, target_language)

    #return all in a dictionary
    return {
        'transcript': transcript,
        'summary': summary,
        'translation': translation,
        'audio_url': audio_url,
    }