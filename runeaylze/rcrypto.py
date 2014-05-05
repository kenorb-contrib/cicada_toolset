"""
crypto.py: Python module for rune-text analyzing
"""
RuneNumbers = { "f":0,"u":1,"th":2,"o":3,"r":4,
	"c":5,"k":5,"c/k":5,"g":6,"w":7,"h":8,
	"n":9,"i":10,"j":11,"eo":12,"p":13,"x":14,
	"s":15,"z":15,"s/z":15,"t":16,"b":17,"e":18,
	"m":19,"l":20,"ng":21,"ing":21,"(i)ng":21,"ng/ing":21,
	"oe":22,"d":23,"a":24,"ae":25,"y":26,"ia":27,
	"io":27,"ia/io":27,"ea":28 }

RuneNumbersReversed = { "f":28,"u":27,"th":26,"o":25,"r":24,
	"c":23,"k":23,"c/k":23,"g":22,"w":21,"h":20,
	"n":19,"i":18,"j":17,"eo":16,"p":15,"x":14,
	"s":13,"z":13,"s/z":13,"t":12,"b":11,"e":10,
	"m":9,"l":8,"ng":7,"ing":7,"(i)ng":7,"ng/ing":7,
	"oe":6,"d":5,"a":4,"ae":3,"y":2,"ia":1,
	"io":1,"ia/io":1,"ea":0 }

Gematria = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,
	53,59,61,67,71,73,79,83,89,97,101,103,107,109]

DotUnicode = '&#x00B7;'

RunesUnicode = ['&#x16A0;','&#x16A2;','&#x16A6;','&#x16A9;','&#x16B1;',
	'&#x16B3;','&#x16B7;','&#x16B9;','&#x16BB;','&#x16BE;','&#x16C1;',
	'&#x16C2;','&#x16C7;','&#x16C8;','&#x16C9;','&#x16CB;','&#x16CF;',
	'&#x16D2;','&#x16D6;','&#x16D7;','&#x16DA;','&#x16DD;','&#x16DF;',
	'&#x16DE;','&#x16AA;','&#x16AB;','&#x16A3;','&#x16E1;','&#x16E0;']

RunesASCII = ["F","U","TH","O","R","C","G","W","H","N","I","J","EO","P",
	"X","S","T","B","E","M","L","NG","OE","D","A","AE","Y","IO","EA"]

class RuneText(object):
	"""
	Rune-text object with crypto-methods
	"""
	def __init__(self,filename='none'):
		# Define class variables
		self.words = []
		self.now = 0 # Number of Words
		self.nor = 0 # Number of Runes
		self.distribution = [] # Distribution of Runes
		self.ioc = 0.0 		# Index of Coincidence
		self.friedman = 0	# Friedman key length
		
		# Check if filename was given
		if filename != 'none':
			self.readFile(filename)
			self.update()
	def readFile(self,filename):
		"""
		Read a machine-readable rune file
		"""
		f = open(filename)
		lines = f.readlines()
		f.close()
		
		# Parse lines
		for line in lines:
			self.parseLine(line)
		
		# Convert characters to numbers
		self.convertCharsToNums()
	def update(self):
		"""
		Update analysis values
		"""
		
		# Get number of words and runes
		self.numWords()
		self.numRunes()

		# Calculate distribution of runes
		self.calculateDistribution()
		
		# Calculate Index of Coincidence
		self.calculateIOC()
		
		# Do Friedman test
		self.calculateFriedman()
	def isNumeric(self,s):
		"""
		Check if the passed string is numeric
		"""
		try:
			float(s)
			return True
		except ValueError:
			return False
	def numWords(self):
		"""
		Return number of words
		"""
		self.now = len(self.words)
	def numRunes(self):
		"""
		Return number of runes
		"""
		count = 0
		for word in self.words:
			for rune in word:
				if rune >= 0 and rune < 29:
					count += 1
		self.nor = count
	def parseLine(self,line):
		"""
		Parse a line from an input file
		"""
		line = line.replace("\n","")
		words_string = line.split('.')
		word_array = []
		for word in words_string:
			word_array.append(word.split('-'))
		self.words.extend(word_array)
	def convertCharsToNums(self):
		"""
		Converts data from a read file to numbers
		"""
		if not self.isNumeric(self.words[0][0]):
			word_array = []
			for word in self.words:
				rune_array = []
				for rune in word:
					if rune in RuneNumbers:
						rune_array.append(RuneNumbers[rune])
					else:
						rune_array.append(-1)
				word_array.append(rune_array)
			self.words = word_array
		else:
			word_array = []
			for word in self.words:
				rune_array = []
				for rune in word:
					if self.isNumeric(rune):
						rune_array.append(int(rune))
					else:
						rune_array.append(-1)
				word_array.append(rune_array)
			self.words = word_array
	def calculateDistribution(self):
		"""
		Calculate rune distribution of text
		"""
		count_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		percentage = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
		for word in self.words:
			for rune in word:
				if rune >= 0 and rune < 29:
					count_array[rune] += 1
		for i in range(0,29):
			percentage[i] = (count_array[i] / self.nor) * 100.0
		distribution_array = []
		distribution_array.append(count_array)
		distribution_array.append(percentage)
		self.distribution = distribution_array
	def calculateIOC(self):
		"""
		Calculate the Index of Coincidence
		"""
		count_sum = 0
		for count in self.distribution[0]:
			count_sum += count*(count-1)
		self.ioc = count_sum/(self.nor*(self.nor-1))
	def calculateFriedman(self):
		"""
		Do the Friedman test 
		"""
		A = 1.0/29.0
		B = 0.06141
		self.friedman = int(round(self.nor*(B-A) 
			/ (self.ioc*(self.nor-1)+B-self.nor*A),0))
	def calculateKasiski(self):
		"""
		Do the Kasiski test
		"""
		pass
	def nGrams(self,n,min_appearances,respect_words=False):
		"""
		Calculate n-grams
		"""
		position = 0
		if not respect_words:
			# Put all runes into one array
			rune_array = []
			for word in self.words:
				for rune in word:
					if rune >= 0 and rune < 29:
						rune_array.append(rune)

			# Loop over runes 
			ngram = { }
			for i in range(0,len(rune_array)-(n-1)):
				ngram_word = ""
				for j in range(0,n):
					ngram_word += str(rune_array[i+j])
					if j != (n-1):
						ngram_word += "-"
				# Check if entry exists
				if ngram_word in ngram:
					ngram[ngram_word][0] += 1
					ngram[ngram_word][1].append(position)
				else:
					add_ngram = { ngram_word: [1,[position]] }
					ngram.update(add_ngram)
				position += 1
		else:
			# Put all runes into one array
			rune_array = []
			for word in self.words:
				if len(word) >= n:
					word_array = []
					for rune in word:
						if rune >= 0 and rune < 29:
							word_array.append(rune)
					rune_array.append(word_array)

			# Loop over runes 
			ngram = { }
			for word in rune_array:
				for i in range(0,len(word)-(n-1)):
					ngram_word = ""
					for j in range(0,n):
						ngram_word += str(word[i+j])
						if j != (n-1):
							ngram_word += "-"
					# Check if entry exists
					if ngram_word in ngram:
						ngram[ngram_word][0] += 1
						ngram[ngram_word][1].append(position)
					else:
						add_ngram = { ngram_word: [1,[position]] }
						ngram.update(add_ngram)
					position += 1
						
		# Sort out sequences that appear not often enough
		keyarray = []
		for key in ngram:
			if ngram[key][0] < min_appearances:
				keyarray.append(key)
		for key in keyarray:
			del ngram[key]
		
		# Sort dictionary descending
		return sorted(sorted(ngram.items()),reverse=True,key=lambda x: x[1][0])
	def wordLengths(self):
		"""
		Returns a listing of word length statistics
		"""
		wordlengths = {}
		for word in self.words:
			if len(word) in wordlengths:
				wordlengths[len(word)] += 1
			else:
				w = { len(word):1 }
				wordlengths.update(w)
		return sorted(wordlengths.items())
	def runesASCII(self):
		"""
		Returns the text in ASCII representation
		"""
		text = ""
		count = 0
		for word in self.words:
			for rune in word:
				text += RunesASCII[rune]
			if count > 10:
				count = 0
				text += "\n"
			else:
				count += 1
				text += " "
		return text
	def vigenereTry(self,keyword,offset=0,max_displayed_chars=10):
		"""
		Tries a vigenere key and displays results
		"""
		
		# Convert key representation
		num_key = []
		num_reverse = []
		key_split = keyword.split("-")
		for key in key_split:
			if not self.isNumeric(key):
				if key in RuneNumbers:
					num_key.append(RuneNumbers[key])
					num_reverse.append(RuneNumbersReversed[key])
			else:
				if self.isNumeric(key):
					num_key.append(int(key))
					num_reverse.append(28-int(key))
		
		key_counter = 0
		rune_counter = 0
		text1 = ""
		text2 = ""
		text3 = ""
		text4 = ""
		# Loop through words
		for word in self.words:
			for rune in word:
				# Check if rune counter reached max
				if(rune_counter < (max_displayed_chars -1)):
					rune_counter += 1
				else:
					break
				text1 += RunesASCII[self.vigenereDecrypt(rune,num_key[key_counter])]
				text2 += RunesASCII[self.vigenereDecrypt(num_key[key_counter],rune)]
				text3 += RunesASCII[self.vigenereDecrypt(rune,num_reverse[key_counter])]
				text4 += RunesASCII[self.vigenereDecrypt(num_reverse[key_counter],rune)]
				# Increment key counter
				if(key_counter < (len(num_key) - 1)):
					key_counter += 1
				else:
					key_counter = 0
			text1 += " "
			text2 += " "
			text3 += " "
			text4 += " "
		
		# Print results
		print("Variation 1: "+text1)
		print("Variation 2: "+text2)
		print("Variation 3: "+text3)
		print("Variation 4: "+text4)
		
	def vigenereDecrypt(self,cipher,key):
		"""
		Decipheres a cipher and key rune ID
		"""
		return (cipher-key) % 29
