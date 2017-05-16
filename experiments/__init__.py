import os

from .test2 import *
from .inject_ditg import *

# TODO: scan and import functions from all files in this package automatically
# for m in os.listdir(os.path.dirname(__file__)):
#     if m == '__init__.py' or m[-3:] != '.py':
#         continue
#     print (m)
#     print (m[:-3])
#     __import__('.'+m[:-3])
