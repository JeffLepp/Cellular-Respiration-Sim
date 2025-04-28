# TODO: transfer M.ATP to C.ATP
# TODO: self regulate rate of metabolism
# TODO: GTP exporting/ -> atp
#       based on available ATP GTP?

from matrix import matrixState
import time

class mitochondriaClass():
    def __init__(self, cell):
        self.cell = cell
        self.matrix = matrixState()

    def exportATP(self):
        if (self.matrix.ATP >= 25):
            self.matrix.ATP -= 1
            self.cell.ATP += 1

    def run(self):
        for i in range(500):
            self.matrix.ETC.Cycle(self.matrix)
            self.matrix.CAC.Cycle(self.matrix)
            self.exportATP()
            time.sleep(.1)


class gylcolysis():
    def __init__(self, cell):
        self.cell = cell

# Stores all molecules in cytoplasm
class cellState():

    def __init__(self):
        self.mitochondria = mitochondriaClass(self)

        # Energy Molecules
        self.ADP = 100
        self.GTP = 100
        self.ATP = 100
        self.NAD = 100
        self.NADH = 100

        # Common Molecules
        self.O2 = 100
        self.H2O = 100

        # Glycolysis Molecules
        self.glucose = 100
        self.Glucose_6_Phosphate = 100
        self.Fructose_6_phosphate = 100
        self.Fructose_1_6_biphosphate = 100
        self.glyceraldehyde_3_phosphate = 100
        self.pyruvate = 100

cellMain = cellState()
cellMain.mitochondria.run()
