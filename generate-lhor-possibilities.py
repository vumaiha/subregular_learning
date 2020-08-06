#  generate-lhor-possibilities.py
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
 
#  Description: Generates all length n strings over the alphabet (l,L,h,H)
#  Parameters: 
# 		outputfile -- a text file where the output of the program will be written
# 		length -- desired length for strings

import sys
from itertools import permutations, repeat, product, chain, combinations
import itertools
import string

outputfile = sys.argv[1]
length = int(sys.argv[2])

def genLHOR (n):
	lst = []
	tuples = list(product('lLhH', repeat=n))
	for s in tuples:
		lst.append("".join(s))
	return lst

lhor_lst = genLHOR(length)

sorted_lst = sorted(lhor_lst, key=str.lower)

print sorted_lst

with open(outputfile,'wb') as string_lst:
	for count, element in enumerate(sorted_lst, 1):
		string_lst.write(element + '\n')
		if count % (length*length) == 0:
			string_lst.write('\n\n')

