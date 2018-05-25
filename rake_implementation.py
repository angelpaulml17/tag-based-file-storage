from __future__ import division
import os

import operator

import nltk

import cPickle


def checkIfPunctuation(word):
    flag1 = False
    flag2 = False
    myPunctuationSet = {'!', '(', ')', '-', '[', ']', '{', '}', ';', ':', '"', '\\', '<', '>', '.', '/', '?', '@', '#',
                        '$', '%', '^', '&', '*', '_', '~', '\'', '`'}
    # punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    if (len(word) < 2):
        flag1 = True
    if word in myPunctuationSet:
        flag2 = True
    return flag1 and flag2


def checkIfNumber(word):
    # if word.isdigit() == True:
    #   print word
    return word.isdigit()


class ImplementedRake:
    def __init__(self):
        # print len(nltk.corpus.stopwords.words())
        self.stopwords = self.stopWordList()
        self.select_Keywords = 1 / 3  # proportion of selected keywords for attaching to files

    def extract(self, text):
        # making sentences out of text
        listOfSentences = nltk.sent_tokenize(text)
        # getting possible phrase keywords
        listOfPhrases = self.possibleKeywords(listOfSentences)
        # calculating the scores of words in the phrase
        scoreOfWord = self.scoreOfWord(listOfPhrases)
        # calculating the score of phrases using the score of its words
        scoreOfPhrase = self.scoreOfPhrase(listOfPhrases, scoreOfWord)
        # sorting the scores of phrases in reverse according to the score
        sorted_scoreOfPhrase = sorted(scoreOfPhrase.iteritems(),
                                      key=operator.itemgetter(1), reverse=True)
        # counting the number of scores
        countOfPhrases = len(sorted_scoreOfPhrase)

        return map(lambda lst: lst[0], sorted_scoreOfPhrase[0:int(countOfPhrases * self.select_Keywords)])

    def stopWordList(self):
        return set(nltk.corpus.stopwords.words())

    def possibleKeywords(self, listOfSentences):
        listOfPhrases = []
        for sentence in listOfSentences:
            words = self.tokenizeNltk(sentence)
            # print words
            phrase = []
            for word in words:
                if word == "stopword" or checkIfPunctuation(word):
                    if len(phrase) > 0:
                        listOfPhrases.append(phrase)
                        phrase = []
                else:
                    phrase.append(word)
        return listOfPhrases

    def tokenizeNltk(self, sentence):
        return map(lambda possibleStopword: "stopword" if possibleStopword in self.stopwords else possibleStopword,
                   nltk.word_tokenize(sentence.lower()))

    def scoreOfPhrase(self, listOfPhrases, scoreOfWord):
        scoreOfPhrase = {}
        for phrase in listOfPhrases:
            phrase_score = 0
            for word in phrase:
                # score of phrase is equal to the sum of scores of its words
                phrase_score = phrase_score + scoreOfWord[word]
            scoreOfPhrase[" ".join(phrase)] = phrase_score
            # print scoreOfPhrase
        return scoreOfPhrase

    def degreeCount(self, phrase):
        ctr = len(filter(lambda notWord: not checkIfNumber(notWord) and not checkIfPunctuation(notWord), phrase)) - 1
        return ctr

    def scoreOfWord(self, listOfPhrases):
        frequencyOfWord = self.initNltkFreqDist()
        degreeOfWord = self.initNltkFreqDist()
        for phrase in listOfPhrases:
            # degree is the number of words in the phrase - number of numbers in the phrase - number of punctuations in the phrase
            degree = self.degreeCount(phrase)
            for word in phrase:
                frequencyOfWord.update([word])
                degreeOfWord.update([word, degree])
        # print phrase
        #     print "__________________________________"
        #     print str(word) + " : " + str(degree)  # other words

        # print frequencyOfWord
        # print "*"*30
        # print degreeOfWord

        for word in frequencyOfWord.keys():
            degreeOfWord[word] = degreeOfWord[word] + frequencyOfWord[word]  # itself
        # score of a word will be its degree divided by frequency
        scoreOfWord = {}
        for word in frequencyOfWord.keys():
            scoreOfWord[word] = degreeOfWord[word] / frequencyOfWord[word]

        for word in scoreOfWord:
            scoreOfWord[word] = scoreOfWord[word] / 100

        return scoreOfWord

    def initNltkFreqDist(self):
        return nltk.FreqDist()

    def rake_test(self):

        rake = ImplementedRake()
        files = []
        tags = {}
        keywords = rake.extract("""
    Located smack-dab in the middle of the brain, these clusters, or nuclei, each send signals to a different area of the brain, igniting opposite behaviors in the face of a visual threat. By selectively altering the activation levels of the two nuclei, the investigators could dispose the mice to freeze or duck into a hiding space, or to aggressively stand their ground, when approached by a simulated predator.
    """)
        print keywords
        # os.chdir("D:\RAKE")
        # file1 = open(r'sample.txt')
        # for file in glob.glob("*.txt"):
        #   files.append(file)
        #   print file

        # for file in files:
        #   with open(file, 'r') as x:
        #       text = x.read()
        #       keywords = rake.extract(text)
        #       keywords = keywords[:3]
        #       tags[file] = keywords
        #       file_map_tag[file] = tags[file]
        #       print file_map_tag[file]
        #       #print tags[file]

    '''
   for x in files:
    temp = open(r'x')
    text = temp.read()
    keywords = rake.extract(text)
    keywords = keywords[:3]
    tags[x] = keywords
  '''
    '''
  for x in files:
    text = x.read()
    keyword
  #file1 = open(r'D:\RAKE\sample.txt')
  '''
    # text = file1.read()
    # keywords1 = rake.extract(text)
    # print keywords1[:3]


if __name__ == "__main__":
    r = ImplementedRake()
    r.rake_test()

'''
import RAKE
import operator
import pprint
import glob
import os
p = pprint.PrettyPrinter(indent=4)
files = []
tags={}

os.chdir("tech/")

for file in glob.glob("*.txt"):
   files.append(file)

Rake = RAKE.Rake("../english.txt")


for file in files:
    with open(file, 'r') as x:
        tags[file] = Rake.run(x.read(),2,2,3)
p.pprint(tags)
'''