import pprint

from subs_analyser import get_phrases_and_timestamps_from_vtt
from audio_analyser import *
from utils import *



def generate_audio_words_per_phrase(words, cut_indexes, signal_phrase, ds_path):

    if len(words) == len(cut_indexes):
        for i, cut_index_tuple in enumerate(cut_indexes):
            store_audio_file(signal_phrase[cut_index_tuple[0]:cut_index_tuple[1]], words[i], ds_path)


def generate_audio_words_per_file(audio_file, subs_file, ds_path) :
    '''
    from the audio_file and with the help of subs_file
    it extracts the words (audio) and put them in the ds_path
    :param audio_file: there is one audio_file per video
    :param subs_file: the subs file in .vtt format, it is organized by phrases
    :param ds_path: directory where the generated audio_words are put
    '''
    
    if not check_paths_exist([audio_file, subs_file, ds_path]) :
        return

    # 1. get phrases and timestamps in a dictionary
    phrases_dict = {
        'phrases' : [],
        'timestamps' : [],
    }
    get_phrases_and_timestamps_from_vtt(subs_file, phrases_dict)
    # ! Watchout for phrases of double line
    pprint.pprint(phrases_dict)


    # 2. Loads the audio_file in the audio_signal
    audio_signal = load_audio_signal(audio_file)

    # 3. Iterates through each phrase and get the words and cut_indexes
    #    Then it generates the audio files for each word

    for i, (phrase) in enumerate(phrases_dict['phrases']):
        phrase_timestamps = phrases_dict['timestamps'][i]
        print("\n-------------------------------------")
        print(phrase , phrase_timestamps)
        print("------------------------------------\n")
        words, cut_indexes, signal_phrase = get_words_cut_indexes_and_signal_phrase(phrase, phrase_timestamps, audio_signal)
        generate_audio_words_per_phrase(words, cut_indexes, signal_phrase, ds_path)
