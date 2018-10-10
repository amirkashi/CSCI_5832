###### ------------------------------------------------------------------- ######
# HW-4
# Amir Kashipazha 
###### ------------------------------------------------------------------- ######


from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from collections import defaultdict


# write output file  
f = open("eng.guessa", 'w')

# function to reading inpuf files 

def readconll(file):
    lines = [line.strip() for line in open(file)]
    while lines[-1] == '':  # Remove trailing empty lines
        lines.pop()
    s = [x.split('_') for x in '_'.join(lines).split('__')]  # Quick split corpus into sentences
    return [[y.split() for y in x] for x in s]


# each sentece saved in one list , and all senteces are saved in a large list 
eng_train = readconll("eng.train")  # making list from eng.train
eng_testa = readconll("eng.testa")  # making list from eng.testa

#print eng_train
#print eng_testa[1]


###### ------------------------------------------------------------------- ######
# this function makes features, label , and first step of output file at a time
# we need features of this function for training set and test set
# we need label of this functionf for test set
# we need test_to_file of this function for printing results to an output file 
###### ------------------------------------------------------------------- ######
def read_INP( TXT ):
	features = []
	labels = []
	test_to_file =[]
	for sentences in TXT:
		#print len(sentences)
		#print sentences[0]
		for j in range(0, len(sentences)):
			#print sentences[j]
			#print j, len(sentences)
			temp_dic = {}
			if len(sentences) == 1: # if there is one word in sentence 
				temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1 } )
			
			elif len(sentences) == 2: # if there are 2 words in the sentence 
				if j == 0:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j+1][1]:1   # 1 tag after 
					} )
				else:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1, # one tag before 
					
					 } )
			elif len(sentences) == 3: # if there are 3 words in the sentence 
				if j == 0:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j+1][1]:1,   # 1 tag after
					sentences[j+2][1]:1 }) # 2 tag after 
				elif j == 1:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1, # 1 tag before
					sentences[j+1][1]:1 # 1 tag after
					 })
				else:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,   # 1 tag before
					sentences[j-2][1]:1  # 2 tag before
					}) 
					
			
			else:
				if j == 0: # first word in sentence 
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j+1][1]:1,      # one tag after
					sentences[j+2][1]:1  } )  # two tag after 
				elif j== 1: # 2nd words in sentence 
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j+1][1]:1,  #one tag after 
					sentences[j+2][1]:1,  # two tag after
					sentences[j-1][1]:1,  # one tag before 
					}) 
				
				elif j==len(sentences)-1: # last word 
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,  # one tag before 
					sentences[j-2][1]:1 }),  # two tag before
				elif j==len(sentences)-2:  # one word before the last word
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,  # one tag before 
					sentences[j-2][1]:1,    # two tag before
					sentences[j+1][1]:1})   # one tag after 
					
				else:
					temp_dic.update( {sentences[j][0]:1, sentences[j][1]:1, sentences[j][2]:1, 
					sentences[j-1][1]:1,  # one tag before 
					sentences[j-2][1]:1,    # two tag before
					sentences[j+1][1]:1,   # one tag after 
					sentences[j+2][1]:1})   # two tag after 
						
			
			labels.append( sentences[j][3])
			features.append( temp_dic )
			temp_list =[ sentences[j][0], sentences[j][1], sentences[j][2], sentences[j][3]] # to save each line in a list 
			test_to_file.append(temp_list) # for printing 
	return labels, features, test_to_file


# label is the label form training data
# features is the feaures to learn from the training data
# dont_useme1, this one is not used here, it will be used to print output for test. it is in the founction to calculate every thing we net at a time
labels, features, dont_useme1 = read_INP( eng_train )



###### making tests
# dont_useme2 it is label function create for train data but we dont need it , 
# i make the function to make all at a time and use what we need 
# test_list: is test set info including word, POS , and other related information
# test to file is first step of printing ouptut , it is the same as test set but it does not have empty line
dont_useme2, test_list, test_to_file = read_INP( eng_testa )
		


vectorizer = DictVectorizer(sparse = True)
X = vectorizer.fit_transform(features)
clf = svm.LinearSVC()                             # use Linear SVM
clf.fit(X, labels)                                     # train classifier


###### ------------------------------------------------------------------- ######
# This for loop predict the NER then added to its related line,
# or appended to the list of specific word that has POS and ....
###### ------------------------------------------------------------------- ######
for i in range(0, len(test_list)):
	test_to_file[i].append( ( clf.predict(vectorizer.transform([ test_list[i] ])) )[0] )


# this for loop print result to an output file 
for j in range(0, len(test_to_file)):
	print >>f, test_to_file[j][0], test_to_file[j][1], test_to_file[j][2], test_to_file[j][3], test_to_file[j][4]

f.close()
