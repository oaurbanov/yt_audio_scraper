import youtube_dl
import json
import os

from . import audio_subs_downloader as asd
from .subs_analyser import get_phrases_and_timestamps_from_vtt
from .audio_analyser import *
from .utils import *


def get_not_yet_scraped_videos(videos_to_scrap, scraped_videos, verbose=0):
    # compare video_infos_lists
    ids_to_scrap = [video_to_scrap['id'] for video_to_scrap in videos_to_scrap]
    ids_scraped = [scraped_video['id'] for scraped_video in scraped_videos]
    if verbose:
        print("\nids_to_scrap: ", ids_to_scrap)
        print("ids_scraped: ", ids_scraped)
    set1 = set(ids_to_scrap)
    set2 = set(ids_scraped)
    ids_not_yet_scraped = list(sorted(set1 - set2))
    ids_scraped_but_not_in_to_do_list = list(sorted(set2 - set1))
    if verbose:
        print("\nids_not_yet_scraped: ", ids_not_yet_scraped)
        print("ids_scraped_but_not_in_to_do_list: ", ids_scraped_but_not_in_to_do_list)
    videos_not_yet_scraped = []
    for id_ns in ids_not_yet_scraped:
        for video in videos_to_scrap:
            if video['id'] == id_ns:
                videos_not_yet_scraped.append(video)
    return videos_not_yet_scraped


def generate_audio_words_per_link(link, lang, downloads_path, ds_path, scraped_videos_path):
    """
    Generates the audio_words in ds_path dir, if video(s) link have been already scraped
    i.e. contained in scraped_videos_path, then it does not generate audio_words again
    just to not replicate data in the dataSet
    :param link: of the videos of playlist
    :param lang: fr, en, es
    :param downloads_path: where audio and sub files per video would be left temporarily
    :param ds_path: where audio_words will be extracted permanently
    :param scraped_videos_path: json containing register of already scraped videos
    :return: True if ok, False if something some error
    """
    # Get final list of videos to scrap
    videos_to_scrap = asd.get_videos_infos_list_from_link(link, lang)
    with open(scraped_videos_path, mode='r', encoding='utf8') as json_file:
        scraped_videos = json.load(json_file)
    not_yet_scraped_videos = get_not_yet_scraped_videos(videos_to_scrap, scraped_videos)

    # Before start scraping I check the paths where I will put the file
    if len(not_yet_scraped_videos) == 0:
        return True  # Nothing to do
    elif len(not_yet_scraped_videos) > 0:
        if not os.path.exists(downloads_path):
            print("ERROR: download path does not exist")
            return False
        audios_downloads_path = os.path.join(downloads_path, 'audios')
        subs_downloads_path = os.path.join(downloads_path, 'subs')
        if not os.path.exists(audios_downloads_path):
            os.mkdir(audios_downloads_path)
        if not os.path.exists(subs_downloads_path):
            os.mkdir(subs_downloads_path)

        for video in not_yet_scraped_videos:
            if video['automatic_captions_lang']:
                wav_path, subs_path = asd.download_audios_and_subs(video['link'], lang,
                                                                   audios_downloads_path, subs_downloads_path)
                #generate_audio_words_per_file(wav_path, subs_path, ds_path)
    # TODO: Don't forget to update the json in scraped_videos_path
    return True


def generate_audio_words_per_phrase(words, cut_indexes, signal_phrase, ds_path):
    if len(words) == len(cut_indexes):
        for i, cut_index_tuple in enumerate(cut_indexes):
            store_audio_file(signal_phrase[cut_index_tuple[0]:cut_index_tuple[1]], words[i], ds_path)


def generate_audio_words_per_file(audio_file, subs_file, ds_path):
    """
    from the audio_file and with the help of subs_file
    it extracts the words (audio) and put them in the ds_path
    :param audio_file: there is one audio_file per video
    :param subs_file: the subs file in .vtt format, it is organized by phrases
    :param ds_path: directory where the generated audio_words are put
    """
    
    if not check_paths_exist([audio_file, subs_file, ds_path]):
        return

    # 1. get phrases and timestamps in a dictionary
    phrases_dict = {
        'phrases': [],
        'timestamps': [],
    }
    time_offset = get_phrases_and_timestamps_from_vtt(subs_file, phrases_dict)

    # 2. Loads the audio_file in the audio_signal
    audio_signal = load_audio_signal(audio_file)

    # 3. Iterates through each phrase and get the words and cut_indexes
    #    Then it generates the audio files for each word
    for i, (phrase) in enumerate(phrases_dict['phrases']):
        if i == i:  # Fix here the phrase index I want to analyse
            phrase_timestamps = phrases_dict['timestamps'][i]
            print("\n--------------------------------------------------------------------------------------------------"
                  "------------------------")
            print(phrase, phrase_timestamps, " time_offset: ", time_offset)
            print("------------------------------------")
            words, cut_indexes, signal_phrase = get_words_cut_indexes_and_signal_phrase(phrase, phrase_timestamps,
                                                                                        time_offset, audio_signal)
            generate_audio_words_per_phrase(words, cut_indexes, signal_phrase, ds_path)
            print("----------------------------------------------------------------------------------------------------"
                  "----------------------")
