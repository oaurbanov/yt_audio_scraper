# -*- coding: UTF-8 -*-

import os
import re

import phrase_analyser

def get_secs(t_string):

    hours = t_string[0:2]
    minutes = t_string[3:5]
    secs = t_string[6:8]
    m_secs = t_string[8:12]

    secs_total = int(hours)*3600 + int(minutes)*60 + int(secs) + float(m_secs)
    # print(hours,",", minutes,",", secs ,",", m_secs)
    # print (secs_total)
    return secs_total



def get_time_diff(t1, t2):

    secs_diff =  round(get_secs(t2) - get_secs(t1), 3)
    # print("t2: ", t2, " t1: ", t1)
    # print("secs_diff : ", secs_diff)
    return secs_diff

def is_valid_text_line(line) :

    if line != "\n" and line != " \n" and not ("<c>" in line and "</c>" in line) :
        return True
    
    return False


# https://github.com/CoreyMSchafer/code_snippets/blob/master/Python-Regular-Expressions/snippets.txt
def get_phrases_and_timestamps_from_vtt(subs_file, phrases_dict):

    # get subs file as an array of lines
    with open(subs_file, mode='r') as fp:
        subs_lines = fp.readlines()

    # patterns that I will match later
    pattern_timestamps_line  = re.compile("(?P<time_begin>\d\d:\d\d:\d\d\.\d\d\d+) --> (?P<time_end>\d\d:\d\d:\d\d\.\d\d\d+)")

    # # pattern_word = re.compile("(^|\w)[a-zàâçéèêëîïôûùüÿñæœ'-]*(<)")
    # pattern_word = re.compile("(^|> )(?P<extracted_word>[a-zàâçéèêëîïôûùüÿñæœ'-]+)<")

    phrases_arr = []
    times_arr = []
    for i, (line) in enumerate (subs_lines) :

        # I first match timestamp_info "00:00:00.440 --> 00:00:02.140"
        matches_ts = pattern_timestamps_line.finditer(line)

        for match in matches_ts:
            # when I match for timestamp_info line, I check next_line and next_next_line are valid text line
            next_line = subs_lines[i+1]
            if is_valid_text_line(next_line) :

                tb = match.group('time_begin')
                te = match.group('time_end')
                times = (tb, te)

                # I filter ghost lines
                if get_time_diff(tb, te) > 0.1 : # secs

                    # next line after timestamp_info contains subs text, that can have several lines
                    phrase_text = next_line
                    # we just look for the next 4 lines
                    for k in range(1,5) :
                        if (i+1+k < len(subs_lines)) :
                            k_next_line = subs_lines[i+1+k]
                            if is_valid_text_line(k_next_line) :
                                phrase_text += k_next_line
                            else :
                                break
                    
                    # append phrase with its corresponding timestamps tuple
                    phrases_arr.append(phrase_analyser.clean_phrase(phrase_text))
                    times_arr.append(times)

    # appending each array per line
    phrases_dict['phrases'] = phrases_arr
    phrases_dict['timestamps'] = times_arr