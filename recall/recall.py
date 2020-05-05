# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import extract_keyword
import os	
path=os.path.split(os.path.realpath(__file__))[0]

with open(path+"/word2index") as f:
	word2index=json.load(f)

def recall(sentence,topK=10):
	keywords=extract_keyword.extract_keyword(sentence)
	if len(keywords)==0:
		return [],None
	topword=sorted(keywords,key=lambda s:s[1],reverse=True)[0][0]
	top_index=set([s[0] for s in word2index.get(topword,[])])
	rec_score={}
	for word,score in keywords:
		rec_word_score=word2index.get(word,[])
		for index,s in rec_word_score:
			if index not in top_index:
				continue
			rec_score[index]=rec_score.get(index,0.0)+s*score
	rec_score=rec_score.items()
	rec_score=sorted(rec_score,key=lambda s:s[1],reverse=True)[0:topK]
	#rec_score=[  [index2item[index],score] for [index,score] in rec_score]
	return rec_score,keywords

  
if __name__ == '__main__':
	with open(path+"/../index2item") as f:
		index2item=json.load(f)
	while True:
		#print "输入问句\n"
		sentence=raw_input("请输入问句:\t")
		results,_=recall(sentence,topK=50)
		for docid,score in results:
			data=index2item[docid]
			print json.dumps(data,ensure_ascii=False),score
		print 

















