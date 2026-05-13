import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import pipeline

#test with text input
print('=== text input ===')
result = pipeline.run(
    input_type='text',
    text_input='I am here to stay',
    audio_path='',
    target_language='Acholi'
)

print('Transcript:', result['transcript'])
print('Summary:', result['summary'])
print('Translation:', result['translation'])
print('Audio URL:', result['audio_url'])



#Test with audio input
print('=== audio input ===')

result = pipeline.run(
    input_type='audio',
    text_input='',
    audio_path='C:\\Users\\HP\Downloads\\20260513113503_1a5c2e8e-cfc7-46b8-8d9f-df3e2f2c5b1f.mp3',
    target_language='Acholi'
)

print('Transcript:', result['transcript'])
print('Summary:', result['summary'])
print('Translation:', result['translation'])
print('Audio URL:', result['audio_url'])