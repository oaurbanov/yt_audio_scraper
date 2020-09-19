import os
import json

JSON_WHITE_LIST = os.path.join(os.path.dirname(__file__), 'FR/most_common_5000.json')


def is_word_white_listed(word, lang, enable=0):
    """
    Checks if a word belongs to a list of word to extract
    :param word: word string to check if it is whitelisted
    :param lang: language, for what the word will be check
    :param enable: for now this module IS DISABLED by default until finish it
    :return: True if word is in white-list, False if not
    """
    if not enable:
        return True

    if lang.lower() == 'fr':
        # TODO put this in another module, and consider to put in the list composed words also, like j'ai
        index_min = 0
        index_max = 500
        with open(JSON_WHITE_LIST, mode='r', encoding='utf8') as json_file:
            white_list = json.load(json_file)
            if word in white_list[index_min:index_max]:
                return True
        return False
    else:
        print("ERROR: not yet supported language")
        return True
