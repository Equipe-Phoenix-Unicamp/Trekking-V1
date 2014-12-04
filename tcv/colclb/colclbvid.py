import cv2
import sys
import tbplus as tb
import numpy as np

#setting initial hsv values
hue_min = 32
hue_max = 96
sat_min = 64
sat_max = 192
val_min = 64
val_max = 192

#creating trackbars for hsv
cv2.namedWindow("trackbar",cv2.WINDOW_AUTOSIZE)
trackbar = np.zeros((100,640,3))
hue = tb.Tbplus((0,127),64,(hue_min,hue_max))
sat = tb.Tbplus((0,255),128,(sat_min,sat_max))
val = tb.Tbplus((0,255),128,(val_min,val_max))

#creating group and calling callback
hsv = tb.TBPgroup([hue,sat,val])
hsv.wakeup("trackbar",trackbar)

#creating window for original image
cv2.namedWindow("original image",cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(1)

while(1):
   #updating values
   hue_min,hue_max = hue.val
   sat_min,sat_max = sat.val
   val_min,val_max = val.val
   #treshold
   ret,img = cap.read()
   bin_img = cv2.inRange(img,(hue_min,sat_min,val_min),(hue_max,sat_max,val_max))
   cv2.imshow("img",bin_img)
   cv2.imshow("trackbar",trackbar)
   cv2.imshow("original image",img)

   if cv2.waitKey(30) & 0xFF == 27:
      break

print "Final HSV values: ", hue.val, sat.val, val.val

