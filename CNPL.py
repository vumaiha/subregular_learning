import glob
import sys
import re
from itertools import permutations, repeat, product, chain, combinations
import itertools

#alphabet = glob.glob(sys.argv[1])
#training = glob.glob(sys.argv[2])
#grammar = glob.glob(sys.argv[3])

alphabet = ['<','>','a','b','c','d','B','g','D','G']
data_string = ['Ba','Bd','dG','BD','DB','Dg','Gb','Gc','>a','>D','b<','c<','g<','a<']

alphabet1 = ['h', 'l', 'H', 'L']

alphabet2 = ['h', 'l', 'str', 'syl']

#data_string = ['Hhh', 'lllL', 'lHll', 'H', 'L']

weight = ['h', 'l']
stress = ['str']


pos_substrings = set()

req_substrings = set()

banned_substrings = set()

substring_list = [] 
#list of substrings per word


substring_list_wm = []
feature_list_wm = []
observed_substrings = set()
#set of all observed substrings in input wordlist

#word = [(h,s),(l),(l),(l)]

def string_to_wordmodel(string):
	wordmodel = []
	for c in string:
		if c == 'h':
			wordmodel.append(frozenset(['h', 'syl']))
		if c == 'H':
			wordmodel.append(frozenset(['h','str', 'syl']))
		if c == 'L':
			wordmodel.append(frozenset(['l','str', 'syl']))
		if c == 'l':
			wordmodel.append(frozenset(['l', 'syl']))
	return wordmodel
	
def wordmodel_to_string(wordmodel):
	string = []
	for i in wordmodel:
		if i == {'h'}:
			string.append('h')
		if i == {'h','s'}:
			string.append('H')
		if i == {'l','s'}:
			string.append('L')
		if i == {'l'}:
			string.append('l')
	return ''.join(string)

#print string_to_wordmodel('hHHhlll')

data_wordmodel = map(string_to_wordmodel,data_string)

#print data

#print map(wordmodel_to_string,data)

#gets required substrings and banned substrings given a list of strings
for w in data_string:
	substrings = set()
	for i in range(len(w)-1):
		substring = w[i] + w[i+1]
		substrings.add(substring)
	substring_list.append(substrings)
print substring_list
req_substrings=set.intersection(*substring_list)
observed_substrings = set.union(*substring_list)
#print 'required substrings:', req_substrings



for i in permutations(alphabet, 2):
    pos_substrings.add("".join(i))
for i in range(len(alphabet)):
	pos_substrings.add(alphabet[i]+alphabet[i]) 
#print 'all possible substrings:', pos_substrings


print 'observed substrings:', observed_substrings
banned_substrings = pos_substrings - observed_substrings

print 'banned substrings:', banned_substrings

	
#gets required substrings given a list of word models	

#print data_wordmodel

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))


for w in data_wordmodel:
	substrings = set()
	substring_set = set()
	features = set()
	last_substring = set()
	for i in range(len(w)-1):
		substrings = set(product(list(powerset(w[i])),list(powerset(w[i+1])))) | set(powerset(w[i]))
		for substring in substrings:
			#print substring 
			substring_set.add(substring)
	#print substring_set
	#last_substring = set(powerset(w[len(w)-1]))
	for substring in last_substring:
		substring_set.add(substring)
	substring_list_wm.append(substring_set)

req_substrings_wm=set.intersection(*substring_list_wm)
observed_substrings_wm = set.union(*substring_list_wm)

#print substring_list_wm
#print observed_substrings_wm
#print req_substrings_wm

	#for l in range(len(w)):
		##print w[l]
		#substrings.add(w[l])
		#for j in range(len(alphabet2)):
			#if alphabet2[j] in w[l]:
				#features.add(alphabet2[j])
	#substring_list_wm.append(substrings)
	#feature_list_wm.append(features)
	#print substrings
#print feature_list_wm
#print substring_list_wm

	
#req_substrings_wm=set.intersection(*substring_list_wm) | set.intersection(*feature_list_wm)
#observed_substrings = set.union(*substring_list)
#print 'required substrings:', req_substrings_wm
