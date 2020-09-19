# Audio scraper

It is an audio dataSet generator. For training Neural Networks

Just put the video links (tested with youtube videos) in the json array under "links" key, and a .wav file with each pronounced word will be extracted.

In order to extract each word the video should have automatic-generated subtitles.
For better extractions, the videos should have audio with low noise and silence (70 ms) between words. 

## Repo tree
```

├── audioscraper   --> package
│   ├── scraper    --> extracts the audio_words, generates the DataSet
│   ├── validator  --> validates and cleans extracted audo_words in DataSet
│   └── controller --> handles the other packs for a standalone operation in a server
│   └── dictionary --> handles withe-list of most common audio_words per language
└── tests
    ├── context.py
    ├── test_audio_analyser.py
    ├── test_audio_subs_downloader.py
    ├── test_audio_words_generator.py
    ├── test_validator.py
    └── .tmp   --> temporal files for tests
    └── resources   --> resources for tests
        └── scraper
            └── dataSet  --> generated dataSet with test_audio_words_generator.py
                ├── one
                ├── two
                ├── three
                └── .scraped_videos_history.json  --> keeps register of scraped videos, to avoid data replication

```

## TODOs:
- Implement a proper logging class
- Improve path handling, and put main.py at audioscraper pack level
- Finish sub-pack dictionary. Consider also composed words (like j'ai)
- Implement the validator.recognize_from_signal. To predict directly from audio-chunks, without creating the audio file
- Fix audioscraper.validator for Google-cloud-speech
