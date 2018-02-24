import anvil.server
from anvil_API_key import *

anvil.server.connect(anvil_key)

# {'dog': ('NOUN', '0.2', 128, 2)} POS, Information_content, Hue, position_in_sentence

@anvil.server.callable
def get_rectangles(words):
    for word in words:
        words[word]
