import anvil.server
from anvil_API_key import *
from random import *
import math
from main import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic



# {'dog': ('NOUN', '0.2', 128, 2)} POS, Information_content, Hue, position_in_sentence


@anvil.server.callable
def pass_rectangles(sentence):
    return get_rectangles(process_sentences(sentence))


def get_rectangles(words):
    i = 1
    rects = []
    for word in words:
        print(get_rectangle_dimensions(words[word][1]))
        width, height = get_rectangle_dimensions(words[word][1])
        rect = {
            'x' : (i/len(words)) * random(),
            'y' : random(),
            'width' : width,
            'height' : height
        }
        print(rect)
        rects.append(rect)
        i += 1
    return rects

def get_rectangle_dimensions(IC):
    if IC > 60:
        IC = 60
    area = IC * 200
    side = math.sqrt(area)
    rectangleness = randint(-(int(side/2)), int(side/2))
    side1 = side - rectangleness
    side2 = area/side1
    return side1 , side2

def verb_hue():
    lemma = WordNetLemmatizer()
    lemma.lemmatize('was', 'v')
    print('verb lemma', lemma.lemmatize('was', 'v'))
    print(wn.synsets(lemma.lemmatize('existed', 'v')))

if __name__ == '__main__':
    print(get_rectangles(process_sentences('This is a sentence')))
    verb_hue()

anvil.server.connect(anvil_key)
anvil.server.wait_forever()
