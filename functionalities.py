import cPickle
import marshal
import os
import os.path
import RAKE
import operator
# import glob
# import pprint
# from rake_implementation import *
import sqlite3
import MySQLdb

# p = pprint.PrettyPrinter(indent=4)
db_conn = None
cursor = None
pickle_mapping_dictionary = open("mapping_dictionary.pkl", 'rb')
mapping = cPickle.load(pickle_mapping_dictionary)

try:

    # db_conn = sqlite3.connect('tags.db')
    # db_conn.isolation_level = None
    # print db_conn
    # print "$"*30
  db_conn = MySQLdb.connect(host="127.0.0.1",user= "root",passwd="root",db="tags")
    # db_conn.autocommit = True
except:
  print "connection not established"

cursor = db_conn.cursor()


# try:

#     dbc = sqlite3.connect('tags.db')
#     dbc.isolation_level = None
#     print dbc
#     print "$"*30
# except:
#     print "!"*30

# # cursor = dbc.cursor()
# # dbc.text_factory = str
###################################



def info():
    print "stats for total no. of tags and file count"
    print "insert_tag tags : syntax : insert_tag tag filepath "
    print "U for Union" + " syntax - U tag1 tag2 "
    print "I for Intersection" + " syntax - I tag1 tag2 "
    print "exit"


def stat():
    length = len(mapping)
    s = set(sum(mapping.values(), []))
    print "number of tags: " + str(length)
    print "number of files: " + str(len(s))



# method does not incorporate sql implementation
def insert_tag(tags):
    global mapping
    if len(tags)==1:
        print "tag should be entered followed by the filepath"
        return
    tag = tags[0]
    # print mapping
    if(tag not in mapping):
        # print "1"
        mapping[tag]=[]
    files = tags[1:]
    for file in files:
        if(os.path.isfile(file)):
            f,ext = os.path.splitext(file)
            ext = ext[1:].strip()
            if ext!='':
                if ext not in mapping:
                    # print "2"
                    mapping[ext]=[]
                if file not in mapping[ext]:
                    # print "3"
                    mapping[ext].append(file)
            file = os.path.abspath(file)
            if file not in mapping[tag]:
                # print "4"
                mapping[tag].append(file)
            print "tag successfully added"
        elif(os.path.exists(file)):
            for root, dirnames, files in os.walk(file):
                for file in files:
                    f, ext = os.path.splitext(file)
                    filepath = os.path.abspath(os.path.join(root, file))
                    ext = ext[1:].strip()
                    if ext!='':
                        if ext not in mapping:
                            mapping[ext]=[]
                        if filepath not in mapping[ext]:
                            mapping[ext].append(filepath)
                    if filepath not in mapping[tag]:
                        mapping[tag].append(filepath)
                    print "tag successfully added"
        else:
            print "can not associate tag as no such file found"
    pickle_file = open('mapping_dictionary.pkl', 'wb')
    cPickle.dump(mapping, pickle_file)
    pickle_file.close()


def union(tags):
    # global dbc
    # print dbc

    # cursor = dbc.cursor()
    # dbc.text_factory = str
    global db_conn
    global cursor

    # cursor = db_conn.cursor()
    temp2 = " ".join(tags)
    temp3 = temp2
    flag1 =False
    flag2 =False
    query = (""" select * from tags_files where tag_name = %s """)
    print "Results from pickle file:"
    if temp2 in mapping:
        print "tag found"
        print temp2+ ": " + str(mapping[temp2])
    # print "*"*30
    flag1=True
    # return


    for p in tags:
        if p in mapping:
            print p + ": " + str(mapping[p])
            flag2 = True

    if flag1  is False and flag2 is False:
        print "No file with this tag found"

    cursor.execute(query, (temp3,))
    results = cursor.fetchall()
    # cursor.close()
    print "Results from mysql:"
    for row in results:
    # print '@'*30
        print "%s : %s" % (row[1],repr(row[2]))
    words_of_phrase = temp3.split()
    # print words_of_phrase
    for word in words_of_phrase:
    #query = (""" select * from tags_files where tag_name = %s """)
    # cursor = db_conn.cursor()
        cursor.execute(query, (word,))
        r = cursor.fetchall()
        for row in r:
            # print '@'*30
            # print '^'*30
            print "%s : %s" % (row[1],repr(row[2]))
    #if temp in mapping:
    #print mapping[temp]
    # dbc.close()

    # cursor.close()
    # db_conn.close()
    # cursor.close()
    # cursor = db_conn.cursor()

    # cursor.execute('''select tag_name, tag_location  from tags_files where tag_name=?''',(tags,))
    # rows = cursor.fetchall()
    # for row in rows:
    #  print '@'*30
    #  print row

    # for word in tags:
    #  cursor.execute('''select tag_name, tag_location  from tags_files where tag_name=?''',(word,))
    #  r = cursor.fetchall()
    #  for row in r:
    #    print '@'*30
    #    print row
    # #if temp in mapping:
    #  #print mapping[temp]
    #  dbc.close()


# method does not incorporate sql implementation
def intersection(tags):
    s = set()
    flag=False
    for tag in tags:
        if tag in mapping:
            if flag==False:
                s = set(mapping[tag])
                flag=True
            else:
                s = s & set(mapping[tag])
        else:
            print "No file has all the tags entered"
            return
    
    for loc in s:
        print loc






operations = []
operations.append(('info', marshal.dumps(info.func_code)))
operations.append(('stats', marshal.dumps(stat.func_code)))
operations.append(('insert_tag', marshal.dumps(insert_tag.func_code)))
operations.append(('U', marshal.dumps(union.func_code)))
operations.append(('I', marshal.dumps(intersection.func_code)))




operations_dictionary = dict(operations)

pickle_file = open('functionalities_dictionary.pkl', 'wb')
cPickle.dump(operations_dictionary, pickle_file)
pickle_file.close()
