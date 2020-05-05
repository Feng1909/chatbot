# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import jieba
import random
def add(prefix,key,words_sent,similar_info):
	s="{}:{}".format(prefix,key)
	if s not in similar_info:
		similar_info[s]=set([])
	similar_info[s].add(words_sent)

with open("../train_data") as f:
	lines=f.readlines()#[0:10]
similar_info={}
count=0
for line in lines:#[0:30000]:
	if count%1000==0:
		print count,len(lines)
	count+=1
	data=json.loads(line.strip())
	q=data['q'].replace("\t","")
	a=data['a'].replace("\t","")
	q_words_sent=str((set([s for s in jieba.cut(q)]),q))
	a_words_sent=str((set([s for s in jieba.cut(a)]),a))
	add("a",a,q_words_sent,similar_info)
	#add("q",q,a_words_sent,similar_info)
	
results=[]
count=0
for info in similar_info.values():
	info=list(info)
	print count,len(similar_info),len(info)
	count+=1
	l=len(info)
	if len(info)>100:
		continue
	for i in range(0,l):
		for j in range(i+1,l):
			w1,s1=eval(info[i])
			w2,s2=eval(info[j])
			c=len([ w for w in w1 if w in w2])
			if c>=2:
				results.append("{}\t{}".format(s1,s2))
with open("train_data","w") as f:
	f.writelines("\n".join(results))
	








