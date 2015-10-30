import math
import random as r
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

#This is not a proper neigherest neighbor algorithm with proper training data

class point:
    def __init__(self,x,y,value):
        self.position=[x,y]
        self.value=value
        self.label=None
        self.near=None
        
    def nearset(self, l):
        self.near=l
    
    def setlabel(self,lab):
        self.label=lab
        
    def pprint(self):
        return [self.position,self.value,self.label]
        
    def type(self):
        return "point"
    
            
    def labelnearest(self): #takes a list of neighbors, finds the mode label and assigns the point that label
        labellist=[None]*len(self.near)
        for i in range(0,len(self.near)):
            labellist[i]=self.near[i].label
        lset=list(set(labellist))
        labelcount=[None]*len(lset)
        top=0
        mode=None
        for i in range(0,len(lset)):
            labelcount[i]=[lset[i],labellist.count(lset[i])] #set makes an unorderedlist of unique elements
            if labelcount[i][1]>top:
                top=labelcount[i][1]
                mode=labelcount[i][0]
        #print labelcount
        self.label=mode
            
            
        
class enviornment:
    def __init__(self):
        self.pointlist=None
        
    def listset(self,l):
        self.pointlist=l
    
#    def enviosave(self):
#        p=self.pointlist
#        f=
#        for i in (0,len(p)):
            
        
    def nearest(self,point,k): #Gives a list of the nearest k points
        #Acts on a single point
        #On second though it might have been been to just calculate distance everytime you need it than deal with the addional list of distances
        nearlist=[[None,None]]*k
        p1=point.position
        for i in range(0,len(self.pointlist)): #Start Comparing to every point
            if self.pointlist[i].label!=None: #Makes it so that only label points are used as reference and keeps self from being used
                p2=self.pointlist[i].position
                d=math.sqrt(float((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))
                #print "The type of d is "+str(type(d))
                #First it fills nearlist
                if i<=(k-1): #taking advantage of the fact that near list has k entries to fill it up with the first k elements and then find closer ones
                    nearlist[i]=[self.pointlist[i],d]
                    if i==(k-1):
                        dlist=zip(*nearlist)[1] #list of distances for nearlist
                        imax=dlist.index(max(dlist))
                        #print "The initial dlist is "+str(dlist) #This only happens once
                #then is starts replacing nearlist with closer members        
                elif d < dlist[imax]:
                    #print "Closer Memeber Found"
                    nearlist[imax]=[self.pointlist[i],d]
                    dlist=zip(*nearlist)[1]
                    imax=dlist.index(max(dlist))
                #else:
                    #print str(self.pointlist[i].position)+" rejected because distance was "+str(d)+" and max was "+str(dlist[imax])
                    
        nearlist=zip(*nearlist)[0]
        point.nearset(nearlist)
        #print "The closest point to "+str(point.position)+" is "
        #for i in range(0,len(point.near)):
            #print str(point.near[i].position)+", which is "+str(point.near[i].label) 
            
        #THis should print out the initial dlist and then the eventual closes points after they have been found

    def creatlist(self,num,f): #Creates a randomly placed list with values preassigned
        l=[None]*num       # The values tell the correct label, which is based on wheather y<=x, which caues it to be red, or not which casues it to be blue. 
        for i in range(0,num):  #A random half of the points have already be labeled correctly
            x=r.random()-r.randint(0,1)
            y=r.random()-r.randint(0,1)
            if y<=f(x):
                val="red"
                #print str(x)+","+str(y)+" is red"  
            else:
                val="blue"
            l[i]=point(x,y,val) 
            if i<=num/2:
                l[i].setlabel(val)
            self.pointlist=l

    def pointgraph(self,gn,f): #gn is figure number and f is the actual function that seperates the points
        p=self.pointlist
        k=len(p)
        lred=[None]*k
        lblu=[None]*k
        lbla=[None]*k
        ired=0
        iblu=0
        ibla=0
        for i in range(0,len(p)):
            if p[i].label=="red":
                lred[ired]=p[i].position
                #print str(p[i].position)+" is red"
                #print p[i].position[1]<=p[i].position[0]
                ired+=1
            elif p[i].label=="blue":
                lblu[iblu]=p[i].position
                iblu+=1
            else:
                lbla[ibla]=p[i].position
                ibla+=1
        #for some reason I need to use * to get zip to work.  If I don't I have to imput the arguement for zip as two multiple arguements
        #maybe * causes the list to be parsed as a multiple arguement for zip to act on
        #remeber that ired, iblue, and ibla are all now the first None element
        l2red=[None]*(ired)
        for i in range(0,ired):
            l2red[i]=lred[i]
        #print "number red is "+str(ired)

        l2blu=[None]*(iblu)
        #print "number blue is "+str(iblu)

        for i in range(0,iblu):
            l2blu[i]=lblu[i]
        
        l2bla=[None]*(ibla)
        #print "number black is "+str(ibla)
        for i in range(0,ibla):
            l2bla[i]=lbla[i]
           
        redx,redy=zip(*l2red)
        blux,bluy=zip(*l2blu)
        if ibla>0:
            blax,blay=zip(*l2bla)
        #print l2red

        plt.figure(gn)
        plt.plot(redx,redy,'o',color='r')
        plt.plot(blux,bluy,'o',color='b')
        if ibla>0:
            plt.plot(blax,blay,'o',color='k')
        x=np.arange(-1.0,1.0,0.01)
        y=f(x)
        plt.plot(x,y)
        plt.show()
        
    def neararrow(self,gn):
        plist=self.pointlist
        plt.figure(gn)
        for i in range(0,len(plist)):#for every point
            if plist[i].near!=None: #if near has been assigned
                p1=plist[i].position #position of point
                for j in range(0,len(plist[i].near)): #for every member of near
                    p2=plist[i].near[j].position #position of neightbor
                    plt.arrow(p1[0],p1[1],p2[0]-p1[0],p2[1]-p1[1])
        plt.show()
        

def f1(x):
    return (x+0.5)*(x-0.5)*5*x
    

        
#This creates the enviorment and has half the points labeled as training data    
t1=datetime.now()
e=enviornment()
e.creatlist(2000,f1)
e.pointgraph(1,f1)


#This code  runs through each point and applies the nearest neighbor algorithm on it
for i in range(0,len(e.pointlist)):
    if e.pointlist[i].label==None:
        e.nearest(e.pointlist[i],3)
        e.pointlist[i].labelnearest()
        #print "\n"
e.pointgraph(2,f1)
e.neararrow(2)        
print str(datetime.now()-t1)


