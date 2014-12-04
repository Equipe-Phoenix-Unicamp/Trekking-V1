import cv2
from random import randint

def bestdiv(side,sdiv=64,perc=0.1):
   margin = int(sdiv*0.1*perc)
   bestdiv = sdiv
   i = sdiv - 1
   while(sdiv-i <= margin and i > 0):
      if(side%i < side%bestdiv):
         bestdiv = i
      i -= 1
   i = sdiv + 1
   while(i-sdiv <= margin):
      if(side%i < side%bestdiv):
         bestdiv = i
      i += 1
   return bestdiv

#class for representing continuous images   
class blob:

   #calculates central point of object
   def setPoint(self):
      self.pt = ( (int((self.rng_x[0] + self.rng_x[1]) / 2)), (int((self.rng_y[0] + self.rng_y[1]) / 2 )) )

   #updates object's size
   def update(self,posit,value):
      if posit == (0,0):
         self.rng_x = (value,self.rng_x[1])
      elif posit == (0,1):
         self.rng_x = (self.rng_x[0],value)
      elif posit == (1,0):
         self.rng_y = (value,self.rng_y[1])
      elif posit == (1,1):
         self.rng_y = (self.rng_y[0],value)
      elif posit == 0:
         self.rng_x = value
      elif posit == 1:
         self.rng_y = value
      self.setPoint()   

   #mark itself on an image
   def mark(self,mat):
      randcolor = (randint(0,255),randint(0,255),randint(0,255))
      cv2.rectangle(mat,(self.rng_x[0],self.rng_y[0]),(self.rng_x[1],self.rng_y[1]),randcolor,1)
      cv2.circle(mat,self.pt,3,randcolor,-1)

   #traces itself on image
   def trace(self,mat,color=(0,0,255)):
      i = 0
      div = (self.rng_y[1]-self.rng_y[0])/len(self.lines)
      for line in self.lines:
         y = self.rng_y[0] + i*div
         for l in line:
            mat[y:(y+1),l[0]:l[1]] = color 
         i += 1 
   
   #TODO: remake this useless shit
   def markContour(self,mat,color=(255,0,0)):
      secs = (self.rng_y[1]-self.rng_y[0])/len(self.lines)
      y = self.rng_y[0]
      #for lain in self.lines[0]:
        # cv2.line(mat,(lain[0],y),(lain[1],y),color)
      for i in range(len(self.lines)-1):
         a = self.lines[i]
         b = self.lines[i+1]
         if(len(b) > len(a)):
            for k in range(len(b)):
               cv2.line(mat,(b[k][0],y+secs),(b[k][0],y),color)        
               cv2.line(mat,(b[k][1],y+secs),(b[k][1],y),color) 
               if(k < len(b)-1):       
                  cv2.line(mat,(b[k][1],y),(b[k+1][0],y),color)
         elif(len(b) < len(a)):
            for k in range(len(a)):
               cv2.line(mat,(a[k][0],y),(a[k][0],y+secs),color)        
               cv2.line(mat,(a[k][1],y),(a[k][1],y+secs),color) 
               if(k < len(a)-1):       
                  cv2.line(mat,(a[k][1],y+secs),(a[k+1][0],y+secs),color)
         else:
            for k in range(len(a)):
               cv2.line(mat,(a[k][0],y),(b[k][0],y+secs),color)        
               cv2.line(mat,(a[k][1],y),(b[k][1],y+secs),color)
         y += secs 
      for lain in self.lines[len(self.lines)-1]:
         cv2.line(mat,(lain[0],y),(lain[1],y),color)
            
   #returns area of square around object
   def area(self):
      return (self.rng_x[1] - self.rng_x[0])*(self.rng_y[1] - self.rng_y[0])

   def __init__(self,rng_x=(0,0),rng_y=(0,0)):
      self.rng_x = rng_x
      self.rng_y = rng_y
      self.lines = []
      self.setPoint()

   def __repr__(self):
      string = str(self.rng_x) + " , " + str(self.rng_y)
      return string

# SIM, EH BUBBLESORT MESMO, O PIOR ALGORITMO DE ORDENACAO DE TODOS
# CHORA JUCELIO
def ordered(blobs,bigger_first=True):
	if bigger_first:
		return (sorted(blobs, key=lambda blob: blob.area()))[::-1]
	return sorted(blobs, key=lambda blob: blob.area())


#BORON DINES
