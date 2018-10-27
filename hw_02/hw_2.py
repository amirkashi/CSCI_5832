# -*- coding: utf-8 -*-
import codecs
import math
import operator


def classify(text, language_classes):
	sigma = 0.1
	alphabet_size = 32.0
	test_case = " " + text
	languages_score = {}
	for language in language_classes:
		score_of_each_language = 0.0
		for i in range(0, len(test_case) - 1):
			l1 = test_case[i]
			l2 = test_case[i + 1]
			frequency_of_l1_l2 = float(language_classes[language].get(l1 + l2, 0))
			frequency_of_l1 = float(language_classes[language].get(l1, 0))
			p = (frequency_of_l1_l2 + sigma) / (frequency_of_l1 + sigma * alphabet_size)
			score_of_each_language += math.log(p)
		languages_score[language] = score_of_each_language
	sorted_score = sorted(languages_score.items(), key=operator.itemgetter(1), reverse = True)
	return sorted_score[0][0], sorted_score

def main():
	alphabet_list = set()
	languages = ['de', 'en', 'nl', 'sv']
	alphabet_list = set()
	language_classes = {}
	for language in languages:
		unigram_bigram = {}
		for line in codecs.open(language, 'r', encoding='utf-8'):
			line = line.strip()
			for letter in line:
				alphabet_list.add(letter)
				if letter in unigram_bigram:
					unigram_bigram[letter] += 1
				else:
					unigram_bigram[letter] = 1
			for letter in range(0, len(line) - 1):
				bigram = line[letter] + line[letter + 1]
				if bigram in unigram_bigram:
					unigram_bigram[bigram] += 1
				else:
					unigram_bigram[bigram] = 1
		language_classes[language] = unigram_bigram
	print classify(u'this is a very short text', language_classes)
	print classify(u'dies ist ein sehr kurzer text', language_classes)
	print classify(u'dit is een zeer korte tekst', language_classes)
	print classify(u'detta är en mycket kort text', language_classes)	
main()
