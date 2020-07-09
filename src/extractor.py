import matplotlib.pyplot as plt
import numpy as np

from silence_analyser import find_silences, clean_signal_on_borders
from phrase_analyser import get_temptative_cuts
from utils import *


def plot_energy(energy_signal, threshold, silences, temptative_cuts) :

    print("threshold: ", threshold)
    describe_signal(energy_signal, "energy_signal")

    plt.plot(np.arange(0,len(energy_signal),1), energy_signal)
    plt.axhline(y=threshold, color='green', linestyle='--')
    for xc in temptative_cuts:
        plt.axvline(x=xc, color='black', linestyle='--')
    for silence in silences:
        plt.axvline(x=silence[0], color='red', linestyle='--')
        plt.axvline(x=silence[1], color='orange', linestyle='--')
    plt.show()

def plot_signal(signal_phrase, silences, temptative_cuts) :
    plt.plot(np.arange(0,len(signal_phrase),1), signal_phrase)
    for xc in temptative_cuts:
        plt.axvline(x=xc, color='black', linestyle='--')
    for silence in silences:
        plt.axvline(x=silence[0], color='red', linestyle='--')
        plt.axvline(x=silence[1], color='orange', linestyle='--')
    plt.show()

def extract_words(signal_phrase, phrase, sample_rate) :

    # find silences
    energy_signal, threshold, silences = find_silences(signal_phrase, sample_rate)

    silences, signal_phrase, energy_signal = clean_signal_on_borders(silences, signal_phrase, energy_signal)

    # extract temptative indexes regarding size of each word
    temptative_cuts = get_temptative_cuts(phrase, signal_phrase) 
    print("Temptative cut positions: ",temptative_cuts)

    plot_signal(signal_phrase, silences, temptative_cuts)
    # plot_energy(energy_signal, threshold, silences, temptative_cuts)

    # TODO now with silences extracted and temptative_cuts I can start to infer wich audio-words worths to extract

    words = []
    index_cuts = []

    return words, index_cuts
