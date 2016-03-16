
import sys
import pylab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import copy
import math
import matplotlib.pyplot as plt
import functools
from RangeSlider import RangeSlider

import Tkinter
#################################################
############## GUI class ########################
#################################################

class tbjcGUI(Tkinter.Frame):

    def __init__(self, parent,controller):

        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.initGUI()

#    def _quit(self):
#        self.container.master.quit()
#        self.container.master.destroy()

    def initGUI(self):

       # self.master.title("bobo's lollipop")
        self.pack(fill=Tkinter.BOTH, expand=1)

        fig = plt.figure(1)
        self.ax = fig.add_subplot(111)
        self.ax.grid(True)
        self.ax.set_xlim([-0.5,0.5])
        self.ax.set_ylim([-0.5,0.5])
        self.ax.axhline(0, color='black')
        self.ax.axvline(0, color='black')
        self.parent.master.minsize(width=1000,height=600)
        self.BlockerShape = self.ax.plot([0,0,0.2,0.2,0],[0,0.2,0.2,0,0])
        #self.parent.master.protocol("WM_DELETE_WINDOW",self._quit)
        self.canvas = FigureCanvasTkAgg(fig,self)
        self.canvas.show()
        self.canvas.get_tk_widget().place(relwidth=0.35, relheight=0.4,relx=0.03,rely=0.05)

        fig2 = plt.figure(2)
        self.ax2 = fig2.add_subplot(111)
        self.ax2.grid(True)
        self.ax2.set_xlim([20,70])
        self.ax2.set_ylim([0,10])
        self.ax2.axhline(0, color='black')
        self.ax2.axvline(0, color='black')

        self.canvas2 = FigureCanvasTkAgg(fig2, self)
        self.canvas2.show()
        self.canvas2.get_tk_widget().place(relwidth=0.57, relheight=0.9,relx=0.4,rely=0.05)

        ############# initial Section #######################

        iframe1 = Tkinter.Frame(self, bd=2, relief=Tkinter.GROOVE, width=500, height=400  )
        iframe1.place(relwidth=0.35, relheight=0.2,relx=0.03,rely=0.5)

        # create the range slider widget to spec
        self.rs = RangeSlider(iframe1,
                         lowerBound = 0, upperBound = 100,
                         initialLowerBound = 25, initialUpperBound = 75);
        self.rs.setUpperBound(360)
        self.rs.setLowerBound(-60)
        self.rs.setLower(-22.5)
        self.rs.setUpper(22.5)
        self.rs.setMajorTickSpacing(60)
        self.rs.setMinorTickSpacing(10)
        self.rs.setPaintTicks(True)
        self.rs.setSnapToTicks(False)
        self.rs.setFocus()
        self.rs.place(relwidth=1, relheight=0.6,relx=0.,rely=0.0)
        self.rs.subscribe(self.slider_changeState  )

        self.phi1string = Tkinter.StringVar()
        self.phi1 = Tkinter.Label( iframe1, textvariable=self.phi1string, relief=Tkinter.GROOVE ,justify=Tkinter.RIGHT )
        self.phi1.place(relwidth = 0.25,relheight=0.3,relx = 0.05, rely=0.55)

        self.phi2string = Tkinter.StringVar()
        self.phi2 = Tkinter.Label( iframe1, textvariable=self.phi2string, relief=Tkinter.GROOVE,justify=Tkinter.RIGHT )
        self.phi2.place(relwidth = 0.25,relheight=0.3,relx = 0.35, rely=0.55)

        #self.slider_changeState(None)

        self.ResetButton = Tkinter.Button(iframe1, text ="Reset", command = self.ResetButton_CallBack)
        self.ResetButton.place(relwidth = 0.25,relheight=0.3,relx = 0.7, rely=0.55)

        ############# controller Section #######################

        iframe2 = Tkinter.Frame(self, bd=2, relief=Tkinter.GROOVE, width=500, height=400  )
        iframe2.place(relwidth=0.35, relheight=0.25,relx=0.03,rely=0.7)

        self.blocker_dict = {0:{"name":"X","initial":0,"lower":-0.5,"high":0.5},
                1: {"name":"Y","initial":0,"lower":-0.5,"high":0.5},
                2: {"name":"W","initial":1,"lower":0,"high":1},
                3:{"name":"H","initial":0.1,"lower":0,"high":0.5},
                4:{"name":"Z","initial":0.2,"lower":0,"high":0.8}}

        self.BlockerController = {}

        for groupID, prop in self.blocker_dict.iteritems():
            stmp = Tkinter.Scale(iframe2, from_=prop["lower"], to=prop["high"], resolution = (prop["high"]-prop["lower"])*0.01, command=functools.partial(self.BlockerChanged,groupID), orient = Tkinter.HORIZONTAL,showvalue=False)
            stmp.set(prop["initial"])
            stmp.place(relx = 0.05,rely = 0.05+0.17*groupID, relwidth = 0.3, relheight = 0.15)

            strvar = Tkinter.StringVar()
            ltmp = Tkinter.Label(iframe2,textvariable = strvar,relief=Tkinter.GROOVE)
            ltmp.place(relx = 0.4,rely = 0.05+0.17*groupID, relwidth = 0.2, relheight = 0.15)

            self.BlockerController[groupID] = {"scale":stmp,"label":strvar}

        self.DrawingButton = Tkinter.Button(iframe2, text ="Draw", command = self.DrawingButton_CallBack)
        self.DrawingButton.place(relx = 0.7, rely =0.1, relwidth = 0.2, relheight = 0.2)

        ############# NavigationToolBar #####################
        toolbar = NavigationToolbar2TkAgg( self.canvas, self )
        toolbar.update()
    def DrawingButton_CallBack(self):

        if self.controller.DrawingButton_CallBack is not None:
            self.controller.DrawingButton_CallBack()

    def BlockerChanged(self,groupID,*args):
        #print groupID, args[0]
        '''
        ct =  self.BlockerController[groupID]
        ct["label"].set(str(self.blocker_dict[groupID]["name"]+":"+args[0]))
        '''
        values = []
        for gi, dd in self.BlockerController.iteritems():
            values.append(dd["scale"].get())
        x1 = values[0]-values[2]/2
        x2 = values[0]+values[2]/2
        y1 = values[1]-values[3]/2
        y2 = values[1]+values[3]/2
        self.BlockerShape[0].set_data([x1,x1,x2,x2,x1],[y1,y2,y2,y1,y1])

        if groupID<=4:
            if self.controller.BlockerChanged_CallBack is not None:
                self.controller.BlockerChanged_CallBack(groupID, *args)

    def ResetButton_CallBack(self):

        if self.controller.ResetButton_CallBack is not None:
            self.controller.ResetButton_CallBack()

    def slider_changeState(self, e):
        '''
        phi1 = self.rs.getLower()
        phi2 = self.rs.getUpper()
        phi1string = "%.1f" % phi1
        self.phi1string.set("phi1:"+phi1string)
        phi2string = "%.1f" % phi2
        self.phi2string.set("phi2:"+phi2string)
        '''
        if self.controller.RS_CallBack is not None:
            self.controller.RS_CallBack()
