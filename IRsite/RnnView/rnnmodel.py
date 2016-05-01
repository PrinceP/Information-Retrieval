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
	dicts = {'all': 32, 'coach': 110, 'month': 318, 'four': 202, 'code': 111, 'go': 213, 'Chennai': 377, 'Jammu': 81, 'departing': 139, 'thursday': 496, 'to': 502, 'dinnertime': 151, 'under': 529, 'sorry': 450, 'include': 235, 'midwest': 311, 'worth': 564, 'southwest': 451, 'me': 301, 'returning': 408, 'far': 181, 'airfare': 24, 'ticket': 498, 'difference': 148, 'arrange': 54, 'tickets': 499, 'Kanpur': 378, 'louis': 286, 'cheapest': 99, 'list': 276, 'wednesday': 546, 'leave': 268, 'heading': 222, 'ten': 474, 'direct': 152, 'turboprop': 520, 'Bagdogra': 312, 'rate': 395, 'cost': 121, 'quebec': 392, 'layover': 266, 'choices': 101, 'port': 282, 'Chandigarh': 77, 'what': 554, 'stands': 454, 'reaching': 397, 'transcontinental': 510, 'Bhopal': 236, 'goes': 214, 'new': 332, 'transportation': 512, 'bareily': 104, 'fifteenth': 187, 'hours': 228, 'let': 272, 'twentieth': 523, 'along': 33, 'thrift': 494, 'passengers': 371, 'great': 216, 'thirty': 490, 'canadian': 91, 'leaves': 269, 'alaska': 31, 'leaving': 270, 'amount': 38, 'weekday': 549, 'makes': 294, 'midway': 310, 'via': 541, 'depart': 138, 'county': 124, 'names': 327, 'total': 507, 'seventeenth': 434, 'use': 533, 'twa': 521, 'from': 208, 'Dibrugarh': 255, 'would': 565, 'abbreviations': 15, 'destination': 144, 'flights': 194, 'next': 334, 'live': 278, 'going': 215, 'Allahabad': 319, 'h': 219, 'limousine': 275, 'tell': 473, 'today': 503, 'more': 320, 'Hyderabad': 107, 'about': 16, 'm80': 292, 'downtown': 159, 'train': 509, 'Imphal': 351, 'fly': 196, 'noontime': 342, 'f': 179, 'this': 491, 'car': 93, 'Dehradun': 328, 'anywhere': 44, 'can': 89, 'following': 199, 'making': 295, 'arrive': 58, 'my': 325, 'could': 123, 'give': 212, 'december': 134, 'numbers': 348, 'want': 542, 'DIGITDIGITDIGITDIGITDIGITDIGIT': 12, 'airplane': 27, 'times': 501, 'information': 237, 'provide': 388, 'travel': 513, 'six': 440, 'carries': 95, 'how': 230, 'sunday': 463, 'fourth': 204, 'types': 527, 'nonstop': 339, 'economy': 168, 'fare': 182, 'petersburg': 375, 'may': 299, 'earlier': 164, 'plane': 381, 'ff': 185, 'coming': 115, 'Indore': 333, 'eighth': 171, 'fn': 198, 'las': 260, 'a': 13, 'boeing': 74, 'third': 487, 'departure': 141, 'q': 390, 'so': 446, 'Daman': 553, 'sa': 412, 'restriction': 405, 'serving': 433, 'help': 224, 'september': 426, 'over': 370, 'midnight': 309, 'soon': 449, 'logan': 281, 'through': 495, 'still': 457, 'before': 72, 'thirtieth': 489, 'but': 83, 'thank': 479, 'fit': 191, 'located': 280, 'actually': 18, 'late': 263, 'offers': 355, 'listing': 277, 'texas': 477, 'DIGITDIGITDIGITDIGIT': 11, 'then': 483, 'evening': 174, 'return': 407, 'yn': 568, 'lunch': 290, 'wednesdays': 547, 'they': 486, 'arriving': 60, 'now': 346, 'rental': 399, 'day': 130, 'landings': 259, 'february': 184, 'airports': 30, 'name': 326, 'sundays': 464, 'january': 244, 'Agartala': 102, 'each': 163, 'meal': 302, 'dulles': 160, 'thirteenth': 488, 'ea': 162, 'used': 534, 'connect': 116, 'okay': 357, 'morning': 321, 'tenth': 476, 'saturday': 416, 'out': 369, 'canada': 90, 'looking': 284, 'Cochin': 128, 'arizona': 52, 'cars': 96, 'friday': 206, 'seventh': 435, 'california': 88, 'bwi': 85, 'ord': 364, 'earliest': 165, 'shortest': 437, 'dc10': 133, 'rentals': 400, 'airport': 29, 'atl': 63, 'florida': 195, 'days': 131, 'round': 410, 'american': 37, 'st.': 452, 'first': 190, 'flying': 197, 'number': 347, 'one': 359, 'eleventh': 173, 'approximately': 48, 'another': 42, 'type': 526, 'tomorrow': 504, '<UNK>': 7, 'service': 430, 'twenty': 524, 'dfw': 146, 'weekdays': 550, 'least': 267, 'their': 482, 'rates': 396, 'too': 505, 'Aurangabad': 423, 'sixteenth': 442, 'that': 480, 'serve': 427, 'DIGITDIGITDIGIT': 10, 'july': 248, 'than': 478, 'distance': 154, 'kind': 252, 'b': 67, 'Hubli': 367, 'second': 424, 'i': 232, 'classes': 106, 'traveling': 514, 'and': 40, 'rae': 251, 'san': 415, 'Jaipur': 114, 'stopovers': 460, 'takeoff': 468, 'Goa': 466, 'say': 418, 'mornings': 322, 'rent': 398, 'have': 221, 'need': 331, 'breakfast': 80, 'any': 43, 'also': 34, 'costs': 122, 'take': 467, 'which': 557, 'Coimbatore': 306, 'Bhubaneswar': 379, 'sure': 465, 'price': 386, 'who': 558, 'serviced': 431, 'most': 323, 'eight': 169, 'plan': 380, 'services': 432, 'america': 36, 'class': 105, 'later': 264, 'm': 291, 'nineteenth': 336, 'salt': 413, 'show': 439, 'cheap': 98, 'Gauhati': 64, 'tuesdays': 519, 'find': 189, 'fifth': 188, 'ground': 217, 'snack': 445, 'explain': 177, 'minnesota': 314, 'should': 438, 'only': 360, 'stand': 453, 'interested': 238, 'carolina': 94, 'do': 156, 'dl': 155, 'get': 211, 'michigan': 308, 'express': 178, 'stop': 458, 'dc': 132, 'Gwalior': 307, 'international': 239, 'during': 161, 'Agra': 539, 'qw': 393, 'stapleton': 455, 'qx': 394, 'requesting': 402, 'ohio': 356, 'where': 556, 'qo': 391, 'arrival': 56, 'eighteenth': 170, 'maximum': 298, 'connections': 119, 'see': 425, 'are': 50, 'close': 108, 'Dimapur': 229, 'paul': 372, 'capacity': 92, 'Jodhpur': 376, 'please': 383, 'smallest': 444, 'various': 538, 'between': 73, 'Bangalore': 137, 'f28': 180, 'available': 66, 'we': 545, 'august': 65, 'aircraft': 23, 'here': 225, 'cities': 103, 'jfk': 246, 'both': 78, 'c': 87, 'last': 261, 'many': 296, 'taking': 470, 'display': 153, 'april': 49, 's': 411, 'flies': 192, 'co': 109, 'very': 540, 'tuesday': 518, 'nonstops': 340, 'tennessee': 475, 'stopover': 459, 'cp': 125, 'november': 345, 'expensive': 176, 'Diu': 69, 'west': 552, 'airlines': 26, 'nationair': 329, 'much': 324, 'define': 135, 'mco': 300, 'flight': 193, 'eastern': 167, 'airplanes': 28, 'Bhuj': 506, 'lives': 279, 'prices': 387, 'general': 209, 'those': 492, 'highest': 227, 'georgia': 210, 'look': 283, 'these': 485, 'originate': 365, 'missouri': 315, 'air': 22, 'will': 559, 'near': 330, 'itinerary': 243, 'stopping': 461, 'mitchell': 316, 'fourteenth': 203, 'thursdays': 497, 'is': 241, 'it': 242, 'arrangements': 55, 'in': 234, 'if': 233, 'different': 149, 'make': 293, 'connection': 118, 'same': 414, 'northwest': 344, 'ewr': 175, 'twelfth': 522, 'week': 548, 'arrives': 59, 'again': 21, 'takeoffs': 469, 'uses': 535, 'francisco': 205, 'database': 129, 'pennsylvania': 373, 'well': 551, 'options': 362, 'without': 563, 'jersey': 245, 'y': 566, 'the': 481, 'latest': 265, 'taxi': 472, 'Jamnagar': 543, 'just': 250, 'less': 271, 'ninth': 337, 'abbreviation': 14, 'seats': 422, 'love': 287, 'yes': 567, 'jose': 247, 'sixteen': 441, 'lake': 256, 'book': 75, 'ap80': 47, 'fares': 183, 'has': 220, 'march': 297, 'around': 53, 'delhi': 569, 'utah': 537, 'possible': 385, 'early': 166, 'know': 254, 'schedules': 420, 'using': 536, 'd': 126, 'like': 273, 'arrivals': 57, 'either': 172, 'night': 335, 'served': 428, 'tower': 508, 'limo': 274, 'seating': 421, 'right': 409, 'saturdays': 417, 'people': 374, 'lastest': 262, 'back': 68, "'t": 5, 'serves': 429, 'kinds': 253, 'transport': 511, 'provided': 389, 'monday': 317, 'for': 200, 'noon': 341, 'stops': 462, 'does': 157, 'connecting': 117, 'three': 493, 'booking': 76, 'be': 70, 'business': 82, 'schedule': 419, 'sixth': 443, 'departures': 142, 'ap57': 46, 'by': 86, 'after': 19, 'on': 358, 'DIGIT': 8, 'sfo': 436, 'DIGITDIGIT': 9, 'of': 353, 'dollars': 158, 'angeles': 41, 'dinner': 150, 'afternoon': 20, 'mean': 304, 'or': 363, 'colorado': 113, 'united': 530, 'into': 240, 'within': 562, 'bound': 79, 'two': 525, 'Amritsar': 471, 'your': 571, 'guardia': 218, 'area': 51, 'there': 484, 'continental': 120, 'los': 285, 'Jorhat': 313, 'airline': 25, '72s': 6, 'way': 544, 'lowest': 288, 'buy': 84, 'north': 343, 'offer': 354, 'some': 447, 'hp': 231, 'restrictions': 406, 'landing': 258, 'Ahmedabad': 100, 'hi': 226, 'delta': 136, 'Calcutta': 97, 'trying': 517, 'with': 561, 'fort': 201, 'october': 352, 'wish': 560, 'up': 531, 'us': 532, "'re": 3, 'planes': 382, 'pm': 384, 'ua': 528, 'trips': 516, 'blair': 71, 'originating': 366, 'ac': 17, 'Bhavnagar': 145, 'reservations': 404, 'describe': 143, 'am': 35, 'an': 39, 'ap': 45, 'as': 61, 'sometime': 448, 'at': 62, 'trip': 515, 'diego': 147, 'codes': 112, "'ll": 1, 'no': 338, 'when': 555, 'field': 186, 'other': 368, 'you': 570, 'nw': 349, 'repeat': 401, "'s": 4, "o'clock": 350, 'june': 249, 'lufthansa': 289, 'meaning': 305, "'d": 0, 'reservation': 403, "'m": 2, 'friends': 207, 'meals': 303, 'land': 257, 'daily': 127, 'Jamshedpur': 361, 'departs': 140, 'time': 500, 'starting': 456, 'hello': 223}
	dicts = dict((k.lower() if isinstance(k, basestring) else k, v.lower() if isinstance(v, basestring) else v) for k,v in dicts.iteritems())
	return dicts

def returnDictionaryOriginal():
	dicts = atisfold(3)
	dicts = dicts[3]
	return dicts

