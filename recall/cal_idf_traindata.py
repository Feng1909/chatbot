# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import jieba
import math
def convert(lines):
	results=[]
	for line in lines:
		if line.startswith("M") or line.startswith("E"):
			results.append(line)
		else:
			results[-1]=results[-1]+line
	return results
def cal_idf(all_words):
	word_count={}
	num=1.0*len(all_words)
	for words in all_words:
		words=set(words)
		for word in words:
			word_count[word]=word_count.get(word,0)+1
	word_count=word_count.items()
	word_count
	idf=dict([[word,math.log(num/count)] for [word,count] in word_count])
	return idf

with open("/data/chat/xiaohuangji50w_nofenci.conv") as f:
	lines=f.readlines()#[0:100]
lines=[line.strip().decode("utf-8") for line in lines]
lines=convert(lines)
all_words=[]
for i in range(0,len(lines),3):
	try:
		s1=lines[i+1].split(" ")[1]
		words=jieba.cut(s1)
		words=[word for word in words]
		all_words.append(words)
	except:
		pass
idf=cal_idf(all_words)
with open("idf","w") as f:
	json.dump(idf,f,ensure_ascii=False)
word2vec_data=[ " ".join(words) for words in all_words]
with open("train_data_word2vec","w") as f:
	f.writelines("\n".join(word2vec_data))



















