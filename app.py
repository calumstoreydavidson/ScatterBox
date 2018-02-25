import anvil.server
from anvil_API_key import *
from random import *
import math
from main import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic
import colorsys



# {'dog': ('NOUN', '0.2', 128, 2)} POS, Information_content, Hue, position_in_sentence

sentences = []

@anvil.server.callable
def pass_sentences():
    return get_sentences()

@anvil.server.callable
def empty_sentences():
    global sentences
    for i in range(len(sentences)):
        sentences.pop()
    print(sentences)


def get_sentences():
    return sentences

@anvil.server.callable
def pass_rectangles(sentence):
    return get_rectangles(process_sentences(sentence))



def get_rectangles(words):
    print(words)
    i = 1
    rects = []
    for word in words:
        width, height = get_rectangle_dimensions(words[word][1])
        rgb = colorsys.hls_to_rgb((words[word][2] - 1)/360, 0.8, 0.8)
        r = "{0:0{1}x}".format(int(rgb[0] * 256), 2)
        g = "{0:0{1}x}".format(int(rgb[1] * 256), 2)
        b = "{0:0{1}x}".format(int(rgb[2] * 256), 2)
        color = '#' + r + g + b
        rect = {
            'x' : (i/len(words)) * random(),
            'y' : random(),
            'width' : width,
            'height' : height,
            'color' : color
        }
        print(rect)
        rects.append(rect)
        i += 1
    return rects

def get_rectangle_dimensions(IC):
    if IC > 60:
        IC = 60
    area = IC * IC * IC * IC
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

@anvil.server.http_endpoint("/user/:id")
def get_user(id, **params):
    resultFailure = {'message': 'Failure'}
    print(anvil.server.request.query_params['Body'])
    sentences.append(anvil.server.request.query_params['Body'])
    return resultFailure
    return "You requested user %s with params %s"

@anvil.server.http_endpoint('/sms/')
def sms(description, **qs):
    resultFailure = {'message': 'Failure'}
    #if anvil.server.request.method=="POST" and anvil.server.request.body is not None:
    #    print(anvil.request.query_params)
    print(dir(anvil.server))
    return resultFailure
    #number = request.form['From']
    #message_body = request.form['Body']
    #return message_body




if __name__ == '__main__':
    print(get_rectangles(process_sentences('This is a sentence')))
    verb_hue()

anvil.server.connect(anvil_key)
anvil.server.wait_forever()
