# yt_audio_scraper

It is an audio dataSet generator. For training Neural Networks

Just put the youtube video links in the json array under "links" key, and $.wav$ file with each pronunced word will be extracted.

In order to extract each word the video should have automatic-generated subtitles.
For better extractions, the videos should have audio with low noise and silence (70 ms) between words. 

# TODOs: 
- Implement some validation method, just 60% of generated audio_words are correct, when audio meets noise and silence criteria
- Implement "white list" of words I want to extract
- When storing audio_words, check current video has not been stored yet, save audio_words in having into account the video ID
- Get List of videos to extract from a link_playlist, it would more useful than the json

# Issues


-----------

Installing deps with conda:

```
conda install --name audio_env -c conda-forge youtube-dl
conda install --name audio_env -c conda-forge SpeechRecognition
conda install --name audio_env -c conda-forge google-cloud-texttospeech

conda install --name audio_env -c conda-forge google-cloud-sdk
conda install --name audio_env -c conda-forge google-api-python-client
---------------------

# Creating new env with python3.7

conda create --name audio_py37 python=3.7
conda activate audio_py37
conda install --name audio_env -c orc0 google-cloud-speech

conda install --name audio_py37 -c conda-forge youtube-dl

```


