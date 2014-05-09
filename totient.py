"""
totient.py: Implemention of totient function
"""

def gcd(a,b):
	while b != 0:
		c = a % b
		a = b
		b = c
	return a

def phi(n):
	x = 0
	for i in range(1,n+1):
		if gcd(n,i) == 1:
			x += 1
	return x
