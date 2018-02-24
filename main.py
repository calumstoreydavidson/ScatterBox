from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic
from nltk.corpus.reader.wordnet import information_content
from nltk.tokenize import RegexpTokenizer
# from anvil_API_key import *
import nltk
# import anvil.server

# anvil.server.connect(anvil_key)

brown_ic = wn_ic.ic("ic-brown.dat")
tokenizer = RegexpTokenizer(r'\w+')


# @anvil.server.callable
# def get_rectangles(words):
#     for word in words:
#         words[word]


def main():
    test_text = "The fat platypus sat upon the gnarled old tree for the night while " \
                "the curious seal swims across the vast ocean to read a book. the cow " \
                "was happy on the sunny day.The cow attacked the villagers on the sunny day." \
                "the book"
    input_text = test_text

    process_sentences(input_text)


def process_sentences(input_text):
    sentences = input_text.split('.')
    for sentence in sentences:
        words = tokenizer.tokenize(sentence)
        tagged_words = pos_tag_input(words)

        # dict = # {'dog': ('NOUN', '0.2', 128, 2)} POS, Information_content, Hue, position_in_sentence
        # trashed_words = non noun/verbs - getting ignore for now
        dict, trashed_words = parse_tagged_words(tagged_words)

        # do stuff with DICT HERE !!!!!!!!!!!

        # debug - see dict outputs
        print('\n\nSentence: ', sentence)
        print("Non-Noun/Verbs Encountered!!!", trashed_words)
        print('Output: ', dict)


def pos_tag_input(words):
    return nltk.pos_tag(words)


def parse_tagged_words(tagged_words):
    dict1 = {}
    trashed_words = []
    for i in range(len(tagged_words)):
        tag = tagged_words[i][1]
        word = tagged_words[i][0]
        # print("\nword:", word, " tag:", tag)

        word_info_content = parse_tagged_word(tag, trashed_words, word)

        if word_info_content is not None:
            dict1[word] = [tag, word_info_content, 0, i]
    return dict1, trashed_words


def parse_tagged_word(tag, trashed_words, word):
    word_info_content = None
    if tag == "NN" or tag == "NNS":
        word_info_content = get_word_info_content(word, wn.NOUN)
    elif tag == "VBD":
        word_info_content = get_word_info_content(word, wn.VERB)
    else:
        trashed_words.append([word, tag])
        # print("Non-Noun/Verb Encountered!!!", [word, tag])
        # print(nltk.help.upenn_tagset(tag))
    return word_info_content


def get_word_info_content(word, tag_type):
    # print("\n", word, tag_type)
    s = wn.synsets(word, tag_type)[0]
    word_info_content = information_content(s, brown_ic)
    # print(word_info_content)
    return word_info_content


main()
