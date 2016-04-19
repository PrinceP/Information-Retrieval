from __future__ import print_function
import six.moves.cPickle as pickle

from collections import OrderedDict
import copy
import gzip
import os
import urllib
import random
import stat
import subprocess
import sys
import timeit

import numpy

import theano
from theano import tensor as T

import sys
sys.setrecursionlimit(1500)

PREFIX = os.getenv(
    'ATISDATA',
    os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0],
                 'data'))

def atisfold(fold):
    assert fold in range(5)
    filename = os.path.join(PREFIX, 'atis.fold'+str(fold)+'.pkl.gz')
    f = gzip.open(filename, 'rb')
    try:
        train_set, valid_set, test_set, dicts = pickle.load(f, encoding='latin1')
    except:
        train_set, valid_set, test_set, dicts = pickle.load(f)
    return train_set, valid_set, test_set, dicts



# utils functions
def shuffle(lol, seed):
    '''
    lol :: list of list as input
    seed :: seed the shuffling

    shuffle inplace each list in the same order
    '''
    for l in lol:
        random.seed(seed)
        random.shuffle(l)


# start-snippet-1
def contextwin(l, win):
    '''
    win :: int corresponding to the size of the window
    given a list of indexes composing a sentence

    l :: array containing the word indexes

    it will return a list of list of indexes corresponding
    to context windows surrounding each word in the sentence
    '''
    assert (win % 2) == 1
    assert win >= 1
    l = list(l)

    lpadded = win // 2 * [-1] + l + win // 2 * [-1]
    out = [lpadded[i:(i + win)] for i in range(len(l))]

    assert len(out) == len(l)
    return out
# end-snippet-1


class RNNSLU(object):
    ''' elman neural net model '''
    def __init__(self, nh, nc, ne, de, cs):
        '''
        nh :: dimension of the hidden layer
        nc :: number of classes
        ne :: number of word embeddings in the vocabulary
        de :: dimension of the word embeddings
        cs :: word window context size
        '''
        # parameters of the model
        self.emb = theano.shared(name='embeddings',
                                 value=0.2 * numpy.random.uniform(-1.0, 1.0,
                                 (ne+1, de))
                                 # add one for padding at the end
                                 .astype(theano.config.floatX))
        self.wx = theano.shared(name='wx',
                                value=0.2 * numpy.random.uniform(-1.0, 1.0,
                                (de * cs, nh))
                                .astype(theano.config.floatX))
        self.wh = theano.shared(name='wh',
                                value=0.2 * numpy.random.uniform(-1.0, 1.0,
                                (nh, nh))
                                .astype(theano.config.floatX))
        self.w = theano.shared(name='w',
                               value=0.2 * numpy.random.uniform(-1.0, 1.0,
                               (nh, nc))
                               .astype(theano.config.floatX))
        self.bh = theano.shared(name='bh',
                                value=numpy.zeros(nh,
                                dtype=theano.config.floatX))
        self.b = theano.shared(name='b',
                               value=numpy.zeros(nc,
                               dtype=theano.config.floatX))
        self.h0 = theano.shared(name='h0',
                                value=numpy.zeros(nh,
                                dtype=theano.config.floatX))

        # bundle
        self.params = [self.emb, self.wx, self.wh, self.w,
                       self.bh, self.b, self.h0]
        # end-snippet-2
        # as many columns as context window size
        # as many lines as words in the sentence
        # start-snippet-3
        idxs = T.imatrix()
        x = self.emb[idxs].reshape((idxs.shape[0], de*cs))
        y_sentence = T.ivector('y_sentence')  # labels
        # end-snippet-3 start-snippet-4

        def recurrence(x_t, h_tm1):
            h_t = T.nnet.sigmoid(T.dot(x_t, self.wx)
                                 + T.dot(h_tm1, self.wh) + self.bh)
            s_t = T.nnet.softmax(T.dot(h_t, self.w) + self.b)
            return [h_t, s_t]

        [h, s], _ = theano.scan(fn=recurrence,
                                sequences=x,
                                outputs_info=[self.h0, None],
                                n_steps=x.shape[0])

        p_y_given_x_sentence = s[:, 0, :]
        y_pred = T.argmax(p_y_given_x_sentence, axis=1)
        # end-snippet-4

        # cost and gradients and learning rate
        # start-snippet-5
        lr = T.scalar('lr')

        sentence_nll = -T.mean(T.log(p_y_given_x_sentence)
                               [T.arange(x.shape[0]), y_sentence])
        sentence_gradients = T.grad(sentence_nll, self.params)
        sentence_updates = OrderedDict((p, p - lr*g)
                                       for p, g in
                                       zip(self.params, sentence_gradients))
        # end-snippet-5

        # theano functions to compile
        # start-snippet-6
        self.classify = theano.function(inputs=[idxs], outputs=y_pred)
        self.sentence_train = theano.function(inputs=[idxs, y_sentence, lr],
                                              outputs=sentence_nll,
                                              updates=sentence_updates)
        # end-snippet-6 start-snippet-7
        self.normalize = theano.function(inputs=[],
                                         updates={self.emb:
                                                  self.emb /
                                                  T.sqrt((self.emb**2)
                                                  .sum(axis=1))
                                                  .dimshuffle(0, 'x')})
        # end-snippet-7

    def train(self, x, y, window_size, learning_rate):

        cwords = contextwin(x, window_size)
        words = list(map(lambda x: numpy.asarray(x).astype('int32'), cwords))
        labels = y

        self.sentence_train(words, labels, learning_rate)
        self.normalize()

    def save(self, folder):
        for param in self.params:
            numpy.save(os.path.join(folder,
                       param.name + '.npy'), param.get_value())

    def load(self, folder):
        for param in self.params:
            param.set_value(numpy.load(os.path.join(folder,
                            param.name + '.npy')))


def returnModel():
	param = {'fold': 3,'data': 'atis','lr': 0.0970806646812754,'verbose': 1,'decay': True,'win': 7,'nhidden': 200,'seed': 345,'emb_dimension': 50,'nepochs': 60,'savemodel': True}
	folder_name = "rnnslu"
	folder = os.path.join(os.path.dirname(__file__), folder_name)
	vocsize =  572
	nclasses = 127
	rnn = RNNSLU(nh=param['nhidden'],
                 nc=nclasses,
                 ne=vocsize,
                 de=param['emb_dimension'],
                 cs=param['win'])
	rnn.load(folder)
	return rnn 

def returnDictionary():
	data = atisfold(3)
	data = data[3]
	return data

