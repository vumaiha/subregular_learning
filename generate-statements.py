#  generate-statements.py
#  
#  Copyright 2020 Mai Ha Vu<maiha@udel.edu>
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
 
#  Description: Generates all possible FO statements, given the type of alphabet and binary relations
#  Parameters: 
# 		outputfile -- a text file where the output of the function will be written
# 		statement -- type of alphabet we want to use to label elements in the strings, options are: advanced model (AM), standard model (SM), abc, robot, robot-features
#		binary_rel -- type of ordering relations we want to use to describe the binary relation between elements in the strings, options are: precedence, adjacency



import sys
from itertools import permutations, repeat, product, chain, combinations
import itertools

outputfile = sys.argv[1]
statement_type = sys.argv[2] #3 types: advanced model (AM), standard model (SM), abc, robot, robot-features
binary_rel = sys.argv[3] #2 types: precedence and adjacency

am_literals = ['str','h','l']

weight_literals = ['h','l']
stress_literals = ['str']
sm_literals = ['h', 'l', 'H', 'L']
position_literal = ['initial','final']
abc_alphabet = ['a','b','c']

robot_sm_literals = ['a','b','c','d','a-prime','b-prime','c-prime','d-prime','t']
robot_am_literals = ['crawler','quad','move','stop','tethered','untethered','attach']

robot_agent = ['crawler','quad']
robot_movement = ['move','stop']
robot_tether = ['untethered','tethered','attach']

def combine_lsts(lst1,lst2):
	joined_lst = lst1 + lst2
	combo_lst = list(product(lst1,lst2)) 
	for i in joined_lst:
		combo_lst.append(i)
	return combo_lst

#print combine_lsts(weight_literals, stress_literals)	


def combine_3_lsts(lst1,lst2,lst3):
	joined_lst = lst1+lst2+lst3	
	combo_lst = list(product(lst1,lst2,lst3)) + list(product(lst1,lst2)) + list(product(lst1,lst3)) + list(product(lst2,lst3)) 
	for i in joined_lst:
		combo_lst.append(i)
	return combo_lst


print combine_3_lsts(robot_agent,robot_movement,robot_tether)
print combine_lsts(weight_literals, stress_literals)	
	
#generates list of possible fo statements for a variable, e.g. h(x)^str(x)
def generate_fo(lst,var):
	fo_lst = []
	for i in lst:
		if len(i)==3:
			fo_lst.append(i[0]+'('+var+') ^ '+i[1]+'('+var+') ^ ' + i[2]+'('+var+')')
		else:
			if len(i)==2:
				fo_lst.append(i[0]+'('+var+') ^ '+i[1]+'('+var+')')
			else:
				fo_lst.append(i+'('+var+')')
	return fo_lst
	

#takes results of combine_list
def generate_2gram_statements(lst):
	statement_lst = []
	for i in generate_fo(lst,'x'):
		for j in generate_fo(lst,'y'):
			if statement_type == 'AM':
				statement_lst.append('follows(x,y) ^ '+i+' ^ '+j)
			if statement_type == 'SM':
				statement_lst.append('follows(x,y)^ '+i+ ' ^ ' +j)
			#we assume that for 'abc' type we always take adjacency
			if statement_type == 'abc':
				statement_lst.append('adjacent(x,y) ^ '+i+' ^ '+j)
			if statement_type == 'robot':
				statement_lst.append('adjacent(x,y) ^ '+i+' ^ '+j)
			if statement_type == 'robot-features':
				statement_lst.append('adjacent(x,y) ^ '+i+' ^ '+j)
	return statement_lst
	
def generate_robot_2gram(lst1,lst2):
	statement_lst = []
	for i in generate_fo(lst1,'x'):
		for j in generate_fo(lst2,'y'):
			statement_lst.append('adjacent(x,y) ^ '+i+' ^' + j)
	return statement_lst
	
#print generate_2gram_statements(abc_alphabet)

#takes list of literals
def generate_req_statements(lst):
	req_lst = []
	for i in lst:
		if binary_rel == 'precedence':
			req_lst.append('initial(x) ^ final(z) ^ (follows(x,z) v x = z) ^ Exist y (((follows(x,y) ^ follows(y,z)) v x = y v y = z) ^ '+i+'(y))')
		if binary_rel == 'adjacency':
			req_lst.append('initial(x) ^ final(z) ^ (follows(x,z) v x = z) ^ Exist y (((adjacent(x,y) ^ follows(y,z)) v x = y v y = z) ^ '+i+'(y))')
	return req_lst
	
def generate_initial_statements(lst):
	initial_lst = []
	for i in lst:
		if len(i)==3:
			initial_lst.append('adjacent(x,y) ^ initial(x) ^ ' + i[0]+'(y) ^ '+i[1]+'(y) ^ ' + i[2]+'(y)')
		else:
			if len(i)==2:
				initial_lst.append('adjacent(x,y) ^ initial(x) ^ ' + i[0]+'(y) ^ '+i[1]+'(y)')
			else:
				initial_lst.append('adjacent(x,y) ^ initial(x) ^ '+ i + '(y)')
	return initial_lst
		
def generate_final_statements(lst):
	final_lst = []
	for i in lst:
		if len(i)==3:
			final_lst.append('adjacent(x,y) ^ ' + i[0]+'(x) ^ '+i[1]+'(x) ^ ' + i[2]+'(x) ^ final(y)')
		else:
			if len(i)==2:
				final_lst.append('adjacent(x,y) ^ ' + i[0]+'(x) ^ '+i[1]+'(x) ^ final(y)')
			else:
				final_lst.append('adjacent(x,y) ^ ' + i + '(x) ^ final(y)')
	if statement_type == 'robot-features':
		final_lst.append('adjacent(x,y) ^ attach(x) ^ final(y)')
	return final_lst
	
def generate_other_robot_statements(lst):
	attach_reel_lst = []
	for i in lst:
		if len(i)==3:
			attach_reel_lst.append('adjacent(x,y) ^ attach(x) ^ ' + i[0]+'(y) ^ '+i[1]+'(y) ^ ' + i[2]+'(y)')
			attach_reel_lst.append('adjacent(x,y) ^ ' + i[0]+'(x) ^ '+i[1]+'(x) ^ ' + i[2]+'(x) ^ attach(y)')
			attach_reel_lst.append('adjacent(x,y) ^ reel(x) ^ ' + i[0]+'(y) ^ '+i[1]+'(y) ^ ' + i[2]+'(y)')
			attach_reel_lst.append('adjacent(x,y) ^ ' + i[0]+'(x) ^ '+i[1]+'(x) ^ ' + i[2]+'(x) ^ reel(y)')
		else:
			if len(i)==2:
				attach_reel_lst.append('adjacent(x,y) ^ attach(x) ^ ' + i[0]+'(y) ^ '+i[1]+'(y)')
				attach_reel_lst.append('adjacent(x,y) ^ ' + i[0]+'(x) ^ '+i[1]+'(x) ^ attach(y)')
				attach_reel_lst.append('adjacent(x,y) ^ reel(x) ^ ' + i[0]+'(y) ^ '+i[1]+'(y)')
				attach_reel_lst.append('adjacent(x,y) ^ ' + i[0]+'(x) ^ '+i[1]+'(x) ^ reel(y)')
			else:
				attach_reel_lst.append('adjacent(x,y) ^ attach(x) ^ '+ i + '(y)')
				attach_reel_lst.append('adjacent(x,y) ^ ' + i + '(x) ^ attach(y)')
				attach_reel_lst.append('adjacent(x,y) ^ reel(x) ^ '+ i + '(y)')
				attach_reel_lst.append('adjacent(x,y) ^ ' + i + '(x) ^ reel(y)')
	attach_reel_lst.append('adjacent(x,y) ^ attach(x) ^ reel(y)')
	attach_reel_lst.append('adjacent(x,y) ^ reel(x) ^ attach(y)')
	return attach_reel_lst
	


lhor_AM_all_statement_lst = generate_2gram_statements(combine_lsts(weight_literals,stress_literals)) + generate_req_statements(am_literals)

lhor_SM_all_statement_lst = generate_2gram_statements(sm_literals) + generate_req_statements(sm_literals)

robot_SM_all_statement_lst = generate_2gram_statements(robot_sm_literals) + generate_initial_statements(robot_sm_literals) + generate_final_statements(robot_sm_literals)

robot_combo_lst = (list(product(robot_agent,robot_movement,robot_tether)))

robot_AM_all_statement_lst = generate_robot_2gram(robot_combo_lst,robot_am_literals) + generate_initial_statements(robot_am_literals) + generate_final_statements(robot_am_literals)

if statement_type == 'AM':
	with open(outputfile,'wb') as statement_lst:
		for statement in lhor_AM_all_statement_lst:
			statement_lst.write('0 ' + statement+'\n')
if statement_type == 'SM':
	with open(outputfile,'wb') as statement_lst:
		for statement in lhor_SM_all_statement_lst:
			statement_lst.write('0 ' + statement+'\n')
if statement_type == 'abc':
	with open(outputfile,'wb') as statement_lst:
		for statement in generate_2gram_statements(abc_alphabet):
			statement_lst.write('0 ' + statement+'\n')
if statement_type == 'robot':
	with open(outputfile,'wb') as statement_lst:
		for statement in robot_SM_all_statement_lst:
			statement_lst.write('0 ' + statement+'\n')
if statement_type == 'robot-features':
	with open(outputfile,'wb') as statement_lst:
		for statement in robot_AM_all_statement_lst:
			statement_lst.write('0 ' + statement+'\n')

