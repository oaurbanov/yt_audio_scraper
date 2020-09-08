import os
import json

from audio_subs_extractor import download_audios_and_subs
from audio_words_generator import generate_audio_words_per_file

JSON_PATH = "../video_links.json"
AUDIOS_PATH = "../audios"
SUBS_PATH = "../subs"
DS_PATH = "../dataSets"

def get_audios_and_subtitles(json_path, audios_path, subs_path) :
    '''
    From the links in json (from json_path), it downloads the subtitle and audio files
    Each video has an id (used as name) to store the audio and sub files
    :param json_path: path of the json file containing links to the videos to extract audio and subs
    :param audios_path: dir to put the audio_file per video
    :param subs_path: dir to put the sub_file per video
    '''

    print("----------------------------get_audios_and_subtitles------------------------------BEGIN")

    # read json entry
    with open(json_path, mode='r', encoding='utf8') as json_file :
        json_dict = json.load(json_file)
    
    # get audios and subs per each youtube video link
    lang = json_dict["subs_lang"]
    json_dict["titles"] = []
    json_dict["ids"] = []
    for link in json_dict["links"] :
        print ("----------------------------------------------------------")
        title, video_id = download_audios_and_subs(link, lang, audios_path, subs_path)
        json_dict["titles"].append(title)
        json_dict["ids"].append(video_id)

    # write titles and ids to json entry
    with open(json_path, mode='w', encoding='utf8') as json_file :
        json.dump(json_dict, json_file, sort_keys=True, indent=4, ensure_ascii=False)

    print("----------------------------get_audios_and_subtitles------------------------------END")

def generate_dataset(audios_path, subs_path, ds_path) :
    '''
    Iterates through the audio files corresponding to each video
    and using the sub files, It extracts the audios corresponding to each word (audio_word)
    Each audio_word is then put in the ds_path
    :param audios_path: dir with the audio_files one per each video_link
    :param subs_path: dir with the sub_files one per each video_link
    :param ds_path: directory where the generated audio_words are put
    '''

    print ("-----------------------------generate_dataset-----------------------------BEGIN")

    # extract audio_words, walking through the previously extracted audios and subs
    for dirpath, dirnames, filenames in os.walk(audios_path) :
        for filename in filenames :
            if ".wav" in filename :
                print ("----------------------------------------------------------")
                id = filename.replace(".wav", "")
                audio_file = os.path.join(audios_path, filename)
                subs_file = os.path.join(subs_path, id+".fr"+".vtt")
                generate_audio_words_per_file(audio_file, subs_file, ds_path)

    print ("-----------------------------generate_dataset-----------------------------END")

def main() :

    # get_audios_and_subtitles(JSON_PATH, AUDIOS_PATH, SUBS_PATH)

    generate_dataset(AUDIOS_PATH, SUBS_PATH, DS_PATH)


if __name__ == "__main__" :
    main()