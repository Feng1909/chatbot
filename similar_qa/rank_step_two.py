#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
from keras.models import load_model
import keras
import numpy as np
import os
path=os.path.split(os.path.realpath(__file__))[0]
input_length=10
with open(path+"/hanzi_index") as f :
	hanzi_index=json.load(f)
model=load_model(path+"/model")
with open(path+"/index_answer") as f:
	index_answer=json.load(f)
def rank(sentence,index_candidate,topK=10):
	sentence=[ hanzi_index[s] for s in sentence.decode('utf-8') if s in hanzi_index]
	l1=[]
	l2=[]
	for index in index_candidate:
		vector=index_answer.get(index,[0])
		l1.append(sentence)
		l2.append(vector)
	l1=np.array(l1)
	l2=np.array(l2)
	l1=keras.preprocessing.sequence.pad_sequences(l1,maxlen=input_length, value=0.)
	l2=keras.preprocessing.sequence.pad_sequences(l2,maxlen=input_length, value=0.)
	score=model.predict([l1,l2]).tolist()
	score=[s[0] for s in score]
	result=zip(index_candidate,score)
	result=[ [s[0],s[1]] for s in result]
	result=sorted(result,key=lambda s:s[1],reverse=True)[0:topK]
	return result
#print rank("你好吗",["23","3123","34"],topK=10)




	

