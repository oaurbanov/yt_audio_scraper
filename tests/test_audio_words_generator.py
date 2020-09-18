import pytest
import json
import os

from .context import audioscraper

DOWNLOADS_PATH = "./resources/scraper/downloads"
DS_PATH = "./resources/scraper/dataSets"
SCRAPED_VIDEOS_PATH = "./resources/scraper/dataSets/scraped_videos.json"

@pytest.mark.skip
def test_get_not_yet_scraped_videos():
    videos_to_scrap = [{'title': 'Jokes in Slow French - Learn French',
                        'id': '6EidHyDMH2Y',
                        'link': 'https://www.youtube.com/watch?v=6EidHyDMH2Y',
                        'automatic_captions_lang': True},
                       {'title': 'Jokes in Slow French - Learn French',
                        'id': '_Gxb0lsp53U',
                        'link': 'https://www.youtube.com/watch?v=_Gxb0lsp53U',
                        'automatic_captions_lang': True},
                       {'title': 'Jokes in Slow French - Learn French',
                        'id': 'p5Iuo2ySCh0',
                        'link': 'https://www.youtube.com/watch?v=p5Iuo2ySCh0',
                        'automatic_captions_lang': True}]
    scraped_videos = [{'title': 'Conversation in Slow French - Learn French',
                       'id': 'fFb4zm5D0Hg',
                       'link': 'https://www.youtube.com/watch?v=fFb4zm5D0Hg',
                       'automatic_captions_lang': True},
                      {'title': 'Jokes in Slow French - Learn French',
                       'id': '6EidHyDMH2Y',
                       'link': 'https://www.youtube.com/watch?v=6EidHyDMH2Y',
                       'automatic_captions_lang': True}]
    videos_not_yet_scraped = [{'title': 'Jokes in Slow French - Learn French',
                               'id': '_Gxb0lsp53U',
                               'link': 'https://www.youtube.com/watch?v=_Gxb0lsp53U',
                               'automatic_captions_lang': True},
                              {'title': 'Jokes in Slow French - Learn French',
                               'id': 'p5Iuo2ySCh0',
                               'link': 'https://www.youtube.com/watch?v=p5Iuo2ySCh0',
                               'automatic_captions_lang': True}]
    r = audioscraper.get_not_yet_scraped_videos(videos_to_scrap, scraped_videos, 1)
    assert r == videos_not_yet_scraped


def test_generate_audio_words_per_link():
    link = 'https://www.youtube.com/watch?v=6EidHyDMH2Y&list=PLyXyEQ98BGgvT7c63diejUEgHpyY2qKip'
    # videos_on_link = [{'title': 'Jokes in Slow French - Learn French',
    #                    'id': '6EidHyDMH2Y',
    #                    'link': 'https://www.youtube.com/watch?v=6EidHyDMH2Y',
    #                    'automatic_captions_lang': True},
    #                   {'title': 'Jokes in Slow French - Learn French',
    #                    'id': '_Gxb0lsp53U',
    #                    'link': 'https://www.youtube.com/watch?v=_Gxb0lsp53U',
    #                    'automatic_captions_lang': True},
    #                   {'title': 'Jokes in Slow French - Learn French',
    #                    'id': 'p5Iuo2ySCh0',
    #                    'link': 'https://www.youtube.com/watch?v=p5Iuo2ySCh0',
    #                    'automatic_captions_lang': True}]

    # Create scraped_videos json
    scraped_videos = [{'title': 'Conversation in Slow French - Learn French',
                       'id': 'fFb4zm5D0Hg',
                       'link': 'https://www.youtube.com/watch?v=fFb4zm5D0Hg',
                       'automatic_captions_lang': True},
                      {'title': 'Jokes in Slow French - Learn French',
                       'id': '_Gxb0lsp53U',
                       'link': 'https://www.youtube.com/watch?v=_Gxb0lsp53U',
                       'automatic_captions_lang': True},
                      {'title': 'Jokes in Slow French - Learn French',
                       'id': '6EidHyDMH2Y',
                       'link': 'https://www.youtube.com/watch?v=6EidHyDMH2Y',
                       'automatic_captions_lang': True}]

    with open(SCRAPED_VIDEOS_PATH, mode='w', encoding='utf8') as json_file:
        json.dump(scraped_videos, json_file, sort_keys=True, indent=4, ensure_ascii=False)

    assert audioscraper.generate_audio_words_per_link(link, 'fr', DOWNLOADS_PATH, DS_PATH, SCRAPED_VIDEOS_PATH)

