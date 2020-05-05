#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import pickle
import keras
from keras.models import load_model
import numpy as np
from sentence_model import ShortTextModel
def sentence2index(sentence):
	sentence=sentence.decode("utf-8")
	index=np.array([[hanzi_index.get(hanzi,0) for hanzi in sentence]])
	result=keras.preprocessing.sequence.pad_sequences(index, maxlen=length, value=0.)
	return result
def cal_vector(sentence):
	index=sentence2index(sentence)
	return model.predict_vector(index)[0].tolist()[0]
length=10
with open("hanzi_index") as f :
	hanzi_index=json.load(f)
word_num=len(hanzi_index)
model=ShortTextModel(length,word_num)
model.load_model("model")
if __name__ == '__main__':
	sentence="你在干嘛"
	print cal_vector(sentence)
	sentence="吃饭了吗吃饭了吗吃饭了吗"
	print cal_vector(sentence)
	sentence="我操你妈"
	print cal_vector(sentence)



