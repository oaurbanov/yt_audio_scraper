import numpy as np

from audioscraper.scraper import utils

# 0: 10, 0.7, 70
# 1: 50, 0.5, 100
# 16: 50, 0.4, 70 ----- Best

MINIMAL_SILENCE_LENGTH = 50  # milisecs
K_SILENCE_THRESHOLD = 0.4
MINIMAL_WORD_LENGTH = 70  # milisecs


def fromFloat2PCM16(signal_in):
    """
    Converts entry signal
    from array_Float in range(-1,+1)
    to array_int16 in range(-32768, +32768)
    """
    # conversion constant, found empirically
    K_CONSTANT = 8784 / 0.2680664
    signal_out = signal_in * (K_CONSTANT)
    signal_out = signal_out.astype('h')
    return signal_out


def get_energy_signal(signal_in):
    # I pass this from range(-1,+1)  to range(-32768, +32768) just to visualize it better
    signal = fromFloat2PCM16(signal_in)
    segments = np.array(signal)
    energies = [(s ** 2).sum() / len(signal_in) for s in segments]
    threshold = K_SILENCE_THRESHOLD * np.average(energies)
    return threshold, energies


def find_silences(signal_in, sample_rate, minimal_silence_length=MINIMAL_SILENCE_LENGTH,
                  minimal_word_length=MINIMAL_WORD_LENGTH, verbose=False):

    # 1. Get energy signal and its threshold
    threshold, energies = get_energy_signal(signal_in)
    index_of_segments_to_keep = (np.where(energies > threshold)[0])

    # 2. If Silence_duration >= silence_samples : save that as boundary point
    silence_samples = sample_rate * minimal_silence_length * 0.001
    if verbose:
        print("a silence contains n samples = ", silence_samples)

    silences_list = []
    for i, (index) in enumerate(index_of_segments_to_keep):
        # first silence
        if (i == 0 and index >= silence_samples):
            silences_list.append((0, index))
        # last silence
        elif (i == len(index_of_segments_to_keep) - 1 and ((len(energies) - 1) - index) >= silence_samples):
            silences_list.append((index, len(energies) - 1))
        # silences in the middle
        elif (i < len(index_of_segments_to_keep) - 1 and index_of_segments_to_keep[i + 1] - index >= silence_samples):
            silence = (index, index_of_segments_to_keep[i + 1])
            silences_list.append(silence)

    # 3. eliminating words in the middle of silences, that do not have the minimal_word_length
    minimal_word_samples = sample_rate * minimal_word_length * 0.001
    if verbose:
        print("a word contains at least n samples = ", minimal_word_samples)
    for i, (silence) in enumerate(silences_list):
        if i < len(silences_list) - 2:
            next_silence = silences_list[i + 1]
            if (next_silence[0] - silence[1]) <= minimal_word_samples:
                new_silence = (silence[0], next_silence[1])
                silences_list[i] = (-1, -1)
                silences_list[i + 1] = new_silence
    silences_list = [s for s in silences_list if s != (-1, -1)]

    return energies, threshold, silences_list


def clean_signal_on_borders(silences, signal_phrase, energy_signal, verbose=0):
    """
    If first silence and last silence are at begining of signal and/or at the end, respectively
    I can short the signal, and should also readjust indexes of silences and resize energy_signal
    """

    if verbose:
        print('\nSilences: ', silences)
        utils.describe_signal(signal_phrase, 'signal_phrase')
        utils.describe_signal(energy_signal, 'energy_signal')

    # If there is no silences at the borders to cut
    if len(silences) == 0:
        return silences, signal_phrase, energy_signal

    index_end = len(signal_phrase) - 1
    if silences[-1][1] == len(signal_phrase) - 1:
        index_end = silences[-1][0]
        silences.pop(-1)
        signal_phrase = signal_phrase[:index_end]

    # If there was just one silence and I just pop it
    if len(silences) == 0:
        # I also adjust the energy signal
        energy_signal = energy_signal[: index_end]
        return silences, signal_phrase, energy_signal

    index_start = 0
    if silences[0][0] == 0:
        index_start = silences[0][1]
        silences.pop(0)
        signal_phrase = signal_phrase[index_start:]
        # as signal changes I need to readjust also indexes of the silences
        new_silences = []
        for silence in silences:
            silence_start = silence[0] - index_start
            silence_end = silence[1] - index_start
            new_silences.append((silence_start, silence_end))
        silences = new_silences

    # I also adjust the energy signal
    energy_signal = energy_signal[index_start: index_end]

    return silences, signal_phrase, energy_signal
