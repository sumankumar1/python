listoflists=[]
row=int(input("Enter #rows:"))
col=int(input("Enter #cols:"))
print "Enter Elements of your Matrix:" 
for i in range(0,row):
	list=[]
	for j in range(0,col):
		list.append(int(input("("+str(i)+","+str(j)+"):")))
	listoflists.append(list)
print listoflists
	