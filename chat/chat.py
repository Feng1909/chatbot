# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
sys.path.append("../recall")
sys.path.append("../similar_sentence")
sys.path.append("../similar_qa")
import recall
import rank_step_one
import rank_step_two
import numpy as np
def print_result(results):
	results2=[ json.dumps(index2item[i],ensure_ascii=False)+"\t"+str(score)  for [i,score] in results]
	print "\n".join(results2)+"\n\n\n"  	
def random_index(results):
	index_list=[s[0] for s in results]
	score_list=[s[1] for s in results]
	ss=sum(score_list)
	score_list=np.array([s/ss for s in score_list])
	result = np.random.choice(index_list, p = score_list.ravel())
	return result

if __name__ == '__main__':
	with open("../index2item") as f:
		index2item=json.load(f)
	while True:
		#try:
		sentence=raw_input("问句:\t")
		#从40w里面找100个
		results1,topword=recall.recall(sentence,topK=100)
		if len(results1)==0:
			print "不知道"
			continue
		#从100个里面找50个
		results2=rank_step_one.rank(sentence,[s[0] for s in results1],topK=50)
		if len(results2)==0:
			print "不知道"
			continue
		#从50个中找10个
		results3=rank_step_two.rank(sentence,[s[0] for s in results2],topK=10)
		if len(results3)==0:
			print "不知道"
			continue
		index=random_index(results3)
		print "机器人回答:\t"+index2item[index]['a']
		print
			#print_result(results3[0:10])
		#except:
		#	pass


