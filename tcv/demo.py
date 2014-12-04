#demonstracao
import cv2
import sys

sys.path.insert(0,"blob")
sys.path.insert(0,"grid")

import blob as bl
import grid as gr

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
dirg = gr.grid(img,32)

for i in range(1):
   blobs = dirg.locate(img)

   for blob in blobs:
      print "pt, area: ",blob.pt,blob.area()
   
   blobs = bl.ordered(blobs)
   
   print " "
   for blob in blobs:
      print "pt, area: ",blob.pt,blob.area()

   for blob in blobs:
      blob.mark(img)

   #displaying image
   cv2.imshow("img",img)
   cv2.waitKey(0)

   dirg.add(blobs)

dirg.det(img)
#displaying image
cv2.imshow("img",img)
cv2.waitKey(0)


"""
cand = dirg.locate(img)

#converting datatype
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

#marking objects
for c in cand:
   c.mark(img)

#displaying image
cv2.imshow("img",img)
cv2.waitKey(0)

"""

