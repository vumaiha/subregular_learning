# Subregular_learning project

Scripts written to generate inputs for [Alchemy's](https://alchemy.cs.washington.edu/) statistical inference algorithm. They was used to run a number of machine learning experiments, as published in [Fronteries in Robotics and AI](https://www.frontiersin.org/articles/10.3389/frobt.2018.00076/full).

## Program files

1. generate-data.py

   Generates random strings for Leftmost Heavy Ortherwise Rightmost stress rule. It first generates random strings of n-length over the alphabet (l,h), then assigns stress based on the rule.
  
2. string-to-fo.py

   Translates a list of strings into First-order (FO) statements about those strings. 
   
   For example, running `python string-to-fo.py input.txt output.txt abc adjacency` for string ''bc'' in input.txt would yield the following statements in output.txt:
  
   initial(A)
  
   b(B)
  
   c\(C\)
  
   final(D)
  
   adjacent(A,B)
  
   adjacent(B,C)
  
   adjacent(C,D)

3. generate-statements.py
   
   Generates all 2-grams given a word model.
   
   For ecxample, running `python generate-statements.py output.txt abc precedence` yields the following statements in output.txt:
   
   0 adjacent(x,y) ^ a(x) ^ a(y)
   
   0 adjacent(x,y) ^ a(x) ^ b(y)
   
   0 adjacent(x,y) ^ a(x) ^ c(y)
   
   0 adjacent(x,y) ^ b(x) ^ a(y)
   
   0 adjacent(x,y) ^ b(x) ^ b(y)
   
   0 adjacent(x,y) ^ b(x) ^ c(y)
   
   0 adjacent(x,y) ^ c(x) ^ a(y)
   
   0 adjacent(x,y) ^ c(x) ^ b(y)
   
   0 adjacent(x,y) ^ c(x) ^ c(y)
