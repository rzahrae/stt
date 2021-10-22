import json
import azure.cognitiveservices.speech as speechsdk
from flask import current_app

# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
service_region = "eastus"
with open("./instance/azure_speech.key") as file:
    speech_key = file.read().strip()

# Init our SDK
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region
)

speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "log.txt")

def get_stt(filename):
    audio_input = speechsdk.AudioConfig(filename=filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once_async().get()
    return json.loads(result.json)



