import csv
import numpy as np
import Image
import matplotlib.pyplot as pp
import pylab as pl

def getd(filename):  #takes files and returns list of list of ints after hacking of a empty string ""
    with open(filename,'r') as f:
        reader=csv.reader(f,delimiter=' ')
        d=list(reader)
        for i in range(0,len(d)):
            if d[i][-1]=="":
                d[i]=d[i][:-1]
            for j in range(0,len(d[i])):
                d[i][j]=int(d[i][j])
    #for i in range(0,len(d)):
        #print len(d[i])
    return d

class point:
    def __init__(self,vect):
        if len(vect)==785:
            self.vector=np.array(vect[:-1])
            self.label=vect[-1]
        elif len(vect)==784:
            self.vector=np.array(vect)
            self.label=None
        else:
            raise ValueError("Invalid vector length.  Must be 785 for training 784 for testing") 
    
    def type(self):
        return "point"
        
class evo:
    def __init__(self):
        self.trainlist=None
        
    def train(self,plist):
        l=[None]*len(plist)
        for i in range(0,len(plist)):
            l[i]=point(plist[i])
        self.trainlist=l
        
    def knn(self,vect,k): #vect should be an int list
        nearest=[None]*k
        p=point(vect)
        tl=self.trainlist
        ni=0
        for i in range(0,len(tl)):
            if ni<k:
                nearest[i]=tl[i]
                #print str(ni)+"slot of nearest filled"
                if ni==k-1:
                    neardist=[None]*k
                    for j in range(0,len(nearest)):
                        neardist[j]=np.linalg.norm(p.vector-nearest[j].vector)
                    #print neardist
                    #print max(neardist)
                    #print neardist.index(max(neardist))
                    imax=neardist.index(max(neardist))  
                    maxdist=neardist[imax] 
                ni=ni+1         
            else:
                d=np.linalg.norm(p.vector-tl[i].vector)
                if maxdist>d:
                    nearest[imax]=tl[i]
                    neardist[imax]=d
                    imax=neardist.index(max(neardist))        
        return nearest
        
    def label(self,vect,k):
        n=self.knn(vect,k)
        llist=[None]*k
        for i in range(0,len(n)):
            llist[i]=n[i].label
        lset=list(set(llist)) #set of unique labels
        clist=[None]*len(lset) #count for each label
        for i in range(0,len(lset)):
            clist[i]=llist.count(lset[i])
        return lset[clist.index(max(clist))]

            
        
filetrain='C:\Users\Neima\Desktop\NearestNeighbor\hw2train.txt'
e=evo()
e.train(getd(filetrain))
print "Trained"
filetest='C:\Users\Neima\Desktop\NearestNeighbor\hw2test.txt'
test=getd(filetest)


t=[[None,None]]*len(test)
for i in range(0,len(test)):
    #print "i is "+str(i)
    t[i]=[e.label(test[i],4),test[i][-1]]
print t

def toimage(vect,m,n): 
    v=vect[:-1]
    v1=[[0]*m]*n
    v2=np.array(v1)
    for i in range(0,m):
        for j in range(0,n):
            v2[i,j]=float(v[i*m+j])
    pl.imshow(v2)
    pl.show()
    return v2
pl.figure(2)    
v3=toimage(test[2],28,28)
pl.figure(3)
v3=toimage(test[3],28,28)
pl.figure(4)
v3=toimage(test[4],28,28)

#Link might be helpful http://matplotlib.org/users/image_tutorial.html
    