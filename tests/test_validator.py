import pytest
from .context import audioscraper
from audioscraper import validator as vl


AUDIO_WORD_PATH = "./resources/conversation.wav"
GOOGLE_API_CREDENTIALS = "/home/oscar/yt-scraper-289512-4338fa9d704e.json"


def test_recognize_api_1():
    # Getting the prediction using Google Web Speech API: Max 50 queries per month
    word_predicted = vl.recognize_audio_file(AUDIO_WORD_PATH, lang='fr', api_number=1)
    print("\nPrediction: ", word_predicted)
    assert "conversation" == word_predicted

# # TODO: Fix credentials problem
# def test_recognize_2():
#     # Getting the prediction using Google Cloud Speech: Requires Google Cloud Speech credentials
#     word_predicted = vl.recognize_audio_file(AUDIO_WORD_PATH, lang='fr', api_number=2, GOOGLE_API_CREDENTIALS)
