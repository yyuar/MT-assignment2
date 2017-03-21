from collections import *
from math import *
import sys

sourceFile = sys.argv[1]
targetFile = sys.argv[2]
alignFile = sys.argv[3]
phraseMaxLen = 3
sourceDe = []
targetEn = []
alignList = []
for line in open(sourceFile,'r'):
	fields = line.strip().split(' ')
	sourceDe.append(fields)
for line in open(targetFile,'r'):
	fields = line.strip().split(' ')
	targetEn.append(fields)
for line in open(alignFile,'r'):
	fields = line.strip().split(' ')
	for i in range(len(fields)):
		tmp = fields[i].split('-')
		fields[i] = (int(tmp[0]),int(tmp[1]))
	alignList.append(fields)
BP = defaultdict(int)
for i in range(len(sourceDe)):
	#source: sourceDe[i]
	#target: targetEn[i]
	#align: alignList[i]
	srcLen = len(sourceDe[i])
	tgtLen = len(targetEn[i])
	eAlign = [j for j,_ in alignList[i]]  #english: target
	fAlign = [j for _,j in alignList[i]]  #germen: src
	bp = set()
	for fStart in range(srcLen):
		for fEnd in range(fStart,min(fStart+phraseMaxLen,srcLen)):
			tp = []
			for (e,f) in alignList[i]:
				if fStart<=f<=fEnd:
					tp.append(e)
			if len(tp)==0:
				continue
			eStart = min(tp)
			eEnd = max(tp)
			
			flag = 0
			for (e,f) in alignList[i]:
				if eStart<=e<=eEnd:
					if f>fEnd or f<fStart:
						flag = 1
						break
			if flag==1:
				continue
			
			es = eStart
			while True:
				ee = eEnd
				while True:
					if (ee-es)>=phraseMaxLen:
						break
					srcPhrase = " ".join(sourceDe[i][index] for index in range(fStart,fEnd+1))
					tgtPhrase = " ".join(targetEn[i][index] for index in range(es,ee+1))
					bp.add(((eStart,eEnd+1),(fStart,fEnd+1),srcPhrase,tgtPhrase)) 
					ee+=1
					if ee in eAlign or ee==tgtLen:
						break
				es-=1
				if es in eAlign or es<0:
					break
	for item in bp:
		BP[(item[2],item[3])]+=1
print len(BP)
countE = defaultdict(int)
for k,v in BP.items():
	countE[k[1]]+=v
	
f = open(sys.argv[4],'w')
for k,v in BP.items():
	p = 1.0*v/countE[k[1]]
	if p==1:
		ll = 0
	else:
		ll = -log(p)
	f.write(k[0]+'\t'+k[1]+'\t'+str(ll)+'\n')
f.close()
			
			
				
			
