import HELIOS
import AtomicMassTable
from KINEMATICS import KINEMATICS

import sys
import Tkinter
import pylab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import copy
import math
import matplotlib.pyplot as plt
import functools
import numpy

Ne20 =  AtomicMassTable.GetElement(10,20)
H1 =  AtomicMassTable.GetElement(1,1)
Ne21 =  AtomicMassTable.GetElement(10,21)
H2 =  AtomicMassTable.GetElement(1,2)
He4 =  AtomicMassTable.GetElement(2,4)
Na23 =  AtomicMassTable.GetElement(11,23)
Ti48 = AtomicMassTable.GetElement(22,48)
Au197 = AtomicMassTable.GetElement(79,197)

from PosManager import TrajectoryManager, Trajectory
K0=40
P1 = KINEMATICS(m=[Ne20[3],H2[3],Ne21[3],H1[3]], K0= K0,Eex2=2.8,Eex3=0)
P2 = KINEMATICS(m=[Ne20[3],H2[3],Ne21[3],H1[3]], K0= K0,Eex2=4.73,Eex3=0)
P3 = KINEMATICS(m=[Ne20[3],H2[3],Ne21[3],H1[3]], K0= K0,Eex2=6.26,Eex3=0)

tm = TrajectoryManager()
#tm.InitlalTrajectoriesWithFile()
import random
for j in numpy.linspace(-0.1,0.1,50):
    for i in range(90,92):
        P1.calculate(math.radians(i),math.radians(j))
        #print j, P1.philab3, P1.thetalab3
        tm.AddTrajectory(1, P1.thetalab3, P1.philab3 , P1.K3  ,H1[3], H1[2],2)
    for i in range(63,94):
        P2.calculate(math.radians(i),math.radians(j))
        tm.AddTrajectory(2, P2.thetalab3, P2.philab3 , P2.K3  ,H1[3], H1[2],2)
    for i in range(50,95):
        P3.calculate(math.radians(i),math.radians(j))
        tm.AddTrajectory(3, P3.thetalab3, P3.philab3 , P3.K3  ,H1[3], H1[2],2)

points = tm.GetPoints(0.26)
plt.figure(1)
#print points[1]
for groupID,ele in points.iteritems():
    plt.plot(zip(*ele)[0], zip(*ele)[1] ,'o')

plt.figure(2)
for groupID,ele in points.iteritems():
    plt.plot(zip(*ele)[3], zip(*ele)[2] ,'o')
#print zip(*ele)[3]#, zip(*ele)[2]
plt.figure(3)
#print "babala",

test = Trajectory(60,0,P2.K3  ,H1[3], H1[2],2)
ZPos = []
RPos = []

for i in xrange(0,1000):
    tmpz = 0.001*float(i)
    tmpx, tmpy,tmpE,tmpZ = test.GetPos(tmpz)
    ZPos.append(tmpz)
    RPos.append(math.sqrt(tmpx*tmpx+tmpy*tmpy))
    #print tmpx, tmpy,tmpZ,tmpE
plt.plot(ZPos,RPos,'.')
plt.show()
############# NavigationToolBar #####################
toolbar = NavigationToolbar2TkAgg( canvas, root )
toolbar.update()
#canvas._tkcanvas.place(relx = 0, rely = 0.95)
