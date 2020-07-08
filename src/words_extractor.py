import os
import pprint

from subs_analizer import get_phrases_and_timestamps

def check_paths_exist(paths_array) :
    for path in paths_array :
        if not os.path.lexists(path) :
            print("Path does not exist: ", path)
            return False
    return True

def extract_words(audio_file, subs_file, ds_path) :
    '''
    from the audio_file and with the help of subs_file
    it extracts the words (audio) and put them in the ds_path
    '''
    
    if not check_paths_exist([audio_file, subs_file, ds_path]) :
        return

    # get words and tiemstamps in a dictionay
    phrases_dict = {
        'phrases' : [],
        'timestamps' : [],
    }
    get_phrases_and_timestamps(subs_file, phrases_dict)

    pprint.pprint(phrases_dict)

    # ! Watchout for phrases of double line




    # get word audios
