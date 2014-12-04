import time
import cv2
import sys

sys.path.insert(0,"../../grid")
sys.path.insert(0,"../../blob")

import grid
import blob as bl

#opening video file
cap = cv2.VideoCapture("/home/erik/videos/videoplayback.mp4")

#creating named fixed windows
cv2.namedWindow("video",cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("possessed",cv2.WINDOW_AUTOSIZE)

#lower and upper hsv values for thresholding the pigs in the video
lower = (26,74,3)
upper = (125,225,254)

#creating grid
ret, frame = cap.read()
dirg = grid.grid(frame)

#vector of times
timevec = []

while True:
	#start counting time
	benchInit = time.clock()

	#process frames 5 times
	for i in range(5):	
		#reading from video file
		ret, frame = cap.read()
		#checking if video is over
		if frame is None:
			break

		#equalizing histogram TODO: find another function
		#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		#h, s, v = cv2.split(hsv)
		#v = cv2.equalizeHist(v)
		#hsv = cv2.merge([h,s,v])
		#frame2 = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

		#converting to HSV and thresholding
		frame2 = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		frame2 = cv2.inRange(frame2,lower,upper)

		#finding ordered blobs
		blobs = bl.ordered(dirg.locate(frame2))
		#marking them in image
		for blob in blobs:
			blob.mark(frame2)
		#adding points to container
		dirg.add(blobs)

	#checking integrity of image
	if frame is None:
		break
	
	#finding x coordinate of definitive object	
	x = dirg.det()
	#marking a line on it
	frame2[:,x] = 255
	#refreshing container
	dirg.refresh()

	#appending time
	timevec.append(time.clock()-benchInit)

	#showing images
	cv2.imshow("video",frame)
	cv2.imshow("possessed",frame2)

	if cv2.waitKey(1) & 0xFF == 27:
		break

print "average processing time: ", float(sum(timevec))/len(timevec)

