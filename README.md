# yt_audio_scraper

It is an audio dataSet generator. For training Neural Networks

Just put the youtube video links in the json array under "links" key, and $.wav$ file with each pronunced word will be extracted.

In order to extract each word the video should have automatic-generated subtitles.
For better extractions, the videos should have audio with no/low noise and silence between words. 

# TODOs: 
- Try to tweak audio_analyser parameters. Working just for "slow french" ID=fFb4zm5D0Hg
- Implement some validation method: just 60% of generated audio_words are correct
- When storing audio_words, check current video has not been stored yet, save audio_words in a diferent folder per video ID

# Issues


-----------

Installing deps with conda:

```
conda install --name audio_env -c conda-forge youtube-dl
```
