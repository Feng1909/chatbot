# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import extract_keyword
word2index={}
with open("../index2item") as f:
	index2item=json.load(f)
count=0
for i,data in index2item.items():
	if count%1000==0:
		print count,len(index2item)
	count+=1
	q=data['q']
	keywords=extract_keyword.extract_keyword(q)
	for word,score in keywords:
		if word not in word2index:
			word2index[word]=[]
		word2index[word].append([i,score])
with open("word2index","w") as f:
	json.dump(word2index,f,ensure_ascii=False)
		









