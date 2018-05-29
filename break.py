import random

secret = random.randint(1,5)
guess =0
while guess!=secret:
	guess = int(input('guess between 1 and 20:'))
	if guess ==0:
		print('The game is terminated')
		break
else:
	print('you have found it')