from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from collections import defaultdict


f = open("eng.guessa", 'w')

def readconll(file):
    lines = [line.strip() for line in open(file)]
    while lines[-1] == '':
        lines.pop()
    s = [x.split('_') for x in '_'.join(lines).split('__')]
    return [[y.split() for y in x] for x in s]

eng_train = readconll("eng.train")
eng_testa = readconll("eng.testa")

def read_INP(TXT):
	features = []
	labels = []
	test_to_file = []
	for sentences in TXT:
		for j in range(0, len(sentences)):
			temp_dic = {}
			if len(sentences) == 1:
				temp_dic.update({sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1 } )
			elif len(sentences) == 2:
				if j == 0:
					temp_dic.update({sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1,
					sentences[j+1][1]:1
					})
				else:
					temp_dic.update({sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,
					 } )
			elif len(sentences) == 3:
				if j == 0:
					temp_dic.update({sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j+1][1]:1,
					sentences[j+2][1]:1 })
				elif j == 1:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,
					sentences[j+1][1]:1
					 })
				else:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,
					sentences[j-2][1]:1
					}) 
			else:
				if j == 0:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j+1][1]:1,
					sentences[j+2][1]:1  })
				elif j == 1:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j+1][1]:1,
					sentences[j+2][1]:1,
					sentences[j-1][1]:1,
					})
				elif j==len(sentences)-1:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,
					sentences[j-2][1]:1 }),
				elif j==len(sentences)-2:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,
					sentences[j-2][1]:1,
					sentences[j+1][1]:1})
				else:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,
					sentences[j-2][1]:1,
					sentences[j+1][1]:1,
					sentences[j+2][1]:1})
			
			labels.append(sentences[j][3])
			features.append(temp_dic)
			temp_list = [sentences[j][0], sentences[j][1], sentences[j][2], sentences[j][3]]
			test_to_file.append(temp_list)
	return labels, features, test_to_file

labels, features, dont_useme1 = read_INP(eng_train)
dont_useme2, test_list, test_to_file = read_INP(eng_testa)
vectorizer = DictVectorizer(sparse=True)
X = vectorizer.fit_transform(features)
clf = svm.LinearSVC()
clf.fit(X, labels)
for i in range(0, len(test_list)):
	test_to_file[i].append((clf.predict(vectorizer.transform([test_list[i]])))[0])
for j in range(0, len(test_to_file)):
	print >>f, test_to_file[j][0], test_to_file[j][1], test_to_file[j][2], test_to_file[j][3], test_to_file[j][4]
f.close()
