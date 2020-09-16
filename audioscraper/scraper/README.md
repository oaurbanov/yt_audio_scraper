# Scraper project

It is an audio dataSet generator. For training Neural Networks

Just put the youtube video links in the json array under "links" key, and $.wav$ file with each pronunced word will be extracted.

In order to extract each word the video should have automatic-generated subtitles.
For better extractions, the videos should have audio with low noise and silence (70 ms) between words. 


## Deps:

```
conda create --name scraper37 python=3.7
conda activate scraper37

conda install -c conda-forge youtube-dl
conda install -c conda-forge librosa

conda install -c anaconda pytest

conda install -c conda-forge pydub
conda install -c anaconda scipy
```