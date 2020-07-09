from pydub import AudioSegment
from scipy.io import wavfile
import librosa

import matplotlib.pyplot as plt

import numpy as np

from extractor import extract_words
from utils import *

# samples per second
SAMPLE_RATE = 22050

# Time that subs can be offset from actual audio
SUBS_TIME_ADJUSTMENT = 100 # miliseconds


def load_audio_signal(audio_file, target_sample_rate) :
    '''
    returns normalized audio signal, if stereo make it mono
    and adapt it to the sample_rate 
    '''
    print("--------------------------------")
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

    return y


def get_words_and_cuts(phrase , phrase_timestamps, signal, sample_rate, subs_time_adjustment) :


    # extract signal_phrase
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

    # extract words
    words, index_cuts = extract_words(signal_phrase, phrase, sample_rate)

    return words, index_cuts






def generate_audio_dataset(audio_file, phrases_dict, ds_path):

    signal = load_audio_signal(audio_file,SAMPLE_RATE)

    for i, (phrase) in enumerate(phrases_dict['phrases']) :
        if i == 16 :
            phrase_timestamps = phrases_dict['timestamps'][i]
            print("--------------------------extracting from phrase-------------------------------------------")
            print(phrase , phrase_timestamps)
            print("--------------------------------")
            words, index_cuts = get_words_and_cuts(phrase , phrase_timestamps, signal, SAMPLE_RATE, SUBS_TIME_ADJUSTMENT)
            print("--------------------------extracting from phrase-------------------------------------------")

            break





