import pytest
import shutil
import numpy as np

from .context import audioscraper


def describe_signal(signal, name=""):
    print("-------", name, "------")
    print("type: ", type(signal))
    print("len: ", len(signal))
    print("max: ", max(signal))
    print("min: ", min(signal))
    print("-------", name, "------")


def test_load_audio_file():
    y = audioscraper.load_audio_signal("./resources/conversation.wav")
    describe_signal(y, "from load_audio_signal")
    assert len(y) > 0


def test_store_audio_file():
    # I use the dataSets name as it is ignored in the .git
    try:
        shutil.rmtree('./dataSets')
    except:
        print("Path does not exist yet")

    signal = [0.2, 0.1, 0.2, -0.3, -0.4, 0.5]  # float32 in this range(-1,+1)
    np_signal = np.array(signal, dtype='float32')
    assert audioscraper.store_audio_file(np_signal, "dataSets", ".")
