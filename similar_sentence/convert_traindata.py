# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import random
def get_hanzi_index(lines):
	hanzi_index={"unknow":0}
	hanzi_list=set([ s for [s1,s2] in lines for s in s1+s2])
	for s in hanzi_list:
		hanzi_index[s]=len(hanzi_index)
	return hanzi_index
def get_all_sentence(lines):
	results=set([])
	for s1,s2 in lines:
		results.add(s1)
		results.add(s2)
	return results
def get_index(sentence):
	return [ hanzi_index[s] for s in sentence]

with open("train_data") as f:
	lines=f.readlines()#[0:100]
lines=[line.strip().decode('utf-8').split("\t") for line in lines]
lines=[line for line in lines if len(line)==2]
hanzi_index=get_hanzi_index(lines)
with open("hanzi_index","w") as f:
	json.dump(hanzi_index,f,ensure_ascii=False)
all_sentence=get_all_sentence(lines)
all_sentence_index=[get_index(s) for s in all_sentence]
results=[]
count=0
for s1,s2 in lines:
	if count%1000==0:
		print count,len(lines)
	count+=1
	index1=get_index(s1)
	index2=get_index(s1)
	index3_list=random.sample(all_sentence_index,10)
	for index3 in index3_list:
		results.append(str([index1,index2,index3]))
with open("train_data_index","w") as f:
	f.writelines("\n".join(results))







