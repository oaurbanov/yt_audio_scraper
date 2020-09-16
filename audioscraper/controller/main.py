from ..validator import validator as vl

AUDIO_PATH_IN = "../dataSets/conversation/0.wav"
AUDIO_PATH_OUT = "../dataSets/conversation/B_0.wav"


def main():

    # Scrapped wav files are not coded in PCM wav, it is needed by the sr.Recognizer()
    vl.convertRawWav2PCMwav(AUDIO_PATH_IN, AUDIO_PATH_OUT)


if __name__ == "__main__":
    main()






# from ..scraper.audio_subs_downloader import download_audios_and_subs
#
#
#
#
# def main():
#     title, video_id = download_audios_and_subs("link", "lang", "audios_path", "subs_path")
#
#
# if __name__ == "__main__":
#     main()