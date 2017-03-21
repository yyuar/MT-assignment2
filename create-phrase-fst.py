from collections import *
import sys
stateIndex = defaultdict(lambda: len(stateIndex))
initState = ()
stateIndex[initState] = 0
phraseFile = sys.argv[1]
fstFile = sys.argv[2]
f = open(fstFile,'w')
for line in open(phraseFile,'r'):
	fields = line.strip().split('\t')
	source = fields[0]
	target = fields[1]
	p = fields[2]
	lastState = initState
	for token in source.split(' '):
		curState = lastState + (('sr',token),)
		if not stateIndex.has_key(curState):
			f.write(str(stateIndex[lastState]) + ' ' + str(stateIndex[curState]) + ' ' + token + ' <eps>\n')
		lastState = curState
	for token in target.split(' '):
		curState = lastState + (('tg',token),)
		if not stateIndex.has_key(curState):
			f.write(str(stateIndex[lastState]) + ' ' + str(stateIndex[curState]) + ' <eps> ' + token + '\n')
		lastState = curState
	f.write(str(stateIndex[lastState]) + ' ' + str(stateIndex[initState]) + ' <eps> <eps> ' + p + '\n')
	
f.write('0 0 </s> </s>'+'\n'+'0 0 <unk> <unk>'+'\n'+'0')