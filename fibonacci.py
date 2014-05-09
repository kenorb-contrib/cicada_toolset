"""
fibonacci.py: Fibonacci module
"""

def fibonacci(length,start):
	num_array = [0,1]
	for i in range(2,length+start+2):
		num_array.append(num_array[i-1]+num_array[i-2])
	return num_array[start:length+start]
	
def fibonacci_mod29(length,start):
	num_array = [0,1]
	for i in range(2,length+start+2):
		num_array.append( (num_array[i-1]+num_array[i-2]) % 29)
	return num_array[start:length+start]
