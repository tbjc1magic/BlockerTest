import HELIOS
import math
import tbjcconstants

def Ek2v( m, Ek):
    """unit:m(kg),v(m/s)"""
    ratio_tmp = Ek/(m*tbjcconstants.c*tbjcconstants.c)
    v=tbjcconstants.c*math.sqrt(1-1/((ratio_tmp+1)*(ratio_tmp+1)))
    return v

class Trajectory:
    def __init__(self, theta, phi, energy, mass, charge, B):
        #print theta, phi, energy, mass, charge, B
        global Ek2v
        #############################
        self.theta = theta
        self.phi = phi
        self.mass = mass*tbjcconstants.u
        self.charge = charge*tbjcconstants.e
        self.energy = energy*tbjcconstants.MeV
        self.B = B
        ##############################
        self.v = Ek2v(self.mass, self.energy)
        self.Z = HELIOS.ZPos(self.v, math.radians(self.theta), self.charge/tbjcconstants.e, self.mass/tbjcconstants.u, self.B, arrayradius =0.01)
        self.OrbitR,self.OrbitT, = HELIOS.OrbitProperty(self.v, math.radians(theta),self.charge, self.mass, self.B)
        self.vpp = self.v*math.cos(math.radians(self.theta))
        self.vpr = self.v*math.sin(math.radians(self.theta))

    def GetPos(self, Zpos):
        TravelTime = Zpos/self.vpp
        Psi = 2*math.pi*TravelTime/self.OrbitT
        L = 2*self.OrbitR*math.sin(Psi/2)
        x = L*math.cos(Psi/2+math.radians(self.phi))
        y = L*math.sin(Psi/2+math.radians(self.phi))

        print Psi, self.phi, x,y
        return x,y,self.energy/tbjcconstants.MeV,self.Z

class TrajectoryManager:

    def __init__(self):
        self.Trajectories = {}

        return

    def InitialTrajectriesWithFile(self, filename):

        with open(filename) as f:
            content = f.readlines()
            for line in content:
                print line

        return

    def AddTrajectory(self, groupID,  theta, phi, energy, mass, charge, B ):

        if groupID not in self.Trajectories:
            self.Trajectories[groupID] = []
        self.Trajectories[groupID].append(Trajectory(theta, phi, energy, mass, charge, B))
        return self.Trajectories

    def GetPoints(self, Zpos):
        return_dict = {}
        for groupID in self.Trajectories:

            return_dict[groupID] = []

            for tr in self.Trajectories[groupID]:
                return_dict[groupID].append( tr.GetPos(Zpos) )

        return return_dict
