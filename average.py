avg=0.0;
n=0;
a="0";
while True:
	a = raw_input("Enter a number:")	
	if a.isdigit() == False:
		break
	avg=avg+int(a)
	n=n+1
if n!=0:
	avg=avg/n
print "Non-Number Entered....\nTschuss!!\n"+"Average of "+str(n)+" numbers entered is: "+str(avg) 
