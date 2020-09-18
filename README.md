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
- Implement sub-pack for white_listing words. To generate the main words to extract. Having also composed words (like j'ai)
- Implement the validator.recognize_from_signal. To predict directly from audio-chunks, without creating the audio file
- Fix audioscraper.validator for Google-cloud-speech
