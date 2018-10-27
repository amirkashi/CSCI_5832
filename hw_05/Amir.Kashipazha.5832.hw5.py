import numpy as np

# grammar was taken form course assingnment website
grammar = {
    ('S', 'NP', 'VP'): 0.9,
    ('S', 'VP'): 0.1,
    ('VP', 'V', 'NP'): 0.5,
    ('VP', 'V'): 0.1,
    ('VP', 'V', '@VP_V'): 0.3,
    ('VP', 'V', 'PP'): 0.1,
    ('@VP_V', 'NP', 'PP'): 1.0,
    ('NP', 'NP', 'NP'): 0.1,
    ('NP', 'NP', 'PP'): 0.2,
    ('NP', 'N'): 0.7,
    ('PP', 'P', 'NP'): 1.0,
    ('N', 'people'): 0.5,
    ('N', 'fish'): 0.2,
    ('N', 'tanks'): 0.2,
    ('N', 'rods'): 0.1,
    ('V', 'people'): 0.1,
    ('V', 'fish'): 0.6,
    ('V', 'tanks'): 0.3,
    ('P', 'with'): 1.0
}

nonTermsSet = set()
for w in grammar:
	nonTermsSet.add(w[0])
nonTerms = list(nonTermsSet)
nontermLabel = {}
for i in range(0, len(nonTerms)):
	nontermLabel[nonTerms[i]] = i

def CKY(words):
	score = np.zeros( (len(words)+1, len(words)+1, len(nonTerms)) ) 
	for i in range(0, len(words)):
		for A in nonTerms:
			if (A, words[i]) in grammar:
				score[i][i+1][nontermLabel[A]] = grammar[(A,words[i])]
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
	for span in range(2, len(words)+1):
		for begin in range(0, len(words) - span+1):
			end = begin + span
			for split in range(begin+1, end):
				for A in nonTerms:
					for B in nonTerms:
						for C in nonTerms:
							if (A, B, C) in grammar.keys():
								prob = score[begin][split][nontermLabel[B]] * score[split][end][nontermLabel[C]] * grammar[(A, B, C)]
								if prob > score[begin][end][nontermLabel[A]]:
									score[begin][end][nontermLabel[A]] = prob
			added = True
			while added:
				added = False
				for A in nonTerms:
					for B in nonTerms:
						if (A, B) in grammar.keys():
							prob = grammar[(A, B)] * score[begin][end][nontermLabel[B]]
							if prob > score[begin][end][nontermLabel[A]]:
								score[begin][end][nontermLabel[A]] = prob
								added = True
	finalScore = score[0][len(words)][nontermLabel['S']]
	return finalScore

print CKY(['fish', 'people', 'fish', 'tanks'])
print CKY(['people', 'with', 'fish', 'rods', 'fish', 'people'])
print CKY(['fish', 'with', 'fish', 'fish'])
print CKY(['fish', 'with', 'tanks', 'people', 'fish'])
print CKY(['fish', 'people', 'with', 'tanks', 'fish', 'people', 'with', 'tanks'])
print CKY(['fish', 'fish', 'fish', 'fish', 'fish'])
print CKY(['rods', 'rods', 'rods', 'rods'])
