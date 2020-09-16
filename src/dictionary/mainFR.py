import textract
import json
import pprint


PDF_PATH = '../../resources/dictionary/freqDictFR.pdf'
JSON_OUTPUT = '../../resources/dictionary/FR/most_common_5000.json'
JSON_OUTPUT_BY_LISTS = '../../resources/dictionary/FR/common_by_lists.json'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# 1. Load PDF as string text
text = textract.process(PDF_PATH)
print(type(text))
print('length of string text: ')
print(len(text))

# 2. Organize text in pages
lines = text.split('\n')
print('lines on this text: ')
print(len(lines))
pages = []
lines_same_page = []
first_page_found = False
for line in lines:
    if "Page 1\n":
        first_page_found = True
    if first_page_found and "Page " in line and is_number(line[5:]) and line[5:] != "1":
        pages.append(lines_same_page)
        lines_same_page = []
    elif first_page_found:
        lines_same_page.append(line.lower())

# # 2.1. Print page 9, just to see it is ok
# print("\n--- total pages:")
# print(len(pages))  # index starts in 1, as 0 contains preface info
# print("\n--- page 9:")
# print(pages[9])
# print("\n----------\n")
# for line in pages[9]:
#     print(line)
# print("\n----------\n")

# 3. Extract 5000 most common words
common_words = []
last_index = 0  # To keep counting accordingly
last_index_vocab_list = 0
tuple_page_line_indexes_vocab_list = []  # [(page_index, line_index),...] for extracting vocabulary_lists
for page_index, page in enumerate(pages[9:258]):
    for line_index, line in enumerate(page):
        words = line.split(' ')
        if len(words) >= 2:
            if is_number(words[0]) and words[1] != '|':
                if float(words[0]) == last_index + 1:
                    # Extract the 5000 most common words
                    common_words.append(words[1])
                    last_index = float(words[0])
                elif float(words[0]) == last_index_vocab_list + 1:
                    # Extract the vocabulary lists, useful too
                    last_index_vocab_list = float(words[0])
                    tuple_page_line_indexes_vocab_list.append((page_index + 9, line_index))
                    # print(line)
print("\n--- total common_words:")
print(len(common_words))  # 5000

# 3.1. Print 30 first most common words, just to see it is ok
print("\n-------30 first most common_words:")
for word in common_words[:30]:
    print(word)

# 4.  Save json most_common_5000 words
with open(JSON_OUTPUT, mode='w') as json_file:
    json.dump(common_words, json_file, sort_keys=True, indent=4, ensure_ascii=False)

# 5.  Extract thematic vocabulary lists
vocab_list_dict = {}
for tuple_page_line in tuple_page_line_indexes_vocab_list:
    page_index = tuple_page_line[0]
    line_index = tuple_page_line[1]
    vocab_list_key = ''
    vocab_list_items = []
    for i, line in enumerate(pages[page_index]):
        if i >= line_index:
            words = line.split(' ')
            if len(words) >= 2:
                if i == line_index:  # key is here
                    vocab_list_key = ' '.join([word for word in words[1:]])
                elif len(words) >= 3:
                    if is_number(words[1]) and not '.' in words[0] and not ':' in words[0]:
                        if words[0][0] == '\x0c':
                            words[0] = words[0][1:]
                        vocab_list_items.append(words[0])
            elif len(words) == 1:  # Opposites: []  has just one word
                if words[0] != '|' and words[0] != '#' and words[0] != '' and not is_number(words[0]) \
                        and not '.' in words[0] and not ':' in words[0]:
                    if words[0][0] == '\x0c':
                        words[0] = words[0][1:]
                    vocab_list_items.append(words[0])
    # putting the extracted list into the dict, with its corresponding key
    if vocab_list_key != 'word length' and vocab_list_key != 'use of the pronoun "se"':  # not needed 2 lists
        vocab_list_dict[vocab_list_key] = vocab_list_items

# # 5.1. Print thematic vocabulary lists, just to see it is ok
# print("\n----------\n")
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(vocab_list_dict)

# 6.  Save thematic vocabulary lists json
with open(JSON_OUTPUT_BY_LISTS, mode='w') as json_file:
    json.dump(vocab_list_dict, json_file, sort_keys=True, indent=4, ensure_ascii=False)
