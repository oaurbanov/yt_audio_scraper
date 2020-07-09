

def get_temptative_cuts(phrase, signal_phrase) :
    '''
    extract temptative indexes regarding size of each word
    '''

    # I first clean the phrase
    chars_to_replace = ["¡", "!", "\"", "#", "$", "%", "&", "(", ")", "*", "+", ",", ".", ";", ":", "?", "¿"]
    for char in chars_to_replace:
        phrase = phrase.replace(char, " ")
    phrase = phrase.replace("  ", " ")
    phrase = phrase.replace("  ", " ")
    if (phrase[len(phrase)-1] == " ") :
        phrase = phrase[0:len(phrase)-2]
    if (phrase[len(phrase)-1] == "\n") :
        phrase = phrase[0:len(phrase)-2]

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
