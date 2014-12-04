import cv2
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-F", "--fps",help="Change FPS", type=int,default=60)
parser.add_argument("-W", "--width", help="Change WIDTH", type=int,default=640)
parser.add_argument("-H", "--height", help="Change HEIGHT", type=int,default=480)
args = parser.parse_args(sys.argv[1:])

fps = args.fps
width = args.width
height = args.height
print args
print fps
print width
print height

cv2.namedWindow("Beats")

cap = cv2.VideoCapture(1)

cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,width)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,height)
cap.set(cv2.cv.CV_CAP_PROP_FPS,fps)

while True:
	t, frame = cap.read()
	cv2.imshow("Beats",frame)
	if cv2.waitKey(1) & 0XFF == 27:
		break
