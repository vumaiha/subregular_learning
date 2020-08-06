#  generate-data.py
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
 
#  Description: Generates random strings for Leftmost Heavy Ortherwise Rightmost stress rule
#  Parameters: 
# 		outputfile -- a text file where the output of the program will be written
# 		n -- desired length for strings, by default it is 6



import sys
from itertools import permutations, repeat, product, chain, combinations
import itertools
import random
import string

outputfile = sys.argv[1]
n = int(sys.argv[2])

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))


random_str_lst = []

#generates random sequence made of 'l' and 'h'
for i in range(n):
	random_str_lst.append(random_generator(random.randint(1,5), 'lh'))

#assigns stress to a list of random strings made of 'l' and 'h'. Left most 'h' gets stress, otherwise rightmost 'l' does. Stress is noted with capitalized 'H' or 'L'.
def assign_stress(str_lst):
	temp_str_lst = []
	new_str_lst = []
	for s in str_lst:
		temp_str_lst.append(list(s))
	for s in temp_str_lst:
		i = 0
		while i != len(s)-1 and s[i] != 'h':		
			i += 1	
		if s[i] == 'h':
			s[i] = 'H'
		else:
			s[i] = 'L'
	for s in temp_str_lst:
		new_str_lst.append("".join(s))
	return new_str_lst

lhor_strings = assign_stress(random_str_lst)

with open(outputfile,'wb') as string_lst:
	for s in lhor_strings:
		string_lst.write(s + '\n')			
				
	
