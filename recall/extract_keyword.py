# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import jieba
import os
import jieba.posseg as pseg
def extract_center(words):
	vectors=[ word_vector[word] for word in words if word in word_vector]
	l=len(vectors)
	if l==0:
		return None
	d=len(vectors[0])
	results=[0 for i in range(0,d)]
	for vector in vectors:
		for i in range(0,d):
			results[i]=results[i]+vector[i]
	return results
def inner(v1,v2):
	return sum([s1*s2 for [s1,s2] in zip(v1,v2)])

def cal_word_score(words,center_vectors):
	results=[[word,inner(word_vector_normal[word],center_vectors)] for word in words if word in word_vector]
	max_score=max([s[1] for s in results])
	results=[[word,score/max_score] for [word,score] in results]
	return results
def split(sentence):
	results={}
	words_flag= pseg.cut(sentence)
	for w in words_flag:
		try:
			results[w.word]=w.flag
		except:
			pass
	return results
	

def extract_keyword(sentence):
	sentence=sentence.decode('utf-8')
	#$words=set([word for word in jieba.cut(sentence)])
	words_flag=split(sentence)
	words=words_flag.keys()
	center_vectors=extract_center(words)
	if center_vectors==None:
		return []
	word_score=cal_word_score(words,center_vectors)
	word_score=[ [word,round(score*idf.get(word,1.0),2)] for [word,score] in word_score]
	def add_flag_score(word):
		if words_flag[word].startswith("n") or words_flag[word].startswith("n"):
			return 5
		else :
			return 1
	word_score=[[ word,score*add_flag_score(word)] for [word,score] in word_score]
	return word_score
def read_vector(filepath):
	with open(filepath) as f:
		lines=f.readlines()
	lines=[line.strip().split("\t") for line in lines]
	word_vector=dict([[s[0].decode('utf-8'),eval(s[1])] for s in lines])
	return word_vector

	
path=os.path.split(os.path.realpath(__file__))[0]
with open(path+"/idf") as f:
	idf=json.load(f)
word_vector=read_vector(path+"/word2vec")
word_vector_normal=read_vector(path+"/word2vec_normal")
#result=extract_keyword("特别喜欢刘德华")
#print result
	









