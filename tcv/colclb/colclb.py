import cv2
import sys
import tbplus as tb
import numpy as np

#global vars
ix,iy = 0,0
rect  = ((0,0),(0,0))
drawing = False

def draw_square(event,x,y,flags,param):
   global img,copy,ix,iy,rect,drawing,color
   
   if event == cv2.EVENT_LBUTTONDOWN:
      drawing = True
      ix,iy = x,y

   elif event == cv2.EVENT_MOUSEMOVE:
      if drawing == True:
         img = copy.copy()
         cv2.rectangle(img,(ix,iy),(x,y),(0,0,255),1)
         rect = ((ix,iy),(x,y))

   elif event == cv2.EVENT_LBUTTONUP:
      drawing = False

def median_pixl(img):
   summ = [int(img[:,:,i].sum()/(img.shape[0]*img.shape[1])) for i in range(img.shape[2])]
   return summ

#checking validity of arguments
if (len(sys.argv) != 2):
   print "ERROR: invalid arguments. You must pass the filename of an image"
   exit()

#loads image in grayscale
img = cv2.imread(sys.argv[1])

#error while reading image
if img is None:
   print "ERROR: file could not be opened!"
   exit()

#cloning
copy = img.copy()

#creating window
cv2.namedWindow("img",cv2.WINDOW_AUTOSIZE)  
#mouse function
cv2.setMouseCallback("img",draw_square)
#loop
while(1):
   cv2.imshow("img",img)
   if cv2.waitKey(30) & 0xFF == 27:
      break

#remove the square:
img = copy.copy()

#reorganizing rect for its area to be always positive
if rect[1][0] < rect[0][0]:
   rect = ((rect[1][0],iy),(ix,rect[1][1]))
if rect[1][1] < rect[0][1]:
   rect = ((rect[0][0],rect[1][1]),(rect[1][0],iy))

#defining selected square and converting to hsv
partial = cv2.cvtColor(img[(rect[0][1]+1):rect[1][1],(rect[0][0]+1):rect[1][0]],cv2.COLOR_BGR2HSV)

#calculating median
median = median_pixl(partial)
print "median hsv intensities : ",median

#showing median color in image
img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
img[(rect[0][1]+1):rect[1][1],(rect[0][0]+1):rect[1][0]] = median
img = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
cv2.imshow("img",img)
cv2.waitKey(0)
img = copy.copy()

#setting initial hsv values
hue_min = median[0] - 10
hue_max = median[0] + 10
sat_min = median[1] - 20
sat_max = median[1] + 20
val_min = median[2] - 25
val_max = median[2] + 25

#creating trackbars for hsv
cv2.namedWindow("trackbar",cv2.WINDOW_AUTOSIZE)
trackbar = np.zeros((100,640,3))
hue = tb.Tbplus((0,127),median[0],(hue_min,hue_max))
sat = tb.Tbplus((0,255),median[1],(sat_min,sat_max))
val = tb.Tbplus((0,255),median[2],(val_min,val_max))

#creating group and calling callback
hsv = tb.TBPgroup([hue,sat,val])
hsv.wakeup("trackbar",trackbar)

#creating window for original image
cv2.namedWindow("original image",cv2.WINDOW_AUTOSIZE)

while(1):
   #updating values
   hue_min,hue_max = hue.val
   sat_min,sat_max = sat.val
   val_min,val_max = val.val
   #treshold
   bin_img = cv2.inRange(img,(hue_min,sat_min,val_min),(hue_max,sat_max,val_max))
   cv2.imshow("img",bin_img)
   cv2.imshow("trackbar",trackbar)
   cv2.imshow("original image",copy)

   if cv2.waitKey(30) & 0xFF == 27:
      break

print "Final HSV values: ", hue.val, sat.val, val.val

