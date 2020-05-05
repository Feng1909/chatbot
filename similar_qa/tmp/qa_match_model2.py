#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import pickle
from keras.models import Model
from keras.layers import Input, Dense,Dot,MaxPooling1D,Flatten,Reshape
from keras import backend as K
from keras.layers.embeddings import Embedding
from keras.layers.core import Lambda
import keras
import keras_multi_head
from keras_multi_head import MultiHeadAttention
from functools import partial, update_wrapper
import tensorflow as tf
from keras.models import load_model
import numpy as np
import tensorflow as tf
import keras 
from keras.callbacks import ModelCheckpoint
import random
from keras.layers.merge import dot
if __name__ == '__main__':
	
	with open("hanzi_index") as f :
		hanzi_index=json.load(f)
	word_num=len(hanzi_index)
	input_dimension=128
	lstm_dim=128
	input_length=4
	


	with open("train_data_index") as f:
		lines=f.readlines()[0:1000]
	random.shuffle(lines)
	questions,answers,ls=zip(*[eval(line.strip()) for line in lines])
	questions=np.array(questions)
	answers=np.array(answers)
	ls=np.array(ls)
	questions=keras.preprocessing.sequence.pad_sequences(questions,maxlen=input_length, value=0.)
	answers=keras.preprocessing.sequence.pad_sequences(answers,maxlen=input_length, value=0.)

	input1=Input(shape=(input_length,),name="input1")
	input2=Input(shape=(input_length,),name="input2")
	embedding_layer=keras.layers.Embedding(input_dim=word_num,output_dim=input_dimension)
	embed1=embedding_layer(input1)
	embed2=embedding_layer(input2)
	bilstm=keras.layers.Bidirectional(keras.layers.LSTM(lstm_dim/2,return_sequences=True))
	lstm1=bilstm(embed1)	
	lstm2=bilstm(embed2)
	'''	
	q_attention=MultiHeadAttention(head_num=4)
	a_attention=MultiHeadAttention(head_num=4)
	
	q_out=q_attention([lstm1,lstm2,lstm2])
	a_out=a_attention([lstm2,lstm1,lstm1])
	
	q_out= Lambda(lambda x: K.sum(x, axis=1))(q_out)
	a_out= Lambda(lambda x: K.sum(x, axis=1))(a_out)
	'''
	q_out_1=Dot(axes=2,normalize=True)([lstm1,lstm2])
	a_out_1=Dot(axes=2,normalize=True)([lstm2,lstm1])
	
	q_out = MaxPooling1D(pool_size=input_length)(q_out_1)
	a_out = MaxPooling1D(pool_size=input_length)(a_out_1)
	out=keras.layers.concatenate([q_out,a_out],axis=2)
	out=Flatten()(out)
	out=Dense(1024,activation='relu')(out)
	out=Dense(1,activation='sigmoid')(out)
	model=Model(inputs=[input1,input2],outputs=out)
	model2=Model(inputs=[input1,input2],outputs=q_out_1)
	model3=Model(inputs=[input1,input2],outputs=a_out_1)
	model.compile(loss="binary_crossentropy", optimizer="Adam")
	
	model.fit([questions,answers],ls,epochs=1,batch_size=128)

	print model2.predict([questions[0:1],answers[0:1]])
	print
	print model3.predict([questions[0:1],answers[0:1]])




