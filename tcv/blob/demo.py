#demonstracao .

import blob as bl
import cv2
import sys

#checking validity of arguments
if (len(sys.argv) != 2):
   print "ERROR: invalid arguments. You must pass the filename of an image"
   exit()

#loads image in grayscale
img = cv2.imread(sys.argv[1],0)

#error while reading image
if img is None:
   print "ERROR: file could not be opened!"
   exit()

#displaying image
cv2.namedWindow("img",cv2.WINDOW_AUTOSIZE)  
cv2.imshow("img",img)
cv2.waitKey(0)

#creating grid and finding objects
dirg = bl.grid(img,32)
cand = dirg.locate(img)

#converting datatype
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

#marking objects
for c in cand:
   c.mark(img)

#displaying image
cv2.imshow("img",img)
cv2.waitKey(0)



