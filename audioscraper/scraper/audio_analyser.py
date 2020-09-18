import os
import librosa

import numpy as np
import soundfile as sf

import matplotlib.pyplot as plt
import numpy as np
import math

from .silence_analyser import find_silences, clean_signal_on_borders
from .phrase_analyser import get_temptative_cuts
from .utils import *

# samples per second
SAMPLE_RATE = 22050

# Time that subs can be offset from actual audio
SUBS_TIME_ADJUSTMENT = 100  # miliseconds


def plot_energy(energy_signal, threshold, silences, temptative_cut_indexes, title):
    print("threshold: ", threshold)
    describe_signal(energy_signal, "energy_signal")
    plt.title(title)
    plt.plot(np.arange(0, len(energy_signal), 1), energy_signal)
    plt.axhline(y=threshold, color='green', linestyle='--')
    for xc in temptative_cut_indexes:
        plt.axvline(x=xc, color='black', linestyle='--')
    for silence in silences:
        plt.axvline(x=silence[0], color='red', linestyle='--')
        plt.axvline(x=silence[1], color='orange', linestyle='--')
    plt.show()


def plot_signal(signal_phrase, silences, temptative_cut_indexes, title):
    plt.title(title)
    plt.plot(np.arange(0, len(signal_phrase), 1), signal_phrase)
    for xc in temptative_cut_indexes:
        plt.axvline(x=xc, color='black', linestyle='--')
    for silence in silences:
        plt.axvline(x=silence[0], color='red', linestyle='--')
        plt.axvline(x=silence[1], color='orange', linestyle='--')
    plt.show()


def plot_signal_result(signal_phrase, silences, temptative_cut_indexes, cut_indexes, title):
    plt.title(title)
    plt.plot(np.arange(0, len(signal_phrase), 1), signal_phrase)
    for xc in temptative_cut_indexes:
        plt.axvline(x=xc, color='black', linestyle='--')
    for silence in silences:
        plt.axvline(x=silence[0], color='red', linestyle='--')
        plt.axvline(x=silence[1], color='orange', linestyle='--')
    for cut_index_tuple in cut_indexes:
        plt.axvline(x=cut_index_tuple[0], color='yellow', linestyle='-')
        plt.axvline(x=cut_index_tuple[1], color='green', linestyle='-')
    plt.show()


def load_audio_signal(audio_file, target_sample_rate=SAMPLE_RATE, verbose=0):
    """
    returns normalized audio signal, if stereo make it mono
    and adapt it to the sample_rate
    """
    print("\n--------------------------------")
    print("Loading audio signal ...")
    # I use librosa since it sets a target_sample_rate
    y, sr = librosa.load(audio_file, target_sample_rate)
    # y, sr = sf.read(audio_file)
    print("Audio signal loaded ")
    if verbose:
        print("Sample rate: ", sr)
        describe_signal(y, "Loaded wav signal")
    print("--------------------------------\n")
    return y


def store_audio_file(signal, file_path, sample_rate=SAMPLE_RATE, verbose=0):
    try:
        sf.write(file_path, signal, sample_rate, 'PCM_16')
        if verbose:
            print("Audio file saved: ", file_path)
    except Exception as ex:
        print("Exception: ", ex, ". When saving the file: ", file_path)
        return False
    return True


# def find_closer_end_silence(temptative_cut_index, silences):
#     for silence in reversed(silences):
#         if silence[1] < temptative_cut_index:
#             return silence[1]
#     print("ERROR: not found closer end_silence")
#     return temptative_cut_index


def get_words_cut_indexes_and_signal_phrase(phrase, phrase_timestamps, time_offset, signal, sample_rate=SAMPLE_RATE,
                                            subs_time_adjustment=SUBS_TIME_ADJUSTMENT, verbose=1):
    # 0. Put the offset, set generally in the 5th line of the .vtt subs file:
    # 00:00:01.399 --> 00:00:04.999 align:start position:0%

    to_1 = round(get_secs(time_offset[0]), 2)
    to_2 = round(get_secs(time_offset[1]), 2)
    t_offset = to_1 - to_2  # rule found empirically
    index_offset = round(t_offset * sample_rate)

    # 1. Extract signal_phrase (sub_signal containing just the part of the phrase)
    t1 = round(get_secs(phrase_timestamps[0]) - subs_time_adjustment * 0.001, 2)
    t2 = round(get_secs(phrase_timestamps[1]) + subs_time_adjustment * 0.001, 2)

    index_1 = round(t1 * sample_rate) + index_offset
    index_2 = round(t2 * sample_rate) + index_offset  # (t2 +to_1) added to fit video ID: WofKLzddask

    # check index consistency
    if index_1 < 0:
        index_1 = 0
    if index_2 < 0:
        index_2 = 0
    if index_2 > len(signal) - 1:
        index_2 = len(signal) - 1
    if index_1 >= index_2:
        print("ERROR: time_ini is greater that time_end: ", phrase_timestamps)
        return [], [], []

    signal_phrase = signal[index_1:index_2]

    # 2. extract silences and temptative_cut_indexes

    # 2.1. find silences
    energy_signal, threshold, silences = find_silences(signal_phrase, SAMPLE_RATE)
    # 2.2. clean signal_phrase on borders and adjust silences
    silences, signal_phrase, energy_signal = clean_signal_on_borders(silences, signal_phrase, energy_signal)
    print("Silences: ", len(silences), ", ", silences)

    # 2.3. extract temptative cut_indexes regarding size of each word
    temptative_cut_indexes = get_temptative_cuts(phrase, signal_phrase)
    print("Temptative_cut_indexes: ", len(temptative_cut_indexes), ", ", temptative_cut_indexes)

    # Plot this to understand part 3. of the code
    # plot_signal(signal_phrase, silences, temptative_cut_indexes, phrase)
    # plot_energy(energy_signal, threshold, silences, temptative_cut_indexes, phrase)

    # 3. Now with silences extracted and temptative_cut_indexes I can start to infer which audio-words worths to extract

    # # 3.A. Method 1: Cut the word when its correponding temptative_cut_index is in between a silence_n
    # #                Then, cut from silence_n[0] until silence_n-1[1]
    # words = []
    # cut_indexes = []
    # silences.append((temptative_cut_indexes[-1], temptative_cut_indexes[-1])) # Small adjustment: virtual silence at the end
    # last_silence = (0, 0)
    # # This piece of code just have sense if there is >= number of silences than temptative_cut_indexes
    # if len(silences) >=  len(temptative_cut_indexes)-1 :
    #     for i, (word) in enumerate (phrase.split(" ")):
    #         if word: # checks not empty string
    #             # print(i,word)
    #             last_words_len = len(words)
    #             for silence in silences:
    #                 if num_inside_limits(temptative_cut_indexes[i+1], silence):
    #                     words.append(word)
    #                     cut_indexes.append((last_silence[1], silence[0]))
    #                     last_silence = silence
    #             # If I did not append the current word then I need to update last_silence value
    #             if last_words_len == len(words):
    #                 last_silence = (0, find_closer_end_silence(temptative_cut_indexes[i+1], silences))

    # 3.B. Method 2: Move temptative_cut_index to its closer silence, then all words will be extracted
    words = []
    cut_indexes = []
    silences.insert(0, (0, 0))  # Small adjustment: virtual silence at the beginnig
    silences.append(
        (temptative_cut_indexes[-1], temptative_cut_indexes[-1]))  # Small adjustment: virtual silence at the end
    # This piece of code just have sense if len(silences) >=  len(temptative_cut_indexes) :
    if len(silences) >= len(temptative_cut_indexes) * 0.666:  # Small adjustment: 1/3 of words are pronounced together
        # B.1. Find central position of each silence
        silences_centers = []
        for silence in silences:
            silences_centers.append(silence[0] + math.floor((silence[1] - silence[0]) / 2))

        # B.2. Extract correlation matrix, distance of each cut_index to each silence_center
        h, w = len(temptative_cut_indexes), len(silences)
        cor_matrix = [[0 for x in range(w)] for y in range(h)]
        for i, (cut_index) in enumerate(temptative_cut_indexes):
            for j, (silence_center) in enumerate(silences_centers):
                cor_matrix[i][j] = abs(silence_center - cut_index)

        # B.3. Extract the indexes of the closest silence per each temptative_cut_index
        closest_silences_index_array = []
        for i, (cut_index) in enumerate(temptative_cut_indexes):
            row = cor_matrix[i]
            closest_silence_index = row.index(min(row))
            closest_silences_index_array.append(closest_silence_index)
        csia = closest_silences_index_array

        # B.4. Append the words and its corresponding cut_indexes based on the csia
        for i, (word) in enumerate(phrase.split(" ")):
            if word:  # checks not empty string
                # The closest silence could be repeated for 2 consecutive cut_indexes
                # In that case I don't extract any audio_words
                if csia[i + 1] > csia[i]:
                    words.append(word)
                    cut_indexes.append((silences[csia[i]][1], silences[csia[i + 1]][0]))

    if verbose:
        print("\nget_words_and_cut_indexes results: ---------")
        print("phrase: ", phrase.count(' ') + 1, ", ", phrase)
        print("words: ", len(words), ", ", words)
        print("cut_indexes: ", len(cut_indexes), ", ", cut_indexes)
        print("------------------------------------")

    # Plot this to debug how cuts are made at each phrase
    # plot_signal_result(signal_phrase, silences, temptative_cut_indexes, cut_indexes, phrase)

    return words, cut_indexes, signal_phrase
