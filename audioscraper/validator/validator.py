import speech_recognition as sr
import json


def recognize_audio_signal():
    # TODO build sr.AudioFile()  from signal, frame-rate
    pass


def recognize_audio_file(audio_path_in, lang='fr-FR', api_number=1, google_api_cred_path=""):
    """
    using external APIs, it recognices the audio in the file
    :param audio_path_in:
    :param lang:
    :param api_number:  Wich API to use
                1. Google Web Speech API: Max 50 queries per month
                2. Google Cloud Speech: Requires Google Cloud Speech credentials
    :param google_api_cred_path:
    :return: predicted word
    """

    #Requires kind of spefical format language
    language = lang.lower()+'-'+lang.upper()  # fr-FR TODO process langs like en-US
    prediction = ""
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path_in)
    with audio_file as source:
        audio = r.record(source)

        try:
            if api_number == 1:
                # 1. Google Web Speech API
                prediction = r.recognize_google(audio, language=language)
            elif api_number == 2:
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
        except sr.RequestError as ex:
            # API was unreachable or unresponsive
            print("Exception catch in validator: ", ex)
            print("-API was unreachable or unresponsive")
        except sr.UnknownValueError as ex:
            # speech was unintelligible
            print("Exception catch in validator: ", ex)
            print("-speech was unintelligible")

    return prediction
