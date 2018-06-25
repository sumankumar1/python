import sys
import re

class RealtyObject:
	def __init__(self,id,price,location,area_liv,num_of_rooms,agent):
		self.id=id
		try:
			self.price=int(price)
		except:
			self.price=0
		self.location=location
		try:
			self.area_liv=float(area_liv)
		except:
			self.area_liv=0.0
		try:
			self.num_of_rooms=int(num_of_rooms)
		except:
			self.num_of_rooms=0
		self.agent=agent
	def change_price(self,price=0):
		self.price=price
	def print(self):
		print("Id:{}, Price:{}, location:{}, area_liv:{}, num_of_rooms:{}, agent:{}".format(self.id,self.price,self.location,self.area_liv,self.num_of_rooms,self.agent))

class Apartment(RealtyObject):
	def __init__(self,id,price,location,area_liv,num_of_rooms,agent,floor):
		RealtyObject.__init__(self,id,price,location,area_liv,num_of_rooms,agent)
		self.floor=int(floor)
	def print(self):
		RealtyObject.print(self)
		print("floor:{}".format(self.floor))
		
class House(RealtyObject):
	def __init__(self,id,price,location,area_liv,num_of_rooms,agent,plotarea):
		RealtyObject.__init__(self,id,price,location,area_liv,num_of_rooms,agent)
		self.plotarea=plotarea
	def print(self):
		RealtyObject.print(self)
		print("plotarea:",self.plotarea)

class Request:
	matching_objects=[]
	possible_objects=[]
	possible_locs=()
	def __init__(self,max_price=0,min_area=0.0,min_rooms=0):
		self.max_price=max_price;
		self.min_area=min_area;
		self.min_rooms=min_rooms;
	def check_match(self,r):
		flag=False
		#if self.max_price>=r.price and r.location in self.possible_locs and self.min_area<=r.area_liv and self.min_rooms<=r.num_of_rooms:
		#	flag=True
		l=[self.max_price>=r.price , r.location in self.possible_locs , self.min_area<=r.area_liv , self.min_rooms<=r.num_of_rooms].count(True)
		if l==4:
			flag=True
		dict ={"price":r.price==0,"location":r.location=="","area_liv":r.area_liv==0, "num_of_rooms":r.num_of_rooms==0}
		res = [key for key, value in dict.items() if value==True]
		if len(res)>0 and l>=4-len(res):
			print(len(res),l,res)
			raise Exception ("Following fields have default values or error:",res)
		return flag
		
	def find_matches(self,l):
		for r in l:
			try:
				flag=self.check_match(r)
				if flag==True:
					self.matching_objects.append(r)
			except Exception as e:
				self.possible_objects.append(r)
				#print(e)
				
class Request_apartment(Request):
		possible_locs=()
		def __init__(self,max_price=0,min_area=0.0,min_rooms=0,floor_min=0,floor_max=0):
			Request.__init__(self,max_price,min_area,min_rooms)
			#Request.possible_locs=possible_locs
			self.floor_min=floor_min
			self.floor_max=floor_max
		def check_match(self,r):
			try:
				flag=False
				if (self.floor_min<=r.floor<=self.floor_max):
					flag=True
					#print(flag)
				if flag==True:
					flag=Request.check_match(self,r)
				#print (flag)
				return flag
			except Exception as e:
				#print(e)
				raise
				#raise
				
class Request_house(Request):
		possible_locs=()
		def __init__(self,max_price=0,min_area=0.0,min_rooms=0,plotarea_min=0.0):
			Request.__init__(self,max_price,min_area,min_rooms)
			#Request.possible_locs=possible_locs
			self.plotarea_min=float(plotarea_min)
		def check_match(self,r):
			try:
				flag=True
				if (r.plotarea<self.plotarea_min):
					flag=False
				if flag==True:
					flag=Request.check_match(self,r)
				return flag
			except:
				#pass
				raise
				
def main():
	alist=[]#Apartment list
	hlist=[]#House list
	check_apartment=[]
	check_house=[]
	try:
		a= open(sys.argv[1],"r")
		content = a.read().split()
		a.close()
	except IOError:
		exit('File'+sys.argv[1]+'could not be opened')
	
	i=0
	while(i<len(content)):
		a=Apartment(content[i],content[i+1],content[i+2],content[i+3],content[i+4],content[i+5],content[i+6])
		i=i+7
		alist.append(a)
		
	try:
		a= open(sys.argv[2],"r")
		content = a.read().split()
		a.close()
	except IOError:
		exit('File'+sys.argv[2]+'could not be opened')
	
	i=0
	while(i<len(content)):
		a=House(content[i],content[i+1],content[i+2],content[i+3],content[i+4],content[i+5],content[i+6])
		i=i+7
		hlist.append(a)

	try:
		a= open(sys.argv[3],"r")
		content = a.read().split()
		a.close()
	except IOError:
		exit('File'+sys.argv[3]+'could not be opened')
	
	i=0
	while(i<len(content)):
		a=Request_apartment()
		a.max_price=int(content[i])
		i=i+1
		while re.match('\d+\d$',content[i])==None and re.match('\d+\.\d+$',content[i])==None:
			a.possible_locs=a.possible_locs+(content[i],)
			i=i+1
		a.min_area=float(content[i])
		i=i+1
		a.min_rooms=int(content[i])
		i=i+1
		a.floor_min=int(content[i])
		i=i+1
		a.floor_max=int(content[i])
		i=i+1
		check_apartment.append(a)
		
		
	try:
		a= open(sys.argv[4],"r")
		content = a.read().split()
		a.close()
	except IOError:
		exit('File'+sys.argv[4]+'could not be opened')
		
	i=0
	while(i<len(content)):
		a=Request_house()
		a.max_price=int(content[i])
		i=i+1
		while re.match('\d+\d$',content[i])==None and re.match('\d+\.\d+$',content[i])==None:
			a.possible_locs=a.possible_locs+(content[i],)
			i=i+1
		a.min_area=float(content[i])
		i=i+1
		a.min_rooms=int(content[i])
		i=i+1
		a.plotarea_min=(content[i])
		i=i+1
		check_house.append(a)
		
	print("ENQUIRY FOR APARTMENTS:")
	for r in check_apartment:
		#print("start",len(r.matching_objects))
		r.matching_objects=[]
		r.possible_objects=[]
		r.find_matches(alist)
		#print(len(r.matching_objects))
		#print(len(r.possible_objects))
		print("Enquiry For:",r.max_price,r.possible_locs,r.min_area,r.min_rooms,r.floor_min,r.floor_max)
		print("Total Match Found:",len(r.matching_objects))
		print("Another possible matches",len(r.possible_objects))
		for x in r.matching_objects:
			x.print()
		print('\n')
	
	print("ENQUIRY FOR HOUSE:")
	for r in check_house:
		r.matching_objects=[]
		r.possible_objects=[]
		r.find_matches(hlist)		
		#print(len(r.possible_objects))
		print("Enquiry For:",r.max_price,r.possible_locs,r.min_area,r.min_rooms,r.plotarea_min)
		print("Total Match Found:",len(r.matching_objects))
		print("Another possible matches:",len(r.possible_objects))
		for x in r.matching_objects:
			x.print()
		print('\n')
			
			
main()
			
			
			