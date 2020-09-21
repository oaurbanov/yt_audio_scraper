import pytest
import os
import numpy as np

from .context import audioscraper
from audioscraper import audio_analyser as aa

SAMPLE_RATE = 22050


def describe_signal(signal, name=""):
    print("-------", name, "------")
    print("type: ", type(signal))
    print("len: ", len(signal))
    print("max: ", max(signal))
    print("min: ", min(signal))
    print("-------", name, "------")


def test_store_audio_file():
    signal = [0.2, 0.1, 0.2, -0.3, -0.4, 0.5]  # float32 in this range(-1,+1)
    np_signal = np.array(signal, dtype='float32')
    file_path = "./dummyAudio.wav"
    aa.store_audio_file(np_signal, SAMPLE_RATE, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)


def test_load_audio_signal():
    file_path = "./dummyAudio.wav"
    signal = [0.2, 0.1, 0.2, -0.3, -0.4, 0.5]  # float32 in this range(-1,+1)
    np_signal = np.array(signal, dtype='float32')
    aa.store_audio_file(np_signal, SAMPLE_RATE, file_path)

    y, sr = aa.load_audio_signal(file_path, verbose=1)
    print("len shape: ", len(y.shape))
    assert len(y) > 0 and sr > 0
    os.remove(file_path)
