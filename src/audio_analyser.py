from pydub import AudioSegment
from scipy.io import wavfile
import os
import librosa

import matplotlib.pyplot as plt
import numpy as np

from silence_analyser import find_silences, clean_signal_on_borders
from phrase_analyser import get_temptative_cuts
from utils import *



# samples per second
SAMPLE_RATE = 22050

# Time that subs can be offset from actual audio
SUBS_TIME_ADJUSTMENT = 100 # miliseconds



def plot_energy(energy_signal, threshold, silences, temptative_cut_indexes, title) :

    print("threshold: ", threshold)
    describe_signal(energy_signal, "energy_signal")

    plt.title(title)
    plt.plot(np.arange(0,len(energy_signal),1), energy_signal)
    plt.axhline(y=threshold, color='green', linestyle='--')
    for xc in temptative_cut_indexes:
        plt.axvline(x=xc, color='black', linestyle='--')
    for silence in silences:
        plt.axvline(x=silence[0], color='red', linestyle='--')
        plt.axvline(x=silence[1], color='orange', linestyle='--')
    plt.show()

def plot_signal(signal_phrase, silences, temptative_cut_indexes, title) :

    plt.title(title)
    plt.plot(np.arange(0,len(signal_phrase),1), signal_phrase)
    for xc in temptative_cut_indexes:
        plt.axvline(x=xc, color='black', linestyle='--')
    for silence in silences:
        plt.axvline(x=silence[0], color='red', linestyle='--')
        plt.axvline(x=silence[1], color='orange', linestyle='--')
    plt.show()


def load_audio_signal(audio_file, target_sample_rate=SAMPLE_RATE) :
    '''
    returns normalized audio signal, if stereo make it mono
    and adapt it to the sample_rate 
    '''
    print("------------------load_audio_signal--------------BEGIN")
    print("Loading signal ")
    # sample_rate, signal = wavfile.read(audio_file)
    # print("sample_rate: ", sample_rate)

    # signal_1 = signal[:,0]
    # signal_2 = signal[:,1]
    # signal_mono = (signal[:,0]/2) + (signal[:,1]/2)

    # # describe_signal(signal_1)
    # # describe_signal(signal_2)
    # describe_signal(signal_mono)

    # # # downsampling / upsampling
    # # samples_to_keep = target_sample_rate/sample_rate # 22050 / 44100  = 0.5

    # import librosa
    y, sr = librosa.load(audio_file, target_sample_rate)
    print("sample rate: ", sr)
    describe_signal(y,"loaded wav signal")

    print("------------------load_audio_signal--------------END")
    return y

def store_audio_file(signal, name, ds_path):
    word_folder_path = os.path.join(ds_path, name)
    if not os.path.lexists(word_folder_path):
        os.mkdir(word_folder_path)

    for dirpath, dirnames, filenames in os.walk(word_folder_path):
        index = len(filenames)
        librosa.output.write_wav(os.path.join(word_folder_path, str(index)+".wav"), signal, SAMPLE_RATE)


def find_closer_end_silence(temptative_cut_index, silences) :
    for silence in reversed(silences):
        if silence[1] < temptative_cut_index:
            return silence[1]
    print("ERROR: not found closer end_silence")
    return temptative_cut_index


def get_words_cut_indexes_and_signal_phrase(phrase , phrase_timestamps, signal, sample_rate=SAMPLE_RATE, subs_time_adjustment=SUBS_TIME_ADJUSTMENT) :


    # 1. Extract signal_phrase (sub_signal containing just the part of the phrase)
    t1 = round(get_secs(phrase_timestamps[0]) - subs_time_adjustment*0.001, 2)
    if t1 < 0 : t1 = 0
    t2 = round(get_secs(phrase_timestamps[1]) + subs_time_adjustment*0.001, 2)

    index_1 = round(t1 * sample_rate)
    index_2 = round(t2 * sample_rate)
    
    # check index consistency
    if (index_2 > len(signal)-1) :
        index_2 = len(signal) -1
    if (index_1 >= index_2) :
        print("ERROR: time_ini is greater that time_end: ", phrase_timestamps)

    signal_phrase = signal[index_1:index_2]

    # 2. extract silences and temptative_cut_indexes

    # 2.1. find silences
    energy_signal, threshold, silences = find_silences(signal_phrase, SAMPLE_RATE)
    # 2.2. clean signal_phrase on borders and adjust silences
    silences, signal_phrase, energy_signal = clean_signal_on_borders(silences, signal_phrase, energy_signal)
    print("Silences: ", silences)

    # 2.3. extract temptative cut_indexes regarding size of each word
    temptative_cut_indexes = get_temptative_cuts(phrase, signal_phrase)
    print("Temptative_cut_indexes: ",temptative_cut_indexes)

    ## Plot this to understand part 3. of the code
    # plot_signal(signal_phrase, silences, temptative_cut_indexes, phrase)
    # plot_energy(energy_signal, threshold, silences, temptative_cut_indexes, phrase)

    # 3. Now with silences extracted and temptative_cut_indexes I can start to infer which audio-words worths to extract
    words = []
    cut_indexes = []
    silences.append((temptative_cut_indexes[-1], temptative_cut_indexes[-1])) # Small adjustment: virtual silence at the end
    last_silence = (0, 0)
    # This piece of code just have sense if there is >= number of silences than temptative_cut_indexes
    if len(silences) >=  len(temptative_cut_indexes)-2 :
        for i, (word) in enumerate (phrase.split(" ")):
            if word: # checks not empty string
                # print(i,word)
                last_words_len = len(words)
                for silence in silences:
                    if num_inside_limits(temptative_cut_indexes[i+1], silence):
                        words.append(word)
                        cut_indexes.append((last_silence[1], silence[0]))
                        last_silence = silence
                # If I did not append the current word then I need to update last_silence value
                if last_words_len == len(words):
                    last_silence = (0, find_closer_end_silence(temptative_cut_indexes[i+1], silences))

    print("\nget_words_and_cut_indexes results: ---------")
    print("phrase: ", phrase)
    print("words: ", words)
    print("cut_indexes: ", cut_indexes)
    print("------------------------------------\n")


    return words, cut_indexes, signal_phrase





