import cPickle
import marshal
import types
import os
from subprocess import call
import RAKE
import operator

# import pprint
from functionalities import insert_tag
from functionalities import db_conn
from functionalities import cursor


# p = pprint.PrettyPrinter(indent=4)

call(["python","tag_and_file_mapping.py"])

call(["python","functionalities.py"])



pickle_mapping_dictionary = open("mapping_dictionary.pkl", 'rb')
mapping = cPickle.load(pickle_mapping_dictionary)


pickle_file = open('functionalities_dictionary.pkl', 'rb')
operations = cPickle.load(pickle_file)

while(True):
    inp = raw_input('enter command#: ')
    inp = inp.strip()
    inp = inp.split(' ')
    if (inp[0] == 'exit'):
        print "Bye!"
        break
    if(inp[0] in operations):
        func = types.FunctionType(marshal.loads(operations[inp[0]]), globals(), "something")
        if(len(inp)>1):
            func(inp[1:])

        else:
            func()
    else:
        print "incorrect operation entered, try again"
