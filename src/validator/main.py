# samples per second


AUDIO_PATH_IN = "../../dataSets/conversation/0.wav"
AUDIO_PATH_OUT = "../../dataSets/conversation/B_0.wav"

GOOGLE_API_CREDENTIALS = "/home/oscar/yt-scraper-289512-4338fa9d704e.json"


import validator as vl


# Scrapped wav files are not coded in PCM wav, it is needed by the sr.Recognizer()
vl.convertRawWav2PCMwav(AUDIO_PATH_IN, AUDIO_PATH_OUT)

# Geting the prediction using the external APIs
word_predicted = vl.recognize(AUDIO_PATH_OUT, GOOGLE_API_CREDENTIALS, api_number=1)
