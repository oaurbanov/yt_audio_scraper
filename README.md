# Audio scraper

It is an audio dataSet generator. For training Neural Networks

Just put the video links (tested with youtube videos) in the json array under "links" key, and a .wav file with each pronunced word will be extracted.

In order to extract each word the video should have automatic-generated subtitles.
For better extractions, the videos should have audio with low noise and silence (70 ms) between words. 

## Pack tree
```

├── audioscraper   --> package
│   ├── scraper    --> extracts the audio_words, generates the DataSet
│   ├── validator  --> validates and cleans extracted audo_words in DataSet
│   └── controller --> handles the other packs for a standalone operation in a server
│
├── resources
│   └── dictionary
│       └── FR    --> withe list of french audio words to extract
│
└── tests
    ├── context.py
    ├── test_audio_analyser.py
    ├── test_scraper.py
    ├── test_validator.py
    └── resources          --> resources for the tests
        └── scraper
            ├── dataSets   --> generated dataSet with test_scraper.py
            │   ├── one
            │   ├── two
            │   └── three
            ├── downloads
            │   ├── audios
            │   └── subs
            └── video_links.json  --> contains links of videos to scrape

```

## TODOs:

- When storing audio_words, check current video has not been stored yet, save audio_words in having into account the video ID
- Get List of videos to extract from a link_playlist, it would more useful than the json
- Fix audioscraper.validator for Google-cloud-speech
