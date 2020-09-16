from pydub import AudioSegment

SAMPLE_RATE = 22050

import speech_recognition as sr
import json


def recognize(audio_path_in, google_api_cred_path="", api_number=1, lang='fr-FR'):
    """
    using external APIs, it recognices the audio in the file
    :param audio_path_in:
    :param api:  Wich API to use
                1. Google Web Speech API: Max 50 queries per month
                2. Google Cloud Speech: Requires Google Cloud Speech credentials
    :return: predicted word
    """

    prediction = ""
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path_in)
    with audio_file as source:
        audio = r.record(source)

        if (api_number==1):
            # 1. Google Web Speech API
            prediction = r.recognize_google(audio, language='fr-FR')


        elif (api_number==2):
            # 2. Google Cloud Speech
            with open(google_api_cred_path, mode='r', encoding='utf8') as json_credentials:
                json_dict = json.load(json_credentials)
                json_dump = json.dumps(json_dict, indent=4)
                # print(json_dump)
                # audio_data: AudioData, credentials_json: Union[str, None] = None, language: str = "en-US", preferred_phrases: Union[Iterable[str], None] = None, show_all: bool = False) -> Union[str, Dict[str, Any]
                prediction = r.recognize_google_cloud(audio, json_dump, language=lang)
                # TODO issue 0001:

            # import os
            # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_api_cred_path
            # prediction = r.recognize_google_cloud(audio, language=lang)

    print(prediction)
    return prediction



# def convertRawWav2PCMwav(audio_in, audio_out, frame_rate=SAMPLE_RATE, sample_width=2, verbose=0):
#     """
#     Convert raw wav audio chunks, into PCM codified wav audio
#     :param audio_in: path audio input
#     :param audio_out: path audio output
#     :param frame_rate: encoding frame_rate
#     :param sample_width:
#                     1 : “8 bit Signed Integer PCM”,
#                     2 : “16 bit Signed Integer PCM”,
#                     3 : “32 bit Signed Integer PCM”,
#                     4 : “64 bit Signed Integer PCM”
#     :param verbose:
#     """
#
#     sound = AudioSegment.from_file(audio_in)
#
#     if verbose:
#         print("----------Before Conversion--------")
#         print("Frame Rate", sound.frame_rate)
#         print("Channel", sound.channels)
#         print("Sample Width", sound.sample_width)
#
#     # Change Frame Rate
#     sound = sound.set_frame_rate(SAMPLE_RATE)
#     # Change Channel
#     sound = sound.set_channels(1)
#     # Change Sample Width
#     sound = sound.set_sample_width(sample_width)
#     # Export the Audio to get the changed content
#     sound.export(audio_out, format="wav")
