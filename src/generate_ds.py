import os
import json

from audio_subs_extractor import download_audios_and_subs
from words_extractor import extract_words

JSON_PATH = "../video_links.json"
AUDIOS_PATH = "../audios"
SUBS_PATH = "../subs"
DS_PATH = "../dataSets"

def get_audios_and_subtitles(json_path, audios_path, subs_path) :

    print ("----------------------------get_audios_and_subtitles------------------------------")

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


def generate_dataset(audios_path, subs_path, ds_path) :

    print ("-----------------------------generate_dataset-----------------------------")

    # extract words, walking through the previously extracted audios and subs
    for dirpath, dirnames, filenames in os.walk(audios_path) :
        for filename in filenames :
            if ".wav" in filename :
                print ("----------------------------------------------------------")
                id = filename.replace(".wav", "")
                audio_file = os.path.join(audios_path, filename)
                subs_file = os.path.join(subs_path, id+".fr"+".vtt")
                extract_words(audio_file, subs_file, ds_path)

def main() :

    get_audios_and_subtitles(JSON_PATH, AUDIOS_PATH, SUBS_PATH)

    generate_dataset(AUDIOS_PATH, SUBS_PATH, DS_PATH)


if __name__ == "__main__" :
    main()