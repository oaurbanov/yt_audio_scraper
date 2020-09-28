# Audio scraper

It is an audio dataSet generator. For training Neural Networks

Just pass the video/playlist link (tested with youtube videos) and a dataSet will be generated with a .wav file per each pronounced word

In order to extract each word the video should have .vtt subtitles (automatically generated in Youtube).
For better extractions, the videos should have clear and intelligible audio. Typically, with 70 ms silence between words. 


## Quick start
```
python setup.py develop
python audioscraper -i 'https://www.youtube.com/watch?v=fFb4zm5D0Hg' -l fr -o ./dataSet
```


## Repo tree
```

├── audioscraper   --> package
│   ├── scraper    --> extracts the audio_words, generates the DataSet
│   ├── validator  --> validates and cleans extracted audo_words in DataSet
│   └── dictionary --> handles withe-list of most common audio_words per language
└── tests
    ├── test_audio_analyser.py
    ├── test_audio_subs_downloader.py
    ├── test_audio_words_generator.py
    ├── test_validator.py
    └── resources   --> resources for tests
        └── conversation.wav  --> resource to test validator.py
        └── dataSet  --> generated dataSet with test_audio_words_generator.py
            ├── one
            ├── two
            ├── three
            └── .scraped_videos_history.json  --> keeps register of scraped videos, to avoid data replication

```


## TODOs:
- Implement a proper logging class
- Finish sub-pack dictionary. Consider also composed words (like j'ai)
- Implement the validator.recognize_from_signal. To predict directly from audio-chunks, without creating the audio file
- Fix audioscraper.validator for Google-cloud-speech
