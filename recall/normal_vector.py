import math
def normal(vector):
	ss=math.sqrt(sum([ s*s for s in vector]))
	return [ s/ss for s in vector]
with open("word2vec") as f:
	lines=f.readlines()
lines=[line.strip().split("\t") for line in lines]
results=[ word+"\t"+str(normal(eval(vector))) for word,vector in lines]
with open("word2vec_normal","w") as f:
	f.writelines("\n".join(results))
