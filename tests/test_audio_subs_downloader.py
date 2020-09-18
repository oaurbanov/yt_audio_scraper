import pytest

from .context import audioscraper

# TODO snippet for custom compare dicts in the future
def cmp_dicts(dictionary1, dictionary2):
    try:
        for key in dictionary1.keys():
            if key in dictionary2.keys() and dictionary1[key] == dictionary2[key]:
                pass
            else:
                return False
        return True
    except KeyError:
        return False


def test_get_videos_infos_list_from_link_video():
    link = 'https://www.youtube.com/watch?v=fFb4zm5D0Hg'
    list_1 = [{'title': 'Conversation in Slow French - Learn French',
               'id': 'fFb4zm5D0Hg',
               'link': 'https://www.youtube.com/watch?v=fFb4zm5D0Hg',
               'automatic_captions_lang': True}]
    list_2 = audioscraper.get_videos_infos_list_from_link(link, 'fr')
    assert list_1[0] == list_2[0]


def test_get_videos_infos_list_from_link_playlist():
    # link_playlist = 'https://www.youtube.com/playlist?list=PLA5UIoabheFMYWWnGFFxl8_nvVZWZSykc' #  113
    link_playlist = 'https://www.youtube.com/watch?v=6EidHyDMH2Y&list=PLyXyEQ98BGgvT7c63diejUEgHpyY2qKip'
    list_1 = audioscraper.get_videos_infos_list_from_link(link_playlist, 'fr')
    print("Playlist total videos: ", len(list_1))  # Last time checked, it were 4
    print(list_1[0])
    assert len(list_1) > 0
