from sys import argv
from __data import gem 

if len(argv) > 1:
	startpath = argv[1]    
else : startpath = "D:/Karaoke alfa"

if len(argv) > 2:
    gem(startpath, argv[2])
else: gem(startpath)
