import os
import json

from audio_subs_extractor import download_audios_and_subs

VIDEO_LINKS_JSON_PATH = "../video_links.json"
AUDIOS_PATH = "../audios"
SUBS_PATH = "../subs"
DS_PATH = "../ds"

def main() :
    # read json entry
    with open(VIDEO_LINKS_JSON_PATH, mode='r', encoding='utf8') as json_file :
        json_dict = json.load(json_file)
    
    # get audios and subs per each youtube video link
    lang = json_dict["subs_lang"]
    json_dict["titles"] = []
    for link in json_dict["links"] :
        print ("----------------------------------------------------------")
        title = download_audios_and_subs(link, lang, AUDIOS_PATH, SUBS_PATH)
        json_dict["titles"].append(title)

    # write titles to json entry
    with open(VIDEO_LINKS_JSON_PATH, mode='w', encoding='utf8') as json_file :
        json.dump(json_dict, json_file, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == "__main__" :
    main()