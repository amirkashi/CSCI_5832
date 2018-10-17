#-------------------------------------
# NLP homework 5
#By: Amir Kashipazha
#Following sources was used for this homework:
#	https://www.youtube.com/watch?v=hq80J8kBg-Y
#	https://www.youtube.com/watch?v=MiEKnFyErbQ&list=PL6397E4B26D00A269&index=65
#	http://www.cs.pomona.edu/~kim/CSC181S08/lectures/Lec11/Lec11.pdf
#-------------------------------------

import numpy as np

# grammar was taken form course assingnment website
grammar = {
    ('S','NP','VP'):0.9,
    ('S','VP'):0.1, # unary
    ('VP','V','NP'):0.5,
    ('VP','V'):0.1,     # unary
    ('VP','V','@VP_V'):0.3,
    ('VP','V','PP'):0.1,
    ('@VP_V','NP','PP'):1.0,
    ('NP','NP','NP'):0.1,
    ('NP','NP','PP'):0.2,
    ('NP','N'):0.7,    #unary
    ('PP','P','NP'):1.0,
    ('N','people'):0.5,
    ('N','fish'):0.2,
    ('N','tanks'):0.2,
    ('N','rods'):0.1,
    ('V','people'):0.1,
    ('V','fish'):0.6,
    ('V','tanks'):0.3,
    ('P','with'):1.0
}

# making set of nonterminals to remove repeated nonterminals
nonTermsSet = set()
for w in grammar:
	nonTermsSet.add(w[0])

# making list of nonterminals to be able to iterate to them
nonTerms = list(nonTermsSet)
#print nonTerms

# assign a unique value to each nonterminal to be able to reference or map each terminal using that reference number 
nontermLabel = {}
for i in range(0, len(nonTerms)):
	nontermLabel[nonTerms[i]] = i
#print nontermLabel

# CKY function implementation
def CKY(words):
	# making matirx
	score = np.zeros( (len(words)+1, len(words)+1, len(nonTerms)) ) 
	
	# handling first row of the matirx (this is for words)
	for i in range(0, len(words)):
		for A in nonTerms:
			if (A, words[i]) in grammar:
				score[i][i+1][nontermLabel[A]] = grammar[(A,words[i])]
		# handling unairy 
		added = True
		while added:
			added = False
			for A in nonTerms:
				for B in nonTerms:
					if score[i][i+1][nontermLabel[B]] > 0 and (A,B) in grammar.keys():
						prob = grammar[(A,B)] * score[i][i+1][nontermLabel[B]]
						if prob > score[i][i+1][nontermLabel[A]]:
							score[i][i+1][nontermLabel[A]] = prob
							added = True 
		

	# fill the matrix 
	for span in range(2, len(words)+1):
		for begin in range(0, len(words) - span+1):
			end = begin + span
			for split in range(begin+1, end):
				for A in nonTerms:
					for B in nonTerms:
						for C in nonTerms:
							if (A,B,C) in grammar.keys():
								prob = score[begin][split][nontermLabel[B]] * score[split][end][nontermLabel[C]] * grammar[(A,B,C)]
								if prob > score[begin][end][nontermLabel[A]]:
									score[begin][end][nontermLabel[A]] = prob
									
								
			# handling unary
			added = True
			while added:
				added = False
				for A in nonTerms:
					for B in nonTerms:
						if (A,B) in grammar.keys():
							prob = grammar[(A,B)]* score[begin][end][nontermLabel[B]]
							if prob > score[begin][end][nontermLabel[A]]:
								score[begin][end][nontermLabel[A]] = prob
								added = True 
				


	finalScore = score[0][len(words)][nontermLabel['S']]
	return finalScore


# testing function
print CKY(['fish','people','fish','tanks'])
print CKY(['people','with','fish','rods','fish','people'])
print CKY(['fish','with','fish','fish'])
print CKY(['fish','with','tanks','people','fish'])
print CKY(['fish','people','with','tanks','fish','people','with','tanks'])
print CKY(['fish','fish','fish','fish','fish'])
print CKY(['rods','rods','rods','rods'])
