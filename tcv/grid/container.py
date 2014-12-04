import sys
import cv2

sys.path.insert(0,"../blob/")

import blob as bl

class Container:
   
   def __init__(self):
      self.objs  = []
      self.n_its = 0
      self.const = 1.618034
      self.max   = 10

   def add(self,blist):
      self.n_its += 1
      for i in range(len(blist)):
         self.objs.append((blist[i].pt,self.max/(self.const**i)))

   def refresh(self):
      self.n_its = 0
      self.objs  = []

