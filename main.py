import scraper.audio_subs_downloader as asd
import scraper.audio_words_generator as awg

# from scraper import audio_words_generator as awg
# from scraper.audio_subs_downloader import download_audios_and_subs

import validator.validator as vl

AUDIO_PATH_IN = "../dataSets/conversation/0.wav"
AUDIO_PATH_OUT = "../dataSets/conversation/B_0.wav"



def main():

    # title, video_id = asd.download_audios_and_subs("link", "lang", "audios_path", "subs_path")

    # Scrapped wav files are not coded in PCM wav, it is needed by the sr.Recognizer()
    vl.convertRawWav2PCMwav(AUDIO_PATH_IN, AUDIO_PATH_OUT)


print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
if __name__ == "__main__":
    main()
