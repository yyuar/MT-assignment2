# -*- encoding: utf-8 -*-
from collections import *
from math import *
import sys

nullSymbol = 'nullsymbol'
class IBM():
	def __init__(self, source, target, maxSourceSenLen, maxIter = 7):
		self.source = source
		self.target = target
		self.maxIter = maxIter
		self.maxSourceSenLen = maxSourceSenLen
		
		sourceVoc = {}
		for sen in source:
			for item in sen:
				sourceVoc[item] = 1
		self.src_id_to_token = sourceVoc.keys()
		self.src_token_to_id = {c:i for i,c in enumerate(self.src_id_to_token)}
		self.srcVocSize = len(self.src_id_to_token)
		
		targetVoc = {}
		for sen in target:
			for item in sen:
				targetVoc[item] = 1
		#self.tgt_id_to_token = targetVoc.keys() + [nullSymbol]
		self.tgt_id_to_token = targetVoc.keys()
		self.tgt_token_to_id = {c:i for i,c in enumerate(self.tgt_id_to_token)}
		self.tgtVocSize = len(self.tgt_id_to_token)

	def calculateLL(self,tgt,src):
		#episilon = 1.0/self.maxSourceSenLen
		#tgt = tgt + [nullSymbol]
		#ll = log(1.0/self.maxSourceSenLen) - len(src)*log(len(tgt))
		ll = - len(src)*log(len(tgt))
		for i in src:
			thisSum = 0
			for j in tgt:
				thisSum += self.theta[j][i]
			if thisSum!=0:
				ll+=log(thisSum)
			else:
				return float('-inf')
		return ll
	def train(self):
		# (1) Initialize ¦È[i,j] = 1 / f_vocabulary.
		thetaTmp = defaultdict(lambda : defaultdict(lambda : 1.0/self.srcVocSize))
		count = defaultdict(lambda : defaultdict(int))
		for (x, y) in zip(self.source, self.target):
			#source: De   target:En
			#y.append(nullSymbol)
			for srcToken in x:
				#sumPart = 0
				#for tgtToken in y:
				#	sumPart+=thetaTmp[tgtToken][srcToken]
				#for tgtToken in y:
				#	count[tgtToken][srcToken] += self.theta[tgtToken][srcToken]/sumPart
				sumPart = len(y)
				for tgtToken in y:
					count[tgtToken][srcToken]+=(1.0/sumPart)
		self.theta = defaultdict(lambda : defaultdict(int))
		oo = 0
		for tgt, srcList in count.items():
			sumPart = 0
			oo+=len(srcList)
			for k,v in srcList.items():
				sumPart+=v
			for k,v in srcList.items():
				self.theta[tgt][k] = v/sumPart
		print oo
		#till here get the theta after one iteration
		ll = 0
		wordNum = 0
		for (x, y) in zip(self.source, self.target):
			ll += self.calculateLL(y,x)
			wordNum += len(x)
		print ll/wordNum
		
		for iter in range(self.maxIter):
			count = defaultdict(lambda : defaultdict(int))
			# (2) [E] C[i,j] = ¦È[i,j] / ¦²_i ¦È[i,j] (Equation 110)
			#count[e[i], f[j]] = TODO
			for (x, y) in zip(self.source, self.target):
				#source: De   target:En
				#y.append(nullSymbol)
				for srcToken in x:
					sumPart = 0
					for tgtToken in y:
						sumPart+=self.theta[tgtToken][srcToken]
					for tgtToken in y:
						count[tgtToken][srcToken] += self.theta[tgtToken][srcToken]/sumPart
			# (2) [M] ¦È[i,j] =	C[i,j] / ¦²_j C[i,j] (Equation 107)
			#self.theta[ e[i], f[j] ] = TODO 
			for tgt, srcList in count.items():
				sumPart = 0
				for k,v in srcList.items():
					sumPart+=v
				for k,v in srcList.items():
					self.theta[tgt][k] = v/sumPart

			# (3) Calculate log data likelihood (Equation 106)
			ll = 0
			wordNum = 0
			for (x, y) in zip(self.source, self.target):
				ll += self.calculateLL(y,x)
				wordNum += len(x)
			print ll/wordNum

	#def align(self):
	#	for idx, (e, f) in enumerate(self.bitext):
	#		for i in range(len(e)):
	#			# ARGMAX_j ¦È[i,j] or other alignment in Section 11.6 (e.g., Intersection, Union, etc)
	#			max_j, max_prob = argmax_j(f, e[i])
	#		self.plot_alignment((max_j, max_prob), e, f)
	#	return alignments
	def align(self):
		f = open(sys.argv[3],'w')
		for (x, y) in zip(self.source, self.target):
			rst = []
			for i in range(len(y)):
				maxP = 0
				maxIndex = 0
				for j in range(len(x)):
					if self.theta[y[i]][x[j]]>maxP:
						maxP = self.theta[y[i]][x[j]]
						maxIndex = j
				rst.append(str(maxIndex)+'-'+str(i))
			f.write(' '.join(rst)+'\n')
		f.close()

def main():
	#sourceFile = "en-de/valid.en-de.low.en"
	#targetFile = "en-de/valid.en-de.low.de"
	sourceFile = sys.argv[2]
	targetFile = sys.argv[1]
	sourceDe = []
	targetEn = []
	corpusDe = set()
	corpusEn = set()
	maxIter = 20
	maxSourceSenLen = 0
	maxTargetSenLen = 0
	for line in open(sourceFile,'r'):
		fields = line.strip().split(' ')
		sourceDe.append(fields)
		maxSourceSenLen = max(maxSourceSenLen,len(fields))
	for line in open(targetFile,'r'):
		fields = line.strip().split(' ')
		#have already added the nullsymbol
		#fields.append(nullSymbol)
		targetEn.append(fields)
		maxTargetSenLen = max(maxTargetSenLen,len(fields))
	ibm = IBM(sourceDe, targetEn, maxSourceSenLen, maxIter)
	ibm.train()
	ibm.align()

if __name__ == '__main__': main()
