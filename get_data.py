# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import jieba
def convert(lines):
	results=[]
	for line in lines:
		if line.startswith("M") or line.startswith("E"):
			results.append(line)
		else:
			results[-1]=results[-1]+line
	return results
with open("xiaohuangji50w_nofenci.conv") as f:
	lines=f.readlines()#[0:100]
lines=[line.strip().decode("utf-8") for line in lines]
lines=convert(lines)
results=[]
for i in range(0,len(lines),3):
	try:
		s1=lines[i+1].split(" ")[1]
		s2=lines[i+2].split(" ")[1]
		results.append({"q":s1,"a":s2})
	except:
		pass
results=sorted(results,key=lambda s:s['q'])
results=[json.dumps(s,ensure_ascii=False) for s in results]
with open("train_data","w") as f:
	f.writelines("\n".join(results))






