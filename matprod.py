def main():
	row1=4
	col1=4 #=row2
	col2=4
	mat1=[[1 for x in range(col1)] for y in range(row1)]
	mat2=[[2 for x in range(col2)] for y in range(col1)]
	res=matprod(row1,col1,col2,mat1,mat2,"F")
	print "Full Mode Matrix Product:"
	print res
	for i in range(0,col1):
		for j in range (0,i):
			mat2[i][j]=0;
	res=matprod(row1,col1,col2,mat1,mat2,"U")
	print "Upper Traingular Mode Matrix Product:"
	print res
	
def matprod(row1,col1,col2,mat1,mat2,mode):
	res=[[0 for x in range(col2)] for y in range(row1)]
	if mode == "F":
		for i in range(0,row1):
			for j in range(0,col2):
				for k in range(0,col1):
					res[i][j]=res[i][j]+mat1[i][k]*mat2[k][j]
		return res
	elif mode == "U":
		for i in range(0,row1):
			for j in range(0,col2):
				for k in range(i,col1):
					res[i][j]=res[i][j]+mat1[i][k]*mat2[k][j]
		return res
	else:
		print "Error:Unrecognized Mode Requested"

		
main()