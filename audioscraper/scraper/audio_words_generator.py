import json
import os
import shutil

from . import audio_subs_downloader as asd
from .subs_analyser import get_phrases_and_timestamps_from_vtt
from . import audio_analyser as aa
from .. import validator as vl
from .. import dictionary as dt

TEMP_DOWNLOADS_PATH = './.tmp'
SCRAPED_VIDEOS_JSON_NAME = '.scraped_videos_history.json'


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


def generate_audio_words_per_link(link, lang, ds_path):
    """
    Generates the audio_words in ds_path dir, if video(s) link have been already scraped
    i.e. contained in scraped_videos_history.json, then it does not generate audio_words again
    just to not replicate data in the dataSet
    :param link: of the videos or playlist
    :param lang: fr, en, es ...
    :param ds_path: where audio_words will be saved
    :return: True if ok, False if something went wrong
    """

    # Before start scraping I check the paths where I will put the files
    if not os.path.exists(ds_path):
        print("ERROR: dataSet path does not exist")
        return False
    downloads_path = TEMP_DOWNLOADS_PATH  # here I will put temporarily the .wav and .vtt files downloaded per link
    scraped_videos_path = os.path.join(ds_path, SCRAPED_VIDEOS_JSON_NAME)
    if not os.path.exists(downloads_path):
        os.mkdir(downloads_path)

    # Get final list of videos to scrap
    videos_to_scrap = asd.get_videos_infos_list_from_link(link, lang)
    if not os.path.exists(scraped_videos_path): # if scraped_videos_path does not exist I create an empty one
        with open(scraped_videos_path, mode='w', encoding='utf8') as json_file:
            json.dump([], json_file, sort_keys=True, indent=4, ensure_ascii=False)
    with open(scraped_videos_path, mode='r', encoding='utf8') as json_file:
        scraped_videos = json.load(json_file)
    not_yet_scraped_videos = get_not_yet_scraped_videos(videos_to_scrap, scraped_videos)

    if len(not_yet_scraped_videos) > 0:
        for video in not_yet_scraped_videos:
            if video['automatic_captions_lang']:
                wav_path, subs_path = asd.download_audios_and_subs(video['link'], lang, downloads_path)
                generate_audio_words_per_file(wav_path, subs_path, ds_path, lang)
                # Once audio_words are generated, remove wav and subs files and append it to scraped_videos list
                os.remove(wav_path)
                os.remove(subs_path)
                scraped_videos.append(video)
                # Update the json in scraped_videos_path
                with open(scraped_videos_path, mode='w', encoding='utf8') as json_file:
                    json.dump(scraped_videos, json_file, sort_keys=True, indent=4, ensure_ascii=False)
    else:
        print("Video(s) already scraped for this link: ", link)
        return True  # Nothing to do

    return True


def generate_audio_words_per_phrase(words, cut_indexes, signal_phrase, sample_rate, ds_path, lang, verbose=0):
    score_positives = 0
    score_negatives = 0
    if len(words) == len(cut_indexes):
        for i, cut_index_tuple in enumerate(cut_indexes):
            print("--------------------------------------")
            signal_word = signal_phrase[cut_index_tuple[0]:cut_index_tuple[1]]
            word_name = words[i]
            if dt.is_word_white_listed(word_name, lang):
                # Create path for word, if it does not exist
                word_folder_path = os.path.join(ds_path, word_name)
                if not os.path.exists(word_folder_path):
                    os.mkdir(word_folder_path)
                # Calculate name for the audio file and saved
                number_of_files = len([name for name in os.listdir(word_folder_path)
                                       if os.path.isfile(os.path.join(word_folder_path, name))])
                index_prefix = format(number_of_files, "04d")
                file_name = index_prefix + ".wav"
                word_final_path = word_folder_path + "/" + file_name  # ds_path/word_name/0001.wav
                aa.store_audio_file(signal_word, sample_rate, word_final_path, verbose=1)
                # Validate audio_word, if not valid delete audio_word
                # TODO optimize this once vl.recognize_signal is ready
                word_predicted = vl.recognize_audio_file(word_final_path, lang, api_number=1)
                if word_predicted == word_name:
                    score_positives = score_positives+1
                    pass
                else:
                    score_negatives = score_negatives+1
                    os.remove(word_final_path)
                    if number_of_files == 0:
                        shutil.rmtree(word_folder_path)
                    if verbose:
                        print("Validation failed, word:", word_name, "predicted_word: ", word_predicted)
                        print("audio file deleted: ", word_final_path)
            else:
                if verbose:
                    print("Word skipped, not in white_list : ", word_name)
    if verbose:
        print("\n-------------------------------")
        words_withe_list = [word for word in words if dt.is_word_white_listed(word, lang)]
        print("words: ", len(words), words)
        print("words white-listed: ", len(words_withe_list), words_withe_list)
        print("score_positives: ", score_positives)
        print("score_negatives: ", score_negatives)
    return score_positives, score_negatives


def generate_audio_words_per_file(audio_file, subs_file, ds_path, lang):
    """
    from the audio_file and with the help of subs_file
    it extracts the words (audio) and put them in the ds_path
    :param audio_file: there is one audio_file per video
    :param subs_file: the subs file in .vtt format, it is organized by phrases
    :param ds_path: directory where the generated audio_words are put
    :param lang: language needed for the dictionary white-list
    """

    # 1. get phrases and timestamps in a dictionary
    phrases_dict = {
        'phrases': [],
        'timestamps': [],
    }
    time_offset = get_phrases_and_timestamps_from_vtt(subs_file, phrases_dict)

    # 2. Loads the audio_file in the audio_signal
    try:
        audio_signal, sample_rate = aa.load_audio_signal(audio_file, verbose=1)
    except SystemError as ex:
        print("ERROR: exception catch. Error opening ", audio_file, ". ", ex)
        return False
    except MemoryError as ex:
        print("ERROR: exception catch. Error opening ", audio_file, ". ", ex)
        return False
    except BaseException as ex:
        print("ERROR: exception catch. Error opening ", audio_file, ": OTHER_EXCEPTION. ", ex.__class__, ". ", ex)
        return False

    # 3. Iterates through each phrase and get the words and cut_indexes
    #    Then it generates the audio files for each word
    print("\n\n--------------------- Extracting audio words for : ", audio_file, "-------BEGIN")
    try:
        for i, (phrase) in enumerate(phrases_dict['phrases']):
            if i == i:  # in range(0, 10):  # Fix here the phrase index I want to analyse
                phrase_timestamps = phrases_dict['timestamps'][i]
                print("\n----------------------------------------------------------------------------------------------"
                      "----------------------------")
                print(phrase, phrase_timestamps, " time_offset: ", time_offset)
                print("------------------------------------")
                words, cut_indexes, signal_phrase = aa.get_words_cut_indexes_and_signal_phrase(phrase,
                                                                                               phrase_timestamps,
                                                                                               time_offset,
                                                                                               audio_signal,
                                                                                               sample_rate)
                score_positives, score_negatives = generate_audio_words_per_phrase(words, cut_indexes, signal_phrase,
                                                                                   sample_rate, ds_path, lang, 1)
                # TODO compute score and exit if it is too bad, after first 20 guests
                print("------------------------------------------------------------------------------------------------"
                      "--------------------------")
    except BaseException as ex:
        # TODO if it repeats too much, it needs to be solved in the modules inside
        print("ERROR: exception catch. During extracting audio words for : ", audio_file)
        print(ex.__class__, ". ", ex)
        return False
    print("--------------------- Extracting audio words for : ", audio_file, "-------END\n\n")

    return True
