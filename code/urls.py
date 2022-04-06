import os
from parse import mainParser

directory = 'Apr2'

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        mainParser('Apr2/'+filename)
        continue
    else:
        continue
