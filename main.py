from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic
from nltk.corpus.reader.wordnet import information_content
from nltk.tokenize import RegexpTokenizer
import nltk


brown_ic = wn_ic.ic("ic-brown.dat")
tokenizer = RegexpTokenizer(r'\w+')
noun_categories = {'animals': 24, 'body parts': 48, 'clothes': 72, 'colors': 96, 'days of the week': 120, 'food': 144,
                   'letters': 168, 'names': 192, 'numbers': 216, 'relatives': 240, 'rooms': 264, 'shapes': 288,
                   'sounds': 312, 'toys': 336, 'words': 360}

verb_categories = []


def process_sentences(input_text):
    sentences = input_text.split('.')
    for sentence in sentences:
        words = tokenizer.tokenize(sentence)
        tagged_words = pos_tag_input(words)

        # output_dict = # {'dog': ('NOUN', '0.2', 128, 2)} POS, Information_content, Hue, position_in_sentence
        # trashed_words = non noun/verbs - getting ignore for now
        output_dict, trashed_words = parse_tagged_words(tagged_words)

        # do stuff with DICT HERE !!!!!!!!!!!
        # TODO - this code needs to be above the calling server code
        # - for separating the sentences

        # debug - see output_dict outputs
        print('\n\nSentence: ', sentence)
        print("Non-Noun/Verbs Encountered!!!", trashed_words)
        print('Output: ', output_dict)
    return output_dict


def pos_tag_input(words):
    return nltk.pos_tag(words)


def parse_tagged_words(tagged_words):
    output_dict = {}
    trashed_words = []
    for i in range(len(tagged_words)):
        tag = tagged_words[i][1]
        word = tagged_words[i][0]
        # print("\nword:", word, " tag:", tag)

        word_info_content = parse_tagged_word(tag, trashed_words, word)

        if word_info_content is not None:
            output_dict[word] = [tag, word_info_content, 0, i]

        if len(output_dict.keys()) > 0:
            for word in output_dict.keys():
                best_noun = ['', 0]
                for noun in noun_categories.keys():
                    score = task_3_1_get_word_path_similarity(word, noun, 'res')
                    if best_noun[1] < score:
                        best_noun = [noun, score]
                output_dict[word][2] = noun_categories[best_noun[0]]
    return output_dict, trashed_words


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


def get_word_category(word):
    synset = wn.synsets(word)
    print("\nword: ", word, "synset: ", synset)
    for sense in synset:
        print("sense: ", sense)
        hypernyms = get_hypernyms(sense)
        print("hypernyms: ", hypernyms)
    return None


# from nltk.corpus import wordnet
# food = wordnet.synset('food.n.01')
# print(len(get_hypernyms(food))) # returns 1526


def get_hypernyms(sense):
    hypernyms = set()
    # print(sense.hypernyms())
    for hypernym in sense.hypernyms():
        hypernyms |= set(get_hypernyms(hypernym))
    return hypernyms | set(sense.hypernyms())


def task_3_1_get_word_path_similarity(word1, word2, sim_measure=None):
    synset1 = wn.synsets(word1)
    synset2 = wn.synsets(word2)
    best = 0
    for sense1 in synset1:
        for sense2 in synset2:
            similarity = 0
            if (sim_measure is not None and sense1.pos() == sense2.pos()) or sim_measure is None:
                similarity = get_sim_measure(sense1, sense2, sim_measure)
            if similarity is not None and similarity > best:
                best = similarity
    return best


def get_sim_measure(sense1, sense2, sim_measure=None):
    if sim_measure is None:
        return sense1.path_similarity(sense2)
    elif sim_measure == 'res':
        return sense1.res_similarity(sense2, brown_ic)
    elif sim_measure == 'lin':
        return sense1.lin_similarity(sense2, brown_ic)


if __name__ == '__main__':
    test_text = "The fat platypus sat upon the gnarled old tree for the night while " \
                "the curious seal swims across the vast ocean to read a book. the cow " \
                "was happy on the sunny day.The cow attacked the villagers on the sunny day." \
                "the book"
    input_text = test_text

    process_sentences(input_text)
