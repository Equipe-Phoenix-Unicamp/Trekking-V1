import cv2
import sys
import container
sys.path.insert(0,"../blob")
import blob as bl

from random import randint

def bestdiv(side,sdiv=64):
   margin = int(sdiv*0.1)
   #print "DEBUG: margin = " , margin #debug
   bestdiv = sdiv
   i = sdiv - 1
   while(sdiv-i <= margin and i > 0):
      #print "i = %d, bestdiv = %d, side-/-i = %d, side-/-bestdiv = %d" % (i,bestdiv,side%i,side%bestdiv) #debug
      if(side%i < side%bestdiv):
         bestdiv = i
      i -= 1
   i = sdiv + 1
   while(i-sdiv <= margin):
      #print "i = %d, bestdiv = %d, side-/-i = %d, side-/-bestdiv = %d" % (i,bestdiv,side%i,side%bestdiv) #debug
      if(side%i < side%bestdiv):
         bestdiv = i
      i += 1
   return bestdiv

#class used in function "locate"
class line:
   def __init__(self,rng=(-1,-1),index=-1):
      self.rng = rng
      self.index = index

   #updates line's data
   def update(self,posit,value):
      if posit == 0:
         self.rng = value
      elif posit == 1:
         self.index = value

   def __repr__(self):
      string = str(self.rng) + ", " + str(self.idate)
      return string

class grid(container.Container):
   #finds the best possible division for image
   def __init__(self,mat,sdiv=64):
      container.Container.__init__(self)

      if(mat.shape[0]/sdiv < 3):
         sdiv = int(mat.shape[0]/3)

      self.divy = bestdiv(mat.shape[0],sdiv)
      self.secs = int(mat.shape[0]/self.divy) 
  
      i = 0
      while(mat.shape[1] - (i+1)*self.secs >= 0): 
         i += 1

      self.divx = i
      self.maxwp = int(0.25*self.secs*self.secs)

   def mark(self,mat,color=255):
      for i in range(self.divx):
         mat[0:mat.shape[0],i*self.secs:(i*self.secs+1)] = color
      for i in range(self.divy):
         mat[i*self.secs:(i*self.secs+1),0:mat.shape[1]] = color

   def det(self,img=None,n_its=4):
      side = self.divx*self.secs
      shift = 0

      for i in range(n_its):
         right = left = 0
         if img is not None:
            img[0:img.shape[0],shift+side/2] = 255
         
         for obj in self.objs:
            if obj[0][0] > shift + side/2:
               right += obj[1]
            else:
               left  += obj[1]

         if right > left:
            for obj in self.objs:
               if obj[0][0] < shift + side/2:
                  self.objs.remove(obj)
            shift += side/2
         else:
            for obj in self.objs:
               if obj[0][0] > shift + side/2:
                  self.objs.remove(obj)

         side /= 2

      return shift + side/2
   
   #finds objects in binary image
   def locate(self,mat):
      ncands = nlines = npastlines = 0
      found = False
      enil = []
      pastenil = []
      cand = []
      defcand = []
      for i in range(self.divy):
         y = i*self.secs
         for j in range(self.divx):
            #prov = []
            x = j*self.secs
            if(cv2.countNonZero(mat[y:(y+self.secs),x:(x+self.secs)]) >= self.maxwp):
               if not found:
                  ini = x
                  found = True
            elif found:
               found = False
               enil.append(line((ini,x)))
               #prov.append((ini,x))
               nlines += 1
         if found:
            found = False
            enil.append(line((ini,x+self.secs)))
            #prov.append((ini,x+self.secs))
            nlines += 1

         for l in enil:
            found = False
            for pl in pastenil:
               a = cand[l.index]
               b = cand[pl.index]

               if not((pl.rng[0] >= l.rng[1]) or (pl.rng[1] <= l.rng[0])):
                  #print "kkk"
                  if not found:
                     #print "not found"
                     if(l.rng[0] < b.rng_x[0]):   
                        b.update((0,0),l.rng[0]) 
                     if(l.rng[1] > b.rng_x[1]):   
                        b.update((0,1),l.rng[1]) 
                     l.index = pl.index
                     found = True
                     if(b.rng_y[0]+len(b.lines)*self.secs == y):
                        #print "oloco"
                        b.lines[len(b.lines)-1].append(l.rng)
                     else:
                        b.lines.append([])
                        b.lines[len(b.lines)-1].append(l.rng)
                  elif(a is not b):
                     #print "uepa"
                     diff = (b.rng_y[0] - a.rng_y[0])/self.secs
                     if (diff > 0):
                     #b is lower than a
                        #print ">"
                        for k in range(len(b.lines)):
                           a.lines[k+diff] += b.lines[k]
                     elif (diff < 0):
                     #b is higher than a
                        #print "<"
                        diff = -diff
                        #print diff, len(a.lines), len(b.lines)
                        for k in range(len(a.lines)-1):
                           a.lines[k] += b.lines[k+diff]
                        a.lines = b.lines[0:diff] + a.lines
                     else:
                        #print "=="
                        #print len(a.lines), len(b.lines)
                        #print b.rng_y[0], a.rng_y[0]
                        for k in range(len(b.lines)):
                           a.lines[k] += b.lines[k]

                     if(b.rng_x[0] < a.rng_x[0]):
                        a.update((0,0),b.rng_x[0])
                     if(b.rng_x[1] > a.rng_x[1]):
                        a.update((0,1),b.rng_x[1])
                     if(b.rng_y[0] < a.rng_y[0]):
                        a.update((1,0),b.rng_y[0])

                     for m in range(npastlines):
                        if(cand[pastenil[m].index] is b):
                           pastenil[m].index = l.index
                     b.update(0,(-1,-1))
            if not found:
               cand.append(bl.blob(l.rng,(y,-1)))
               #print "CRIOU", y
               l.index = ncands
               cand[ncands].lines.append([])
               cand[ncands].lines[0].append(l.rng)
               ncands += 1
                           
            cand[l.index].update((1,1),y+self.secs)

         pastenil = enil
         enil = []
         npastlines = nlines
         nlines = 0
         found = False

      for a in cand:
         if (a.rng_x != (-1,-1)):
            defcand.append(a)

      return defcand

