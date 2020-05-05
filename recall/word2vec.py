# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import fasttext
def normal(vector):
	ss=math.sqrt(sum([ s*s for s in vector]))
	return [ s/ss for s in vector]

results1=[]
results2=[]
model = fasttext.train_unsupervised('train_data_word2vec', model='cbow',thread=2,epoch=100)
for word in model.words:
	vector=model[word].tolist()
	results1.append("{}\t{}".format(word,str(vector)))
	results2.append("{}\t{}".format(word,str(normal(vector))))

with open("word2vec","w") as f:
	f.writelines("\n".join(results1))
with open("word2vec_normal","w") as f:
	f.writelines("\n".join(results2))
