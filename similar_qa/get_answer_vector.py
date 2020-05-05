# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import random
def get_index(sentence):
	return [ hanzi_index[s] for s in sentence if s in hanzi_index]
with open("../index2item") as f:
	index2item=json.load(f)
with open("hanzi_index") as f:
	hanzi_index=json.load(f)

results={}
count=0
for index,data in index2item.items():
	count+=1
	print count,len(index2item)
	a=data['a']
	results[index]=get_index(a)

with open("index_answer","w") as f:
	json.dump(results,f)







