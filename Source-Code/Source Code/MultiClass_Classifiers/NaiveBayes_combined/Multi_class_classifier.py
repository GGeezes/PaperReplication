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

from nltk.corpus import movie_reviews
import subprocess
import shlex
import itertools
from nltk.collocations import *
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from classification import *

def _get_words_from_dataset(dataset):

    def tokenize(words):
        if isinstance(words, basestring):
            return word_tokenize(words, include_punc=False)
        else:
            return words
    all_words = chain.from_iterable(tokenize(words) for words, _ in dataset)
    return set(all_words)

def _get_document_tokens(document):
    if isinstance(document, basestring):
        tokens = set((strip_punc(w, all=False)
                    for w in word_tokenize(document, include_punc=False)))
    else:
        tokens = set(strip_punc(w, all=False) for w in document)
    return tokens
    
class Multi_class_classifier:


    def __init__(self):

        db = MySQLdb.connect(host="127.0.0.1", 
                     user="root", 
                      db="re2015_training_set") 

        db.autocommit(True)
        db.begin()
        cur = db.cursor()
        self.db = db
        self.cur = cur 
        self.train ,self.rating_dict , self.test , self.senti_dict , self.senti_pos_dict ,self.senti_neg_dict ,self.present_simple_dict ,self.past_simple_dict ,self.future_dict ,self.present_con_dict = Multi_class_classifier.classifier_fetch_data(self)
        print('Training the Classifier')
        cl = NaiveBayesClassifier(self.train , feature_extractor = self.extractor)
        self.classifer = cl
        print cl.show_informative_features(10)
        print('Testing the accuracy of the classifier')
        print self.accuracy(self.classifer,self.test)
        self.db.commit()
        self.db.close()

    def classifier_fetch_data(self):
        train = []
        rating_dict = {}
        senti_dict = {}
        senti_pos_dict = {}
        senti_neg_dict = {}
        present_simple_dict = {}
        past_simple_dict = {}
        future_dict = {}
        present_con_dict = {}
        test = []

        self.cur.execute("SELECT * FROM Bug_Report_Data_Train " )

        for row in self.cur.fetchall() :
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore')) 
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})

            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})
            train.append((decoded_row, 'bug'))

        self.cur.execute("SELECT * FROM Bug_Report_Data_Test ")

        for row in self.cur.fetchall() :
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})
            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore'))
            test.append((decoded_row, 'bug'))

        self.cur.execute("SELECT * FROM Feature_OR_Improvment_Request_Data_Train " )

        for row in self.cur.fetchall() :
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore')) 
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})
            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})
            train.append((decoded_row, 'feature_improvment'))

        self.cur.execute("SELECT * FROM Feature_OR_Improvment_Request_Data_Test ")

        for row in self.cur.fetchall() :
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})
            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore'))
            test.append((decoded_row, 'feature_improvment'))



        self.cur.execute("SELECT * FROM Rating_Data_Train " )

        for row in self.cur.fetchall() :
            
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore')) 
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})
            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})

            train.append((decoded_row, 'rating'))
            train.append((decoded_row_1, 'rating'))

        self.cur.execute("SELECT * FROM Rating_Data_Test ")

        for row in self.cur.fetchall() :
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})
            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore'))
            test.append((decoded_row, 'rating'))

        self.cur.execute("SELECT * FROM UserExperience_Data_Train " )

        for row in self.cur.fetchall() :
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore')) 
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})
            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})

            train.append((decoded_row, 'UserExperience'))
            train.append((decoded_row_1, 'UserExperience'))

        self.cur.execute("SELECT * FROM UserExperience_Data_Test ")

        for row in self.cur.fetchall() :
            decoded_row = str(row[4])
            decoded_row_1 = str(row[3])
            rating = row[5]
            sentiScore = row[13]
            senti_pos = row[14]
            senti_neg = row[15]
            present_simple = row[19]
            present_con = row [20]
            past_simple = row[21]
            future = row[22]
            if present_simple:
                present_simple = float(int(present_simple))
                present_simple_dict.update({decoded_row: present_simple})
            if present_con:
                present_con = float(int(present_con))
                present_con_dict.update({decoded_row: present_con})
            if past_simple:
                past_simple = float(int(past_simple))
                past_simple_dict.update({decoded_row: past_simple})
            if future:
                future = float(int(future))
                future_dict.update({decoded_row: future})
            if rating:
                rating = float(rating)
                rating = int(rating)
                rating_dict.update({decoded_row: rating})
                rating_dict.update({decoded_row_1: rating})
            senti_dict.update({decoded_row: sentiScore})
            senti_pos_dict.update({decoded_row: senti_pos})
            senti_neg_dict.update({decoded_row: senti_neg})
            decoded_row = str(decoded_row.decode('utf-8',errors = 'ignore'))
            decoded_row_1 = str(decoded_row_1.decode('utf-8',errors = 'ignore'))
            test.append((decoded_row, 'UserExperience'))



        

        self.db.commit()

        return train , rating_dict , test , senti_dict , senti_pos_dict , senti_neg_dict , present_simple_dict , past_simple_dict ,future_dict ,present_con_dict

    def basic_extractor(self , document):
        """A basic document feature extractor that returns a dict indicating
        what words in ``train_set`` are contained in ``document``.

        :param document: The text to extract features from. Can be a string or an iterable.
        :param list train_set: Training data set, a list of tuples of the form
            ``(words, label)``.
        """
        train_set = self.train
        word_features =_get_words_from_dataset(train_set)
        tokens =_get_document_tokens(document)
        features = dict(((u'contains({0})'.format(word), (word in tokens))
                                                for word in word_features))
        return features

    def contains_extractor(self,document):
        """A basic document feature extractor that returns a dict of words that
        the document contains.
        """
        tokens = _get_document_tokens(document)
        features = dict((u'contains({0})'.format(w), True) for w in tokens)
        return features

    def rating_length_extractor(self,document):
        train_set = self.train
        rating_dict = self.rating_dict
        feats = {}
        document_length = len(document)
        feats["rating({0})".format(rating_dict.get(document))]= True
        #feats["length({0})".format(document_length)] = True
        return feats


    def accuracy(self,classifier_n,test_set, format=None):
        """Compute the accuracy on a test set.

        :param test_set: A list of tuples of the form ``(text, label)``, or a
            file pointer.
        """
        test_data = test_set
        test_features = [(classifier_n.extract_features(d), c) for d, c in test_data]
        nb_precisions,nb_recalls ,nb_f = precision_recall_F_Measure(classifier_n,test_data)

        print "Precisions_bug :"
        print nb_precisions['bug']
        print "Recalls_bug :"
        print nb_recalls['bug']
        print "F-measure_Bug"
        print nb_f['bug']
        print "Precisions_feature_improvment :"
        print nb_precisions['feature_improvment']
        print "Recalls_feature_improvment :"
        print nb_recalls['feature_improvment']
        print "F-measure_feature_improvment"
        print nb_f['feature_improvment']
        print "Precisions_UserExperience :"
        print nb_precisions['UserExperience']
        print "Recalls_UserExperience :"
        print nb_recalls['UserExperience']
        print "F-measure_UserExperience"
        print nb_f['UserExperience']
        print "Precisions_rating:"
        print nb_precisions['rating']
        print "Recalls_rating :"
        print nb_recalls['rating']
        print "F-measure_rating"
        print nb_f['rating']
        print "Accuracy:"
        return nltk.classify.accuracy(classifier_n.classifier, test_features)




    def extractor(self,document):
        
        feats = {}
        #score_fn=BigramAssocMeasures.chi_sq
        #score_fn = bigram_measures.pmi
        #n=200
        #stopset = set(stopwords.words('english'))
        tokens = nltk.word_tokenize(document)
        length_words = len(tokens)
        train_set = self.train
        rating_dict = self.rating_dict
        senti_dict = self.senti_dict
        senti_pos_dict = self.senti_pos_dict
        senti_neg_dict = self.senti_neg_dict
        present_simple_dict = self.present_simple_dict
        present_con_dict = self.present_con_dict
        past_simple_dict = self.past_simple_dict
        future_dict = self.future_dict


        word_features = _get_words_from_dataset(train_set)
        tokens = _get_document_tokens(document)
        features = dict(((u'contains({0})'.format(word), (word in tokens))
                                                for word in word_features))

        #bigram_finder = BigramCollocationFinder.from_words(word_tokenize(document))
        #bigrams = bigram_finder.nbest(score_fn, n)
        #features = dict([(ngram, True) for ngram in itertools.chain(document, bigrams)])
        feats["rating({0})".format(rating_dict.get(document))]= True
        feats["length({0})".format(length_words)] = True
        feats["senti_Score({0})".format(senti_dict.get(document))] = True
        v1 = 0
        v2 = 0
        v3 = 0 
        v4 = 0
        if present_simple_dict.get(document):
            v1 = int(float(present_simple_dict.get(document)))
        if present_con_dict.get(document):
            v2 = int(float(present_con_dict.get(document)))
        if past_simple_dict.get(document):
            v3 =  int(float(past_simple_dict.get(document)))
        if future_dict.get(document):
            v4 = int(float(future_dict.get(document)))

        total_verbs = int(v1+v2+v3+v4)
        if v1 > 0 :
            feats["include_present_simple({0})".format(v1/float(total_verbs))] = True   
        if v2 > 0 :
            feats["include_present_con({0})".format(v2/float(total_verbs))] = True
        if v3 > 0 :
            feats["include_past_simple({0})".format(v3/float(total_verbs))] = True
        if v4 > 0 :
            feats["include_future({0})".format(v4/float(total_verbs))] = True

        #feats["senti_Score_pos({0})".format(senti_pos_dict.get(document))] = True
        #feats["senti_Score_neg({0})".format(senti_neg_dict.get(document))] = True  


        output_features = dict(feats.items() + features.items())

        return output_features

    def probability(self,text):
        prob_dist = self.classifer.prob_classify(text)
        print "probaility of having a rating review"  
        print prob_dist.prob("rating")
        print "classified as :"
        print prob_dist.max()


def main():
    Classifier = Multi_class_classifier()


if __name__ == '__main__':
    main()




    


