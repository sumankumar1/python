import random

secret = random.randint(1,20)
guess = -1
while guess !=secret:
	guess = int(input('guess a number between 1 and 20:'))
print('you have found it')