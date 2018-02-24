import anvil.server
from anvil_API_key import *
from random import *
import math


anvil.server.connect(anvil_key)
anvil.server.wait_forever()

# {'dog': ('NOUN', '0.2', 128, 2)} POS, Information_content, Hue, position_in_sentence

@anvil.server.callable
def get_rectangles(words):
    i = 0
    rects = []
    for word in words:
        width, height = words[word][1]
        rect = {
            x : i/len(words) * random(),
            y : random(),
            width : width,
            height : height
        }
        rects.append(rect)

def get_rectangle_dimensions(IC):
    area = 10 * math.log(IC)
    side = math.sqrt(area)
    rectangleness = randint(-(int(side/2)), int(side/2))
    side1 = side - rectangleness
    side2 = area/side1
    return side1, side2
