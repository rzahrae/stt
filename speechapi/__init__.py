import azure.cognitiveservices.speech as speechsdk
from os import path

datadir = "./instance/data"

# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
service_region = "eastus"
with open("./instance/azure_speech.key") as file:
    speech_key = file.read().strip()


def get_tts(filename, text, ssml):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )

    speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "log.txt")

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_path = path.join(datadir, filename)
    audio_output = speechsdk.audio.AudioOutputConfig(filename=audio_path)

    # Creates a synthesizer with the given settings
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_output
    )

    # Synthesizes the text to speech.    
    if ssml:
        result = speech_synthesizer.speak_ssml_async(text).get()
    else:
        result = speech_synthesizer.speak_text_async(text).get()

    result_dict = {"status": "", "path": ""}

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        result_dict["error"] = False
        result_dict["status"] = "Speech synthesized"
        result_dict["path"] = audio_path
    elif result.reason == speechsdk.ResultReason.Canceled:
        result_dict["error"] = True
        cancellation_details = result.cancellation_details
        reason = "Speech synthesis canceled: {}".format(cancellation_details.reason)
        result_dict["status"] = reason
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                error = "Error details: {}".format(cancellation_details.error_details)
                result_dict["status"] = "%s %s" % (reason, error)

    print(result_dict)
    return result_dict
