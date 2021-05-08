import pytest
import json
import os
import shutil

from audioscraper.scraper import audio_words_generator as awg

DS_PATH = os.path.join(os.path.dirname(__file__), 'resources/dataSet')
SCRAPED_VIDEOS_JSON_NAME = '.scraped_videos_history.json'


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
    r = awg.get_not_yet_scraped_videos(videos_to_scrap, scraped_videos, 1)
    assert r == videos_not_yet_scraped


# This is too big test to run it along with the other, Delete the mark to run it
# @pytest.mark.skip
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

    # first check the DS_PATH exist
    if not os.path.exists(DS_PATH):
        os.mkdir(DS_PATH)

    # create the .scraped_videos_history.json
    with open(os.path.join(DS_PATH, SCRAPED_VIDEOS_JSON_NAME), mode='w', encoding='utf8') as json_file:
        json.dump(scraped_videos, json_file, sort_keys=True, indent=4, ensure_ascii=False)

    # generating audio_words
    r = awg.generate_audio_words_per_link(link, 'fr', DS_PATH)

    # count audio_words generated, just folders, not files
    folder_names = []
    for root, dirs, files in os.walk(DS_PATH):
        folder_names = dirs
        break
    print(folder_names)  # ['lunettes', 'serveur', 'restaurant', 'description', 'pourriez', 'vidéo', 'justement', ...]
    assert r and len(folder_names) > 3

    # clean generated audio_words
    shutil.rmtree(DS_PATH)
