from __future__ import absolute_import
from itertools import chain
from textblob.compat import basestring
from textblob.decorators import cached_property
from textblob.exceptions import FormatError
from textblob.tokenizers import word_tokenize
from textblob.utils import strip_punc, is_filelike

import textblob.formats as formats
from textblob.classifiers import *
from textblob import TextBlob
from textblob import Word
import MySQLdb
import nltk
#from nltk.tokenize import word_tokenize

from nltk.corpus import movie_reviews
#import words
import subprocess
import shlex
import itertools
from nltk.collocations import *
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from classification import *
from Bug_classifier import *
from Feature_Improvment_classifier import *
from Rating_classifier import *
from UserExperience_classifier import *


class Classification_System:

	def __init__(self):

		self.Bug_Classifier = Bug_classifier()
		self.Feature_Classifier = Feature_Improvment_classifier()
		self.UserExp_Classifer = UserExperience_classifier()
		self.Rating_Classifier = Rating_classifier()


	def Analyse_Review(self,text):
		print "Review:"
		print "************"
		print text
		print "************"
		self.Bug_Classifier.probability(text)
		print "************"
		self.Feature_Classifier.probability(text)
		print "************"
		self.Rating_Classifier.probability(text)
		print "************"
		self.UserExp_Classifer.probability(text)
		print "************"
		print "End of the Analysis"
		print "************"






def main():

	Classifier = Classification_System()
	#Classifier.Analyse_Review("it would be nice if you add the upload picture to the app ")

if __name__ == '__main__':
    main()





















