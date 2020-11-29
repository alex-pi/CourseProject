# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:26:02 2020

@author: Gang
"""
import numpy as np

import time
from collections import defaultdict
import csv
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import pickle
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt
from globals import DATA_PATH
import os

from sklearn.naive_bayes import MultinomialNB

# List of punctuation characters to scrub. Omits, the single apostrophe,
# which is handled separately so as to retain contractions.
PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '?', '"', '*', '\t', 'https', 'http']

SPECIAL_CHAR = ['{', '@', '\\', '=', '/']
# Carriage return strings, on *nix and windows.
CARRIAGE_RETURNS = ['\n', '\r\n']

STOP_WORD = ['www', 'com', 'and', 'www2', 'html', 'about', 'all', 'by']

SUPPERVISE_WORD = ['faculty', 'people', 'staff']

# Final sanity-check regex to run on words before they get
# pushed onto the core words list.
WORD_REGEX = "^[a-z']+$"

MIN_SUPPORT = 2
MIN_SUPPORT_MAX = 300


class ulr_faculty_classification:

    def __init__(self, data_file='TrainingDataSetTest.csv', trained_model_file='finalized_model.sav'):
        """
        Initialize empty document list.
        """
        self.base_path = DATA_PATH
        self.linkCorpus = []
        self.vocabulary = []
        self.likelihoods = []
        self.url_links = []
        self.labels = []
        self.url_tokens = []
        self.NgramTokenlists = []
        self.dictvocabulary = []
        self.data_path = os.path.join(self.base_path, data_file)
        self.trained_model_path = os.path.join(self.base_path, trained_model_file)
        self.term_doc_matrix = None
        self.document_topic_prob = None  # P(z | d)
        self.topic_word_prob = None  # P(w | z)
        self.topic_prob = None  # P(z | d, w)

        self.number_of_documents = 0
        self.vocabulary_size = 0
        self.SVMClassifier = None

        # If model exists try to load it from the start
        self.load_trained_model()

    def load_trained_model(self):
        try:
            with open(self.trained_model_path, 'rb') as mf:
                self.SVMClassifier = pickle.load(mf)
        except IOError:
            print("WARN: Trained model does not exists.")

    def readFile(self, file):
        '''
        (file) --->(label_list, URL list)
        return the list of label and the list of URL
        '''
        file_name = file
        rows = []
        # reading csv file 
        with open(file_name, 'r') as csvfile:
            #    creating a csv reader object
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
        return rows

    def build_labels(self, docs):
        '''
        (doc)--->label list
        return the list of labels
        '''
        y = np.zeros([len(docs)], dtype=np.int)
        index = 0
        for label in docs:
            y[index] = int(label[0])
            index += 1

        return y

    def getURL_linkfromTrainingDoc(self, trainingData):
        '''
        input: training dataset  (label, web_links)
        output: return a ulrlink list
        '''

        url_links = []
        for url in trainingData:
            url_links.append(url[1])

        return url_links

    def getURL_tokens(self, urlLink):
        """
        input: urlLink list
        output: token list for each ulr link
        """
        url_tokens = []
        filter_tokens = []
        for url in urlLink:
            for punc in PUNCTUATION + SPECIAL_CHAR:
                url = url.replace(punc, ".")
            url_tokens.append(url.split("."))

        # remove "" in url_tokens

        for tokens in url_tokens:
            temp_token = []
            for token in tokens:
                if token == "":
                    pass
                else:
                    temp_token.append(token.lower())
            filter_tokens.append(temp_token)

            # remove stop words
        filter_tokens = self.removeStopwords(filter_tokens)

        return filter_tokens

    def removeStopwords(self, wordlist):
        for word in wordlist:
            for punc in STOP_WORD:
                if punc in word:
                    word.remove(punc)
        return wordlist

    def getNgramToken(self, tokenlists):
        """
        input: token list
        output: return Ngram Token(extract faculty, people)
        """

        NgramTokenlists = []
        for tokenlist in tokenlists:
            NgramTokenlist = []
            for token in tokenlist:
                if "faculty" in token and (len(token) > len("faculty")):
                    NgramTokenlist.append("faculty")
                    token.replace("faculty", "")
                if "people" in token and (len(token) > len("people")):
                    NgramTokenlist.append("people")
                    token.replace("people", "")
                if "staff" in token and (len(token) > len("staff")):
                    NgramTokenlist.append("staff")
                    token.replace("staff", "")
                NgramTokenlist.append(token)

            NgramTokenlists.append(NgramTokenlist)

        return NgramTokenlists

    def build_vocabulary(self, NgramTokenlists):
        """
        Construct a list of unique words in the whole corpus. Put it in self.vocabulary
        for example: ["rain", "the", ...]
        return dic_vocabulary
        """

        vocabulary_list = self.freq_Volcabulary(NgramTokenlists)

        vocabulary = self.Apriori_prune(vocabulary_list, MIN_SUPPORT)
        self.vocabulary_size = len(vocabulary)
        return sorted(vocabulary)

    def freq_Volcabulary(self, Tokenlists):
        volcabulary_list = {}
        for Tokenlist in Tokenlists:
            for word in Tokenlist:
                if word in volcabulary_list and (len(word) > 2):
                    volcabulary_list[word] += 1
                elif len(word) > 2:
                    volcabulary_list[word] = 1
        return volcabulary_list

    def Apriori_prune(self, Ck, MinSupport):
        L = []

        for i in Ck:
            if Ck[i] >= MinSupport:
                L.append([i, Ck[i]])

        return sorted(L)

    def build_term_doc_matrix(self, docs_vocabulary, dict_vocabulary):
        """
        Construct the term-document matrix where each row represents a document, 
        and each column represents a vocabulary term.

        self.term_doc_matrix[i][j] is the count of term j in document i
        input: docs_vocabulary, the collection of links after ngram extract
               dict_vocabulary, the dictionary of vocabulary
        output:term_doc_matrix
               vocabulary_list
        """
        # ############################
        # your code here
        # ############################
        # build val dictionary

        number_of_documents = len(docs_vocabulary)
        vocabulary_size = len(dict_vocabulary)

        vocabulary_list = []
        for vocabulary in dict_vocabulary:
            vocabulary_list.append(vocabulary[0])

        term_doc_matrix = np.zeros([number_of_documents, vocabulary_size], dtype=np.float)

        d_index = 0
        for doc in self.NgramTokenlists:
            term_count = np.zeros(vocabulary_size, dtype=np.int)
            for word in doc:
                if word in vocabulary_list:
                    word_index = vocabulary_list.index(word)
                    term_count[word_index] += 1
            term_doc_matrix[d_index] = term_count
            d_index += 1

        return term_doc_matrix, vocabulary_list

    def getTestURLNgramToken(self, url_link):
        """
        input: token list
        output: return Ngram Token(extract faculty, people)
        """

        NgramTokenlists = []
        url_tokens = []

        for punc in PUNCTUATION + SPECIAL_CHAR:
            url_link = url_link.replace(punc, ".")
        url_tokens.append(url_link.split("."))

        for tokens in url_tokens:
            temp_token = []
            for token in tokens:
                if token == "":
                    pass
                else:
                    temp_token.append(token.lower())
            NgramTokenlists.append(temp_token)

        return NgramTokenlists

    def build_testLink_term_doc_matrix(self, TestURLNgramToken):

        test_vocabulary = self.freq_Volcabulary(TestURLNgramToken)

        number_of_documents = len(TestURLNgramToken)
        vocabulary_size = len(self.vocabulary)

        term_doc_matrix = np.zeros([number_of_documents, vocabulary_size], dtype=np.float)
        dict_test_vocabulary = []
        dict_test_vocabulary.append(test_vocabulary)

        d_index = 0
        for doc in dict_test_vocabulary:
            term_count = np.zeros(vocabulary_size, dtype=np.int)

            for word in doc:
                if word in self.vocabulary:
                    word_index = self.vocabulary.index(word)
                    term_count[word_index] = doc[word]
            term_doc_matrix[d_index] = term_count
            d_index += 1

        return term_doc_matrix

    def SVM_Classification(self):
        """
        
        train the SVM model
        Save the Model with pickle
        """
        # read training data from the file_path
        self.linkCorpus = self.readFile(self.data_path)
        # get the URL links from the training data
        self.url_links = self.getURL_linkfromTrainingDoc(self.linkCorpus)
        # get the label data from the training data
        self.labels = self.build_labels(self.linkCorpus)
        # get the url tokens from the URL link list
        self.url_tokens = self.getURL_tokens(self.url_links)
        # get the Ngram token from url_token
        self.NgramTokenlists = self.getNgramToken(self.url_tokens)
        # build the dictionary of the vocabulary
        self.dictvocabulary = self.build_vocabulary(self.NgramTokenlists)
        # build the term_doc_matrix and vocabulary lists
        self.term_doc_matrix, self.vocabulary = self.build_term_doc_matrix(self.NgramTokenlists, self.dictvocabulary)

        SVM = SVC(kernel='linear')
        # Train the SVM model
        self.SVMClassifier = SVM.fit(self.term_doc_matrix, self.labels)
        # save the SVM model to .sav file
        # filename = 'finalized_model.sav'
        pickle.dump(self.SVMClassifier, open(self.trained_model_path, 'wb'))

    def SVM_Predict(self, url):
        """
            input: url link
            output: predict label and the link
                    (1, ulr)
                    (0,none)
        """
        # load SVM model which we trained
        if self.SVMClassifier is None:
            self.load_trained_model()
        # filename = 'finalized_model.sav'
        # loaded_model = pickle.load(open(filename, 'rb'))
        test_token = self.getTestURLNgramToken(url)
        test_NgramTokenlists = self.getNgramToken(test_token)

        test_term_doc_matrix = self.build_testLink_term_doc_matrix(test_NgramTokenlists)

        predict_label = self.SVMClassifier.predict(test_term_doc_matrix)

        return predict_label


if __name__ == "__main__":
    print('The scikit-learn version is {}.'.format(sklearn.__version__))
    file_path = 'TrainingDataSetTest.csv'
    start_time = time.time()
    facultyClass = ulr_faculty_classification(file_path)
    # Train the SVM Model
    facultyClass.SVM_Classification()
    print("prediction label: 1 --- faculty directory, 0--- None")
    # Validate SVM Model
    dir_url = 'https://www.cs.arizona.edu/about/faculty'
    predict_labels = facultyClass.SVM_Predict(dir_url)
    print('URL prediction', predict_labels, "=", dir_url)
    dir_url = 'https://compbio.cornell.edu/people/faculty/'
    predict_labels = facultyClass.SVM_Predict(dir_url)
    print('URL prediction', dir_url, "=", predict_labels)
    # Model Validation
    file_path = 'TrainingTestingDataSet.csv'
    testClass = ulr_faculty_classification(file_path)
    testData = testClass.readFile(testClass.data_path)
    test_urls = testClass.getURL_linkfromTrainingDoc(testData)
    test_label = testClass.build_labels(testData)
    print(test_label)
    index = 0
    y_test = []
    for url in test_urls:
        predict_labels = facultyClass.SVM_Predict(url)
        y_test.append(predict_labels)
        if (predict_labels - test_label[index]) != 0:
            print(url, index, predict_labels)
        index = index + 1
    average_precision = average_precision_score(y_test, test_label)
    print('Average precision-recall score: {0:0.2f}'.format(
        average_precision))
    precision, recall, thresholds = precision_recall_curve(test_label, y_test)

    pr_display = PrecisionRecallDisplay(precision=precision, recall=recall).plot()
    print("--- %s seconds ---" % (time.time() - start_time))
