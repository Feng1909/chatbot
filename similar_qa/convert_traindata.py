# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import random
def get_hanzi_index(lines):
	hanzi_index={"unknow":0}
	hanzi_list=set([ s for data in lines for s in data['a']+data['q']])
	for s in hanzi_list:
		hanzi_index[s]=len(hanzi_index)
	return hanzi_index
def get_index(sentence):
	return [ hanzi_index[s] for s in sentence]

with open("../train_data") as f:
	lines=f.readlines()#[0:100]
qas=[json.loads(line.strip()) for line in lines]
hanzi_index=get_hanzi_index(qas)
all_answers_index=[ get_index(s['a']) for s in qas]
with open("hanzi_index","w") as f:
	json.dump(hanzi_index,f,ensure_ascii=False)
results=[]
count=0
for data in qas:
	if count%1000==0:
		print count,len(qas)
	count+=1
	q=data['q']
	a=data['a']
	index1=get_index(q)
	index2=get_index(a)
	index3_list=random.sample(all_answers_index,10)
	for index3 in index3_list:
		results.append(str([index1,index2,1]))
		results.append(str([index1,index3,0]))

with open("train_data_index","w") as f:
	f.writelines("\n".join(results))







