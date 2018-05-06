import cv2
import imutils
import time
import numpy as py
import matplotlib.pyplot as plot


cap = cv2.VideoCapture('dunebuggy.avi')
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
width = cap.get(3) 
height = cap.get(4)
road=100#in centemer
width=0;
print fps,width,height
ret,current_frame=cap.read()
previous_frame=current_frame
count=[]
dist=[]
x=0
while(cap.isOpened()):
	if(ret):
		current_frame_gray=cv2.cvtColor(current_frame,cv2.COLOR_BGR2GRAY)
		previous_frame_gray=cv2.cvtColor(previous_frame,cv2.COLOR_BGR2GRAY)
		frame_diff=cv2.absdiff(current_frame_gray,previous_frame_gray)
		
		hsv = cv2.cvtColor(current_frame,cv2.COLOR_BGR2HSV)
		lower_red=py.array([100,100,100])
    		upper_red=py.array([255,255,255])
    		mask = cv2.inRange(hsv,lower_red,upper_red)
   	 	res = cv2.bitwise_and(current_frame,current_frame,mask=mask)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
		center = None
		if len(cnts) > 0:
			#a=0
			#a=a+1
			count.append(x)
			#print x
			c = max(cnts, key=cv2.contourArea)
			M = cv2.moments(c)
			z,y = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			dist.append(z)
 			print z,y
		cv2.imshow("Detect_obect_postion", mask)
		previous_frame=current_frame.copy()
		ret,current_frame=cap.read()
		x=x+1

	if cv2.waitKey(20) & 0xFF == ord('q'):
        	break
	
#print x
i=1
j=1
k=1
count1=[0]
dist1=[0]
vel=[0]
calibration=road/width;
while(i<len(count)):
	count1.append((count[i]-count[i-1])/fps)
	count1[i]=count1[i]+count1[i-1]
	i=i+1
#for c1 in count1:
#	print c1
print "pixel"
while(j<len(dist)):
	dist1.append(dist[j]-dist[j-1])
	j=j+1
for d1 in dist1:
	print d1
while(k<len(dist)):
	vel.append((dist1[k]*calibration)/(count1[k]-count1[k-1]))
	k=k+1
print "velocity"
for v in vel:
	print v
plot.plot(count1,vel,'-k',count1,dist,'-r')
plot.show()
cap.release()
cv2.destroyAllWindows()




