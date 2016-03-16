import HELIOS
import AtomicMassTable
from KINEMATICS import KINEMATICS
import Tkinter

Ne20 =  AtomicMassTable.GetElement(10,20)
H1 =  AtomicMassTable.GetElement(1,1)
Ne21 =  AtomicMassTable.GetElement(10,21)
H2 =  AtomicMassTable.GetElement(1,2)
He4 =  AtomicMassTable.GetElement(2,4)
Na23 =  AtomicMassTable.GetElement(11,23)
Ti48 = AtomicMassTable.GetElement(22,48)
Au197 = AtomicMassTable.GetElement(79,197)

MagneticFieldB =2.
K0=40

from Controller import tbjcController
from View import tbjcGUI
app = tbjcController()
app.mainloop()
