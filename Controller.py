import Tkinter
from View import tbjcGUI
from PosManager import TrajectoryManager, Trajectory
import random
import numpy
import AtomicMassTable
from KINEMATICS import KINEMATICS
import math
import sys

class tbjcController(Tkinter.Tk):

    def __init__(self, *args, **kwargs):

        Tkinter.Tk.__init__(self, *args, **kwargs)
        Tkinter.Tk.wm_title(self, "son of bobo")

        self.protocol("WM_DELETE_WINDOW",self._quit)
        container = Tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in {tbjcGUI}:

            frame = F(container, self)
            self.frames[F] = frame

        self.tbjcGUI = self.frames[tbjcGUI]
        self.tbjcGUI.slider_changeState(None)
        self.show_frame(tbjcGUI)
        self.initial_models()
        self.reset_points()
        self.reset_toDrawPoints()
        self.initial_plots()

    def initial_models(self):

        phi1 = self.tbjcGUI.rs.getLower()
        phi2 = self.tbjcGUI.rs.getUpper()
        self.reset_models(phi1,phi2)

    def reset_points(self):

        zpos = self.tbjcGUI.BlockerController[4]["scale"].get()
        self.points = self.tm.GetPoints(zpos)

    def reset_toDrawPoints(self):

        values = []
        for gi, dd in self.tbjcGUI.BlockerController.iteritems():
            values.append(dd["scale"].get())
        x1 = values[0]-values[2]/2
        x2 = values[0]+values[2]/2
        y1 = values[1]-values[3]/2
        y2 = values[1]+values[3]/2

        #print x1,x2,y1,y2
        shape = [[x1,y1], [x1,y2], [x2,y2], [x2,y1], [x1,y1],]

        self.toDrawPoints = {}
        for gi, itm in self.points.iteritems():
            self.toDrawPoints[gi] = []
            for pp in itm:
                if not self.IsInside([pp[0],pp[1]], shape):
                    self.toDrawPoints[gi].append(pp)
            if not self.toDrawPoints[gi]:
                self.toDrawPoints[gi].append([0,0,0,0])

        #self.toDrawPoints = self.points

    def IsInside(self,point,shape):
        x1 = shape[0][0]
        y1 = shape[0][1]
        x2 = shape[2][0]
        y2 = shape[1][1]

        x = point[0]
        y = point[1]

        #print x1,y1,x2,y2,":",x,y
        if x>x1 and x<x2 and y>y1 and y < y2:
            return True

        return False

    def reset_models(self,phi1,phi2):

        Ne20 =  AtomicMassTable.GetElement(10,20)
        H1 =  AtomicMassTable.GetElement(1,1)
        Ne21 =  AtomicMassTable.GetElement(10,21)
        H2 =  AtomicMassTable.GetElement(1,2)
        He4 =  AtomicMassTable.GetElement(2,4)
        Na23 =  AtomicMassTable.GetElement(11,23)
        Ti48 = AtomicMassTable.GetElement(22,48)
        Au197 = AtomicMassTable.GetElement(79,197)

        K0=38.5
        P1 = KINEMATICS(m=[Ne20[3],H2[3],Ne21[3],H1[3]], K0= K0,Eex2=2.8,Eex3=0)
        P2 = KINEMATICS(m=[Ne20[3],H2[3],Ne21[3],H1[3]], K0= K0,Eex2=4.73,Eex3=0)
        P3 = KINEMATICS(m=[Ne20[3],H2[3],Ne21[3],H1[3]], K0= K0,Eex2=6.26,Eex3=0)

        tm = TrajectoryManager()
        #tm.InitlalTrajectoriesWithFile()

        phirange = []
        resolution = 0.5
        if phi1<0:
            range1 = numpy.linspace(phi1+360,360,int(math.fabs(phi1)/resolution))
            range2 = numpy.linspace(0,phi2,int(math.fabs(phi2)/resolution))
            phirange = list(range1)+list(range2)
        else:
            phirange = list( numpy.linspace(phi1,phi2,int(math.fabs(phi2-phi1)/resolution))    )

        for j in phirange:
          #  for i in range(73,95):
            for i in range(73,95):
                P1.calculate(math.radians(i),math.radians(j))
                #print j, P1.philab3, P1.thetalab3
                tm.AddTrajectory(1, P1.thetalab3, P1.philab3+180 , P1.K3  ,H1[3], H1[2],2)
          #  for i in range(68,95):
            for i in range(68,95):
                P2.calculate(math.radians(i),math.radians(j))
                tm.AddTrajectory(2, P2.thetalab3, P2.philab3 +180, P2.K3  ,H1[3], H1[2],2)
          #  for i in range(60,95):
            for i in range(60,95):
                P3.calculate(math.radians(i),math.radians(j))
                tm.AddTrajectory(3, P3.thetalab3, P3.philab3+180 , P3.K3  ,H1[3], H1[2],2)

        self.tm = tm

    def initial_plots(self):

        colormap = ["r","b","black","green"]

        self.XYline = []
        self.EZ = []

        for gID, ele in self.toDrawPoints.iteritems():
            self.XYline.append(self.tbjcGUI.ax.plot(zip(*ele)[0],zip(*ele)[1],'.',c=colormap[gID]))
            self.EZ.append(self.tbjcGUI.ax2.plot( zip(*ele)[3],zip(*ele)[2] ,'.',c=colormap[gID]))

    def redraw(self):

        for gID, ele in self.toDrawPoints.iteritems():
            self.XYline[gID-1][0].set_data(zip(*ele)[0],zip(*ele)[1])
            self.EZ[gID-1][0].set_data( zip(*ele)[3],zip(*ele)[2])

        self.tbjcGUI.canvas.draw()
        self.tbjcGUI.canvas2.draw()
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def BlockerChanged_CallBack(self,groupID,*args):
        ct = self.tbjcGUI.BlockerController[groupID]
        ct["label"].set(str(self.tbjcGUI.blocker_dict[groupID]["name"]+":"+args[0]))
        self.reset_toDrawPoints()
        self.redraw()
    def ResetButton_CallBack(self):
        #print "bobo1"
        phi1 = self.tbjcGUI.rs.getLower()
        phi2 = self.tbjcGUI.rs.getUpper()
        self.reset_models(phi1,phi2)

        self.reset_points()
        self.reset_toDrawPoints()
        self.redraw()
    def RS_CallBack(self):
        phi1 = self.tbjcGUI.rs.getLower()
        phi2 = self.tbjcGUI.rs.getUpper()
        phi1string = "%.1f" % phi1
        self.tbjcGUI.phi1string.set("phi1:"+phi1string)
        phi2string = "%.1f" % phi2
        self.tbjcGUI.phi2string.set("phi2:"+phi2string)

    def DrawingButton_CallBack(self):
        phi1 = self.tbjcGUI.rs.getLower()
        phi2 = self.tbjcGUI.rs.getUpper()
        self.reset_models(phi1,phi2)

        self.reset_points()
        self.reset_toDrawPoints()
        self.redraw()
    def _quit(self):
        self.quit()
        self.destroy()
