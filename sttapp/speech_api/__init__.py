import json
import time
import azure.cognitiveservices.speech as speechsdk
import speech_recognition as sr
from flask import current_app

# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
service_region = "eastus"
with open("./instance/azure_speech.key") as file:
    speech_key = file.read().strip()

# Init our SDK
endpoint = "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?initialSilenceTimeoutMs=100000&&endSilenceTimeoutMs=100000"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=endpoint)

speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "log.txt")


def get_stt(filename):

    transcript = ""

    def stop_cb(evt):
        print("CLOSING on {}".format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    audio_config = speechsdk.AudioConfig(filename=filename)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    done = False

    def concat_result(evt):
        results = json.loads(evt.result.json)
        nonlocal transcript
        if transcript == "":
            transcript = results["DisplayText"]
        else:
            transcript = "%s %s" % (transcript, results["DisplayText"])

    speech_recognizer.recognized.connect(concat_result)
    speech_recognizer.session_stopped.connect(stop_cb)

    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    # speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(0.5)

    return transcript
