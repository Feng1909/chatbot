# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
with open("train_data") as f:
	lines=f.readlines()#[0:100]
lines=[json.loads(line.strip()) for line in lines]
index2item={}
for i,data in enumerate(lines):
	index2item[i]=data
with open("index2item","w") as f:
	json.dump(index2item,f,ensure_ascii=False)
		









