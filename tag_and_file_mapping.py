import cPickle
import os
import os.path
import RAKE
# import operator
# import pprint
# import marshal
# import types
# from rake_implementation import *
# import sqlite3
import timeit
import MySQLdb

start = timeit.default_timer()



try:
    # db_conn = sqlite3.connect('tags.db')
    # db_conn.isolation_level = None
    # print db_conn
    # print "$"*30
    db_conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root", db="tags")
    # db_conn.autocommit = True

except:
    print "connection not established"

cursor = db_conn.cursor()
# db_conn.text_factory = str



mapping = dict()
tags = {}

Rake = RAKE.Rake("english.txt")

os.chdir(".")

for root, dirnames, files in os.walk("."):
    
    for file in files:
        f, ext = os.path.splitext(file)
        if ext == ".txt":
            # rake = ImplementedRake()
            complete_path = os.path.abspath(os.path.join(root, file))
            with open(complete_path, 'r') as x:
                text = x.read()
                # keywords1 = rake.extract(text)
                keywords = Rake.run(text, 3, 4, 1)
                keywords = sorted(tupl[0] for tupl in keywords[:])
                for i in range(0, (len(keywords)/3)):

                    fpath = os.path.abspath(os.path.join(root, file))
                    if mapping.has_key(keywords[i]):
                        mapping[keywords[i]].append(fpath)
                        cursor.execute("insert into tags_files (tag_name, tag_location) values ('%s','%s')" % (keywords[i], complete_path.encode('string-escape')))
                        keys = keywords[i].split()
                        if len(keys) > 1:
                           
                            for ctr in keys:
                                if mapping.has_key(ctr):
                                    
                                    mapping[ctr].append(fpath)
                                    cursor.execute("insert into tags_files (tag_name, tag_location) values ('%s','%s')" % (ctr, complete_path.encode('string-escape')))
                                else:
                                    mapping[ctr] = []
                                    mapping[ctr].append(fpath)
                                    cursor.execute("insert into tags_files (tag_name, tag_location) values ('%s','%s')" % (ctr, complete_path.encode('string-escape')))
                                    

                        
                    else:
                        mapping[keywords[i]] = []
                        mapping[keywords[i]].append(fpath)
                        
                        cursor.execute("insert into tags_files (tag_name, tag_location) values ('%s','%s')" % (keywords[i], complete_path.encode('string-escape')))
                        keys = keywords[i].split()
                        if(len(keys) > 1):
                            
                            
                            for ctr in keys:
                                if mapping.has_key(ctr):
                                    
                                    mapping[ctr].append(fpath)
                                    cursor.execute("insert into tags_files (tag_name, tag_location) values ('%s','%s')" % (ctr, complete_path.encode('string-escape')))
                                else:
                                    mapping[ctr] = []
                                    mapping[ctr].append(fpath)
                                    cursor.execute("insert into tags_files (tag_name, tag_location) values ('%s','%s')" % (ctr, complete_path.encode('string-escape')))
                                    


    ext = ext[1:]
    fpath = os.path.abspath(os.path.join(root, file))
    print fpath
    if ext not in mapping:
        mapping[ext]=[]
    mapping[ext].append(fpath)
    cursor.execute("insert into tags_files (tag_name, tag_location) values ('%s','%s')" % (ext, fpath.encode('string-escape')))
    db_conn.commit()
# cursor.execute("select * from tags_files")
# results = cursor.fetchall()
# for row in results:
#     print row[1], row[2]
# db_conn.close()

pickle_file = open('mapping_dictionary.pkl', 'wb')
cPickle.dump(mapping, pickle_file)


print timeit.default_timer()-start