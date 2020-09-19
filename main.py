#!/usr/bin/python
import sys
import getopt

from audioscraper import scraper


def main(argv):
    link = ''
    lang = ''
    ds_path = ''
    try:
        opts, args = getopt.getopt(argv, "hi:l:o:", ["link=", "lang=", "ds_path="])
    except getopt.GetoptError:
        print('main.py -i "<link>" -l <lang> -o <ds_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i "<link>" -l <lang> -o <ds_path>')
            sys.exit()
        elif opt in ("-i", "--link"):
            link = arg
        elif opt in ("-l", "--lang"):
            lang = arg
        elif opt in ("-o", "--ds_path"):
            ds_path = arg

    scraper.generate_audio_words_per_link(link, lang, ds_path)


if __name__ == "__main__":
    main(sys.argv[1:])
