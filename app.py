import anvil.server
from anvil_API_key import *

anvil.server.connect(anvil_key)

# {'dog': ('NOUN', '0.2', 128)} POS, Information_content, Hue

@anvil.server.callable
