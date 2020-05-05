#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import pickle
from keras.models import Model
from keras.layers import Input, Dense
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
class ShortTextModel(object):
	def __init__(self,length,word_num):
		self.input_length=length
		self.batch_size=512*10
		self.word_num=word_num

		self.input_dimension=128
		self.lstm_dim=64
		self.middle_num=2
		self.output_dimension=64

		#self.input_embedding=keras.layers.Embedding(input_dim=self.word_num,output_dim=self.input_dimension,weights=[weights])
		self.input_embedding=keras.layers.Embedding(input_dim=self.word_num,output_dim=self.input_dimension)
		self.bilstm=keras.layers.Bidirectional(keras.layers.LSTM(self.lstm_dim/2,return_sequences=True))
		self.middle_layer=[]
		for  i in range(0,self.middle_num):
			self.middle_layer.append(MultiHeadAttention(head_num=4,name="middle_layer_{}".format(i)))
		#self.outter_layer=keras.layers.Dense(self.output_dimension, activation="tanh", input_dim=self.input_length*self.lstm_dim, use_bias= True,name="ouput_layer")
		self.outter_layer=keras.layers.Dense(self.output_dimension,input_dim=self.input_length*self.lstm_dim, use_bias= True,name="ouput_layer")
	
	def inner_loss(self,y_true,y_pred,margin=1.0):
		#output=keras.layers.concatenate([video_vector,p_vector,n_vector],axis=1)
		video_vector,p_vector,n_vector=tf.unstack(y_pred,axis=1)
		right_cos = dot([video_vector,p_vector], -1, normalize=True)
		wrong_cos = dot([video_vector,n_vector], -1, normalize=True)
		loss = Lambda(lambda x: K.relu(margin+x[0]-x[1]))([wrong_cos,right_cos])
		#loss = Lambda(lambda x: x[0]-x[1])([wrong_cos,right_cos])
		return loss


	def construct_model(self,input_X):
		result=input_X
		result=self.input_embedding(result)
		result=self.bilstm(result)
		for  i in range(0,self.middle_num):
			result=self.middle_layer[i](result)
		result=keras.layers.core.Flatten()(result)
		result=self.outter_layer(result)
		result=keras.layers.core.Reshape((1,self.output_dimension))(result)
		return result
	def build_model(self):
		input1=Input(shape=(self.input_length,),name="input1")
		input2=Input(shape=(self.input_length,),name="input2")
		input3=Input(shape=(self.input_length,),name="input3")
		y1=self.construct_model(input1)
		y2=self.construct_model(input2)
		y3=self.construct_model(input3)
		output_c=keras.layers.concatenate([y1,y2,y3],axis=1,name="output_aaa")
		model=Model(inputs=[input1,input2,input3],outputs=output_c)
		predict_model=Model(inputs=input1,outputs=y1)		
		def wrapped_partial(func, *args, **kwargs):
			partial_func = partial(func, *args, **kwargs)
			update_wrapper(partial_func, func)
			return partial_func
		model.compile(loss=wrapped_partial(self.inner_loss), optimizer="Adam")
		self.model=model
		self.predict_model=predict_model
	
	def load_model(self,model_path):
		self.predict_model = load_model(model_path, custom_objects={'metric_loss':self.inner_loss,'MultiHeadAttention':keras_multi_head.MultiHeadAttention})

	def train(self,data,model_path):
		self.build_model() 
		y=[0 for _ in range(0,len(data[0]))]
		self.model.fit(data,y,epochs=4,batch_size=self.batch_size)
		self.predict_model.save(model_path)

	def predict_vector(self,data):
		return self.predict_model.predict([data])


def read_data(path,length):
	with open(path) as f :
		lines=f.readlines()#[0:200]
	random.shuffle(lines)
	lines=[eval(line.strip()) for line in lines]
	x1,x2,x3=zip(*lines)
	y=[[0] for _ in range(0,len(x1))]
	x1=np.array(x1)
	x2=np.array(x2)
	x3=np.array(x3)
	x1=keras.preprocessing.sequence.pad_sequences(x1, maxlen=length, value=0.)
	x2=keras.preprocessing.sequence.pad_sequences(x2, maxlen=length, value=0.)
	x3=keras.preprocessing.sequence.pad_sequences(x3, maxlen=length, value=0.)
	result=[x1,x2,x3]
	return result
if __name__ == '__main__':
	length=10
	data=read_data("train_data_index",length)
	with open("hanzi_index") as f :
		hanzi_index=json.load(f)
	word_num=len(hanzi_index)
	model=ShortTextModel(length,word_num)
	model.train(data,"model")
	#model.load_model("model")
	#x=data[0]
	#print model.predict_vector(x)



