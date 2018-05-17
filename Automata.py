import time
import matplotlib.pyplot as plot
#General Automata Program

def main():
	t1= time.time()
	time1=[]
	s='1'
	n=len(s)
	d=[] #main list for raw data
	temp=[] #temporary list for storing result after applying rule110
	for i in range(0,n):
		d.append(s[i])#insert data into main list
	d.append('0') #one zero on the right
	for i in range(0,10000): # insert n\2 zeros on the left
		d.insert(0,'0')
	n1=len(d)-1 
	temp=list(d)
	for j in range(1,(n1)):#n\2 iteration		
		'''for i in range(0,n1):#print d after completion of (j-1)th iteration
			if d[i]=='1':
				print '*',
			else:
				print ' ',
		print('')'''
		t3=time.time()
		for i in range(n1-j-1,n1):#apply rule on d and insert result in temp
			temp[i]=rule_110(d[i-1],d[i],d[i+1]) #apply any rule
		d=list(temp) #update d after completion of jth iteration
		t4=time.time()
		time1.append(t4-t3)
		#print t4-t3
	t2=time.time()
	t=t2-t1	
	print t2-t1
	x=1
	for t in time1:
		plot.plot(x,t,'ro')
		x=x+1
	plot.show()		

#Rule 110

def rule_110(a,b,c): #rule defination
	if (a== '1' and b== '1' and c== '1'):
		b= '0'
		return b
	if (a== '1' and b== '1' and c== '0'):
		b= '1'
		return b
	if (a== '0' and b== '1' and c== '1'):
		b= '1'
		return b
	if (a== '0' and b== '1' and c== '0'):
		b= '1'
		return b
	if (a== '0' and b== '0' and c== '0'):
		b= '0'
		return b
	if (a== '0' and b== '0' and c== '1'):
		b= '1'
		return b
 	if (a== '1' and b== '0' and c== '0'):
		b= '0'
		return b
	if (a== '1' and b== '0' and c== '1'):
		b= '1'
		return b

main() #call main

