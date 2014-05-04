#!/usr/bin/python

import fileinput
import operator
import collections

def parse_line(line):
	words_string = line.split('.')
	return_array = []
	for word in words_string:
		return_array.append(word.split('-'))
	return return_array

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def conv_char_to_num(word_array):
	if(not is_number(word_array[0][0])):
		charnum = { "f":'1',"u":'2',"th":'3',"o":'4',"r":'5',"c":'6',"g":'7',"w":'8',"h":'9',"n":'10',"i":'11',"j":'12',"eo":'13',"p":'14',"x":'15',"s":'16',"t":'17',"b":'18',"e":'19',"m":'20',"l":'21',"ng":'22',"oe":'23',"d":'24',"a":'25',"ae":'26',"y":'27',"ia":'28',"io":'28',"ea":'29' }
		new_word_array = []
		for word in word_array:
			new_rune_array = []
			for rune in word:
				new_rune_array.append(charnum[rune])
			new_word_array.append(new_rune_array)
		return new_word_array
	else:
		return word_array

def wordnum(word_array):
	return len(word_array)

def runenum(word_array):
	count = 0
	for word in word_array:
		for rune in word:
			if rune != '30':
				count += 1
	return count
	
def get_distribution(word_array,rune_num):
	count_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for word in word_array:
		for rune in word:
			if(int(rune) < 30):
				count_array[int(rune)-1] += 1
	percentage = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	for i in range(0,29):
		percentage[i] = (count_array[i] / rune_num) * 100.0
	return_arrays = []
	return_arrays.append(count_array)
	return_arrays.append(percentage)
	return return_arrays

def calculate_ioc(count_array,n):
	count_sum = 0
	for count in count_array:
		count_sum += count*(count-1)
	return count_sum/(n*(n-1))

def calculate_friedman(ioc,n):
	phi = 1.0/29.0
	mu = 0.0614
	factor = ioc*(n-1)+mu-n*phi
	top = n*(mu-phi)
	return top/factor
	
def calculate_kasiski():
	pass

def calculate_ngram(words,n,min_appearance,respect_to_words=False):
	if not respect_to_words:
		# Put all runes into one array
		rune_array = []
		for word in words:
			for rune in word:
				if rune != '30':
					rune_array.append(rune)
		# Loop over runes 
		ngram = { }
		for i in range(0,len(rune_array)-(n-1)):
			ngram_word = ""
			for j in range(0,n):
				ngram_word += rune_array[i+j]
				if j != (n-1):
					ngram_word += "-"
			# Check if entry exists
			if ngram_word in ngram:
				ngram[ngram_word] += 1
			else:
				add_ngram = { ngram_word:1 }
				ngram.update(add_ngram)
	else:
		# Put all runes into one array
		rune_array = []
		for word in words:
			if len(word) >= n:
				word_array = []
				for rune in word:
					if rune != '30':
						word_array.append(rune)
				rune_array.append(word_array)
		# Loop over runes 
		ngram = { }
		for word in rune_array:
			for i in range(0,len(word)-(n-1)):
				ngram_word = ""
				for j in range(0,n):
					ngram_word += word[i+j]
					if j != (n-1):
						ngram_word += "-"
				# Check if entry exists
				if ngram_word in ngram:
					ngram[ngram_word] += 1
				else:
					add_ngram = { ngram_word:1 }
					ngram.update(add_ngram)
	# Sort out sequences that appear not often enough
	keyarray = []
	for key in ngram:
		if ngram[key] < min_appearance:
			keyarray.append(key)
	for key in keyarray:
		del ngram[key]
	# Sort dictionary descending
	sorted_ngram = sorted(sorted(ngram.items()),reverse=True,key=lambda x: x[1])
	return sorted_ngram
	
# Variables
words = []
number_of_words = 0
number_of_runes = 0
rune_distribution = []

for line in fileinput.input():
	words.extend(parse_line(line.replace("\n","")))

words = conv_char_to_num(words)
number_of_words = wordnum(words)
number_of_runes = runenum(words)
rune_distribution = get_distribution(words,number_of_runes)
ioc = calculate_ioc(rune_distribution[0],number_of_runes)
friedman = int(round(calculate_friedman(ioc,number_of_runes),0))

# CREATE DATAFILE
print(calculate_ngram(words,3,4,False))
"""
# Number of runes
print(str(number_of_runes)+"!!")
# IOC
print(str(ioc)+"!!")
# FRIEDMAN
print(str(friedman)+"!!")
# KASISKI
print("0!!")

print(",".join(str(x) for x in rune_distribution[0])+"!!")

# creat percentage
percentage = []
for perc in rune_distribution[1]:
	perc_string = '%.2f' % round(perc,2)
	percentage.append(perc_string+"%")
print(",".join(str(x) for x in percentage)+"!!")

# Print runes
counter = 0
unicode_runes = ['&#x00B7;','&#x16A0;','&#x16A2;','&#x16A6;','&#x16A9;','&#x16B1;','&#x16B3;','&#x16B7;','&#x16B9;','&#x16BB;','&#x16BE;','&#x16C1;','&#x16C2;','&#x16C7;','&#x16C8;','&#x16C9;','&#x16CB;','&#x16CF;','&#x16D2;','&#x16D6;','&#x16D7;','&#x16DA;','&#x16DD;','&#x16DF;','&#x16DE;','&#x16AA;','&#x16AB;','&#x16A3;','&#x16E1;','&#x16E0;',"'"]
for word in words:
	for rune in word:
		if(counter == 28):
			counter = 0
			print("<br />")
		else:
			counter += 1
		print(unicode_runes[int(rune)])
	if(counter == 28):
		counter = 0
		print("<br />")
	else:
		counter += 1
	print(unicode_runes[0])
"""
