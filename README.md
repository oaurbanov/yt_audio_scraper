# Youtube audio scraper

It is an audio dataSet generator. For training Neural Networks

Just put the youtube video links in the json array under "links" key, and $.wav$ file with each pronunced word will be extracted.

In order to extract each word the video should have automatic-generated subtitles.
For better extractions, the videos should have audio with low noise and silence (70 ms) between words. 

## TODOs: 
- Implement some validation method, just 60% of generated audio_words are correct, when audio meets noise and silence criteria
- Implement "white list" of words I want to extract
- When storing audio_words, check current video has not been stored yet, save audio_words in having into account the video ID
- Get List of videos to extract from a link_playlist, it would more useful than the json

## Deps:
```
# List enviroments and remove one
conda env list
conda env remove --name NAME_ENV

# Create enviroment with python3.7 and activate it
conda create --name audio_py37 python=3.7
conda activate audio_py37

# List packs in the current enviroment
conda list

# Install, update and remove pack in current enviroment
conda install -c conda-forge pydub
conda update pydub
conda remove pydub
```

## Refs:

- https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf