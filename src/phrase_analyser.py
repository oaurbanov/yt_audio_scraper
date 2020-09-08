def clean_phrase(phrase):
    chars_to_replace = ["¡", "!", "\"", "#", "$", "%", "&", "(", ")", "*", "+", ",", ".", ";", ":", "?", "¿"]
    for char in chars_to_replace:
        phrase = phrase.replace(char, " ")
    phrase = phrase.replace("  ", " ")
    phrase = phrase.replace("  ", " ")
    if phrase[-1] == " ":
        phrase = phrase[0:-1]
    if phrase[-1] == "\n":
        phrase = phrase[0:-1]

    return phrase.lower()

def get_temptative_cuts(phrase, signal_phrase) :
    '''
    extract temptative cut indexes regarding size of each word in the phrase
    '''

    # I first clean the phrase
    phrase = clean_phrase(phrase)

    # find temptative cut positions
    total_len = 0
    for word in phrase.split(" "):
        total_len += len(word)
    temptative_cuts = [0]
    current_cut = 0
    for word in phrase.split(" ") :
        current_cut += round((len(word)/total_len) * (len(signal_phrase)))
        if current_cut >= len(signal_phrase) :
            current_cut = len(signal_phrase) -1
        temptative_cuts.append( current_cut )
        # print("word: ", word)
        # print("current_cut: ", current_cut)

    return temptative_cuts
