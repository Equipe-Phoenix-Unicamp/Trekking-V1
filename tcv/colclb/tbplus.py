#graphical trackbar to help process of hsv color calibration.
#by erik perillo

import cv2
import sys

#color definitions
BACKGND_COL = (0,0,0)
BORDER_COL  = (255,0,0)
MIDDLE_COL  = (127,127,127)
MARKER_COL  = (0,255,0)
MARKER2_COL = (0,0,255)

class Tbplus:

   def __init__(self,rng,middle,init_val=None):
      #initial values
      self.rng     = rng
      self.mid     = middle
      self.bar_pos = ((0,0),(0,0))
      self.unit    = 1
      self.img     = None
      self.barbak  = None
      if init_val == None:
         self.val  = [middle,middle]
      else:
         self.val  = list(init_val)

   #draws the bar on an image
   def draw(self,img,pos=(0,0),height=32,width=0):  
      if width == 0:
         width = img.shape[1]

      #binding image to bar
      self.img = img
    
      #the relative unit
      self.unit = float(width-2)/float(self.rng[1]-self.rng[0])     

      #storing position
      self.bar_pos = (pos,(pos[0]+width,pos[1]+height))

      #drawing
      self.img[pos[1]:(pos[1]+height),pos[0]:(pos[0]+width)] = BACKGND_COL
      cv2.rectangle(self.img,(pos[0],pos[1]),(pos[0]+width-1,pos[1]+height),BORDER_COL,1)
      self.img[self.bar_pos[0][1]:self.bar_pos[1][1],self.bar_pos[0][0]+self.unit*(self.mid-self.rng[0])] = MARKER_COL

      #backuping:
      self.barbak = (self.img[self.bar_pos[0][1]:self.bar_pos[1][1],self.bar_pos[0][0]:self.bar_pos[1][0]].copy()) 
      #updating bar on image
      self.update()
 
   #updates both sides of bar in image and position
   def update(self):
      #erasing previous data
      self.img[self.bar_pos[0][1]:self.bar_pos[1][1],self.bar_pos[0][0]:self.bar_pos[1][0]] = self.barbak
      #writing new positions
      start = self.bar_pos[0][0] + self.unit*(self.val[0]-self.rng[0])
      end   = self.bar_pos[0][0] + self.unit*(self.val[1]-self.rng[0])
      self.img[self.bar_pos[0][1]:self.bar_pos[1][1],start:end] = MIDDLE_COL 
      #writing border
      self.img[self.bar_pos[0][1]:self.bar_pos[1][1],self.unit*((self.val[0]+self.val[1]-2*self.rng[0])/2)] = MARKER2_COL

   def verbal_repr(self):
      string = "left value: " + str(self.val[0]) + "\n"
      string += "right value: " + str(self.val[1]) + "\n"
      string += "central initial value: " + str(self.mid) + "\n"
      string += "range: " + str(self.rng) 
      return string

   def __repr__(self):
      return [self.val,self.rng,self.mid]

#class for representing group of bars and manipulating them
class TBPgroup:

   def __init__(self,tbs):
      self.tbars   = tbs
      self.tbaks   = []
      self.drawing = len(tbs)*[False]
      self.first   = True

   #forction for bars manipulation
   def callBack(self,event,x,y,flags,param):
      mouse_over = False

      if self.first:
         self.first = False

      for i in range(len(self.tbars)):
         tb = self.tbars[i]
         if (tb.bar_pos[0][0] < x < tb.bar_pos[1][0]) and (tb.bar_pos[0][1] <= y <= tb.bar_pos[1][1]):
            mouse_over = True
            break

      if mouse_over:
         if (event == cv2.EVENT_LBUTTONDOWN) or (self.drawing[i] and event == cv2.EVENT_MOUSEMOVE):
            self.drawing[i] = True
            val = int((float(x - tb.bar_pos[0][0])/float(tb.bar_pos[1][0] - tb.bar_pos[0][0]))*(tb.rng[1]-tb.rng[0])) + tb.rng[0]
            #assigning value to the correct side
            if val > (tb.val[0] + tb.val[1])/2:
               tb.val[1] = val
            else:
               tb.val[0] = val
            #drawing new bar
            tb.update()
               
         elif event == cv2.EVENT_LBUTTONUP:
           self.drawing[i] = False

   #initiates everything
   def wakeup(self,winname,img,draw=True,pos=(0,0),height=32,width=0):

      #drawing tbs
      if draw:
         for i in range(len(self.tbars)):
            self.tbars[i].draw(img,(pos[0],pos[1]+i*height),height,width)

      #calling mouse callback
      cv2.setMouseCallback(winname,self.callBack)
      

