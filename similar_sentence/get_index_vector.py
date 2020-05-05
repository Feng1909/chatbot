#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import predict
import math
def normal(vector):
	ss=math.sqrt(sum([ s*s for s in vector]))
	vector=[round(s/ss,3) for s in vector]
	return vector

with open("../index2item") as f:
	index2item=json.load(f)
results={}
count=0
for index,data in index2item.items():#[0:100]:
	if count%1000==0:
		print count,len(index2item)
	count+=1
	q=data['q']
	vector=predict.cal_vector(q)
	vector=normal(vector)
	results[index]=vector
with open("index_vector","w") as f:
	json.dump(results,f)
