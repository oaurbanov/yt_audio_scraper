from setuptools import setup

setup(
    name='audioscraper',

    packages=[
        'audioscraper',
        'audioscraper.dictionary',
        'audioscraper.scraper',
        'audioscraper.validator',

    ],

    version='0.1',

    install_requires=[
        'youtube-dl',
        'pysoundfile',
        'matplotlib',
        'psutil',
        'SpeechRecognition'
    ],

    description="generates speech audio dataSets from youtube video links",

    author="Oscar Urbano",
    author_email="oaurbanov@unal.edu.co,

    license="Apache 2.0",

    python_requires=">=3.7",

    keywords=[
        "audio",
        "dataset",
        "downloader",
        "download",
        "youtube",
    ],

    entry_points={
        "console_scripts": ["audioscraper = audioscraper.__main__:console_entry_point"]
    }

)
