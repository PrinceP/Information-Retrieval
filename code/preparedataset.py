import os
import six.moves.cPickle as pickle
import gzip
import numpy as np

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
    

    print np.shape(train_set)

    # for i in train_set:
    # 	print i

    for i in dicts:
    	print i	

    


    for x in range(0,1):
    	print " "	
    	for i in train_set[x][0]:
    		
    		for j in dicts:
    		
    			try:	
    				print dicts[j].keys()[dicts[j].values().index(i)] , 
    			except ValueError:
 					pass	 
    

    for x in range(0,1):
        print " "   
        for i in valid_set[x][0]:
            try:    
                print dicts['tables2idx'].keys()[dicts['tables2idx'].values().index(i)] , 
            except ValueError:
                pass     
            	



    	



    	
    



    

atisfold(0)    



