#  string-to-fo.py
#  
#  Copyright 2018 Mai Ha Vu<maiha@udel.edu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# 
 
#  Description: Takes a file that has a list of strings in them as input, and outputs a series of First-Order statements about these strings
#  Parameters: 
#		inputfile -- a text file with a list of strings, each string separated by new line
# 		outputfile -- a text file where the output of the function will be written
# 		wordmodel_type -- type of alphabet we want to use to label elements in the strings, options are: lhor-features, lhor, abc, robot-features, robot
#		binary_rel -- type of ordering relations we want to use to describe the binary relation between elements in the strings, options are: precedence, adjacency





import glob
import sys
from itertools import permutations, repeat, product, chain, combinations
import itertools
from string import ascii_uppercase


inputfile = sys.argv[1]
outputfile = sys.argv[2]
wordmodel_type = sys.argv[3] #5 types: lhor-features, lhor, abc, robot-features, robot
binary_rel = sys.argv[4] #2 types: precedence and adjacency

#generates a dummy list to use as variables
dummy_lst = list(ascii_uppercase) + list(''.join(words) for words in list(combinations(ascii_uppercase,2))) + list(''.join(words) for words in list(combinations(ascii_uppercase,3))) + list(''.join(words) for words in list(combinations(ascii_uppercase,4)))
dummy_str_lst = ['S' + mystring for mystring in map(str,list(range(3000)))]


#translates a string with alphabet [l,h,L,H] into a wordmodel with [l,h,str] labels
def string_to_wordmodel_lhorfeatures(string):
	wordmodel = []
	for i in range(len(string)):
		feature = set()
		if string[i] == 'h':
			feature = feature | (set(['h']))
		if string[i] == 'H':
			feature = feature | (set(['h','str']))
		if string[i] == 'L':
			feature = feature | (set(['l','str']))
		if string[i] == 'l':
			feature = feature | (set(['l']))
		wordmodel.append(feature)
	return wordmodel

#translates a string with alphabet [l,h,L,H] into a wordmodel with [l,h,L,H] labels
def string_to_wordmodel_lhor(string):
	wordmodel = []
	for i in range(len(string)):
		feature = set()
		if string[i] == 'h':
			feature = feature | (set(['h']))
		if string[i] == 'H':
			feature = feature | (set(['hstr']))
		if string[i] == 'L':
			feature = feature | (set(['lstr']))
		if string[i] == 'l':
			feature = feature | (set(['l']))
		wordmodel.append(feature)
	#print wordmodel
	return wordmodel

#translates a string with alphabet [a,b,c] into a wordmodel with [a,b,c] labels, augments with initial and final
def string_to_wordmodel_abc(string):
	aug_string = 'x' + string + 'x'
	wordmodel = []
	for i in range(len(aug_string)):
		feature = set()
		if aug_string[i] == 'a':
			feature = feature | (set(['a']))
		if aug_string[i] == 'b':
			feature = feature | (set(['b']))
		if aug_string[i] == 'c':
			feature = feature | (set(['c']))
		if i == 0:
			feature = feature | (set(['initial']))
		if i == len(aug_string)-1:
			feature = feature | (set(['final']))
		wordmodel.append(feature)
	return wordmodel

#translates a string with robot movement alphabet into a wordmodel with robot movement labels, augments with initial and final
def string_to_wordmodel_robot(string):
	string = 'x' + string + 'x'
	wordmodel = []
	for i in range(len(string)):
		feature = set()
		if string[i] == 'a':
			feature = feature | (set(['a']))
		if string[i] == 'b':
			feature = feature | (set(['b']))
		if string[i] == 'c':
			feature = feature | (set(['c']))
		if string[i] == 'd':
			feature = feature | (set(['d']))
		if string[i] == 'A':
			feature = feature | (set(['a-prime']))
		if string[i] == 'B':
			feature = feature | (set(['b-prime']))
		if string[i] == 'C':
			feature = feature | (set(['c-prime']))
		if string[i] == 'D':
			feature = feature | (set(['d-prime']))
		if string[i] == 't':
			feature = feature | (set(['t']))
		if i == 0:
			feature = feature | (set(['initial']))
		if i == len(string)-1:
			feature = feature | (set(['final']))
		wordmodel.append(feature)
	return wordmodel

#translates a string with robot movement alphabet into a wordmodel where atomic features make up each letter, augments with initial and final		
def string_to_wordmodel_robotfeatures(string):
	aug_string = 'x' + string + 'x'
	#print aug_string
	wordmodel = []
	for i in range(len(aug_string)):
		feature = set()
		if aug_string[i] == 'a':
			feature = feature | (set(['crawler','move','untethered']))
		if aug_string[i] == 'b':
			feature = feature | (set(['crawler','stop','untethered']))
		if aug_string[i] == 'c':
			feature = feature | (set(['quad','move','untethered']))
		if aug_string[i] == 'd':
			feature = feature | (set(['quad','stop','untethered']))
		if aug_string[i] == 'A':
			feature = feature | (set(['crawler','move','tethered']))
		if aug_string[i] == 'B':
			feature = feature | (set(['crawler','stop','tethered']))
		if aug_string[i] == 'C':
			feature = feature | (set(['quad','move','tethered']))
		if aug_string[i] == 'D':
			feature = feature | (set(['quad','stop','tethered']))
		if aug_string[i] == 't':
			feature = feature | (set(['attach','move','crawler']))
		if i == 0:
			feature = feature | (set(['initial']))
		if i == len(aug_string)-1:
			feature = feature | (set(['final']))
		wordmodel.append(feature)
	return wordmodel

#translates a list of alphabet into FO statements. e.g. [('initial'),(['crawler','move','untethered']),(['quad','move','tethered']),(['final])] --> initial(A), crawler(B), move(B), untethered(B), quad(C), etc.	
def wordmodel_to_features(wordmodel):
	feature_list = []
	for m in range(len(wordmodel)):
		for f in wordmodel[m]:
			feature_list.append(f + '(' + dummy_lst[m] + ')')
	return feature_list 
	
#print wordmodel_to_features(string_to_wordmodel('hHlL'))

#takes a wordmodel and returns all precedence relations in it
def wordmodel_to_precedence(wordmodel):
	precedence_list = []
	variable_combos = []
	for i in permutations(dummy_lst[:len(wordmodel)],2):
		variable_combos.append("".join(i))
	for i in variable_combos:
		if dummy_lst.index(i[0]) < dummy_lst.index(i[1]):
			precedence_list.append('follows(' + i[0] + ',' + i[1] + ')')
	return precedence_list

#takes a wordmodel and returns all adjacency relations in it
def wordmodel_to_adjacency(wordmodel):
	adjacency_list = []
	for i in dummy_lst[:len(wordmodel)]:
		if dummy_lst.index(i[0]) < dummy_lst.index(i[1]):
			adjacency_list.append('adjacent(' + i[0] + ',' + i[1] + ')')

#zip a nested list with a list. For a = [[h,l],[l,l,l],[h]] and b [a,b,c,d,e,f,g,h,i], zip_nestedlst_lst(a,b) = [[a,b],[c,d,e],[f]]
def zip_nestedlst_lst(lst_of_lst,lst):
	size = sum(len(sublst) for sublst in lst_of_lst)
	j = 0
	while j!=size:
		for l in lst_of_lst:
			for i in range(len(l)):
				l[i]=lst[j]
				j += 1
	return lst_of_lst
	
#takes a list of wordmodels (which are also lists), and returns the right precedences in it
def wordmodel_lst_to_precedence(wordmodel_list): 
	precedence_list = []
	variable_combos = []
	abc_list = zip_nestedlst_lst(wordmodel_list,dummy_lst)
	for abc in abc_list:
		for i in permutations(abc,2):
			variable_combos.append(i)
	for i in variable_combos:
		if dummy_lst.index(i[0]) < dummy_lst.index(i[1]):
			precedence_list.append('follows(' + i[0] + ',' + i[1] + ')')
	return precedence_list

#takes a list of wordmodels (which are also lists), and returns the right adjacencies in it
def wordmodel_lst_to_adjacency(wordmodel_list): 
	adjacency_list = []
	abc_list = zip_nestedlst_lst(wordmodel_list,dummy_lst)
	for i in abc_list:
		for j in range(len(i)-1):
			adjacency_list.append('adjacent(' + i[j] + ',' + i[j+1] + ')')
	return adjacency_list
	
#assigns stress to strings
def assign_stress(lst):
	string_lst = [list(word) for word in lst]
	zip_nestedlst_lst(string_lst,dummy_lst)
	stress_assignment = []
	for i in range(len(string_lst)):
		for char in lst[i]:
			#print char
			if wordmodel_type == 'lhor-features':
				if char == 'H' or char == 'L':
					stress_assignment.append('hasStress(' + dummy_str_lst[i] + ')')
			else:
				if char == 'H':
					stress_assignment.append('hasHstr(' + dummy_str_lst[i] + ')')
				if char == 'L':
					stress_assignment.append('hasLstr(' + dummy_str_lst[i] + ')')				
	return stress_assignment


#print statements that declare strings in a list
def list_strings(lst):
	string_assignment = []
	for i in range(len(lst)):
		string_assignment.append('isString(' + dummy_str_lst[i] + ')')
	return string_assignment

#given a wordmodel and preferred binary relation, it lists all FO statements about it with that binary relation
def wordmodel_to_fo(wordmodel): 
	if binary_rel == 'precedence':
		fo = wordmodel_to_features(wordmodel) + wordmodel_to_precedence(wordmodel)
	if binary_rel == 'adjacency':
		fo = wordmodel_to_features(wordmodel) + wordmodel_to_adjacency(wordmodel)
	return fo
	

#given a list of strings, it outputs FO statements about all strings				
def string_lst_to_fo(lst):
	if wordmodel_type == 'lhor-features':
		wordmodel_lst = map(string_to_wordmodel_lhorfeatures,lst) 
	if wordmodel_type == 'lhor':
		wordmodel_lst = map(string_to_wordmodel_lhor,lst) 
	if wordmodel_type == 'abc':
		wordmodel_lst = map(string_to_wordmodel_abc,lst)
	if wordmodel_type == 'robot':
		wordmodel_lst = map(string_to_wordmodel_robot,lst)
	if wordmodel_type == 'robot-features':
		wordmodel_lst = map(string_to_wordmodel_robotfeatures,lst)
	#print wordmodel_lst
	if wordmodel_type == 'lhor-features' or wordmodel_type == 'lhor':
		wordmodel_features = wordmodel_to_features(list(chain(*wordmodel_lst))) + assign_stress(lst) + list_strings(lst)
	else:
		wordmodel_features = wordmodel_to_features(list(chain(*wordmodel_lst)))
	if binary_rel == 'precedence':
		fo_lst = wordmodel_features + wordmodel_lst_to_precedence(wordmodel_lst)
	if binary_rel == 'adjacency':
		fo_lst = wordmodel_features + wordmodel_lst_to_adjacency(wordmodel_lst)
	return fo_lst



with open(outputfile,'wb') as fo_lst:
	with open(inputfile,'r') as str_lst:
		if wordmodel_type == 'abc' or wordmodel_type =='robot' or wordmodel_type == 'robot-features':
			string_list = [string[:len(string)-2] for string in str_lst]
		else:
			string_list = [string[:len(string)-1] for string in str_lst]
		for f in string_lst_to_fo(string_list):
			fo_lst.write(f + "\n")	


