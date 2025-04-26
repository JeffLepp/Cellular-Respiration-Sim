import math
import json
import time
import subprocess
from Logging_config import logger, molecule_logger


# Basic calculations for ETC
class calculateETC():
    def __init__(self, parent):
        self.parent = parent

    def protonDifferential(self):
        # Nernst-based Approach
        R = 8.314 # Ideal gas constant
        T = 310 # Kelvin, about body temp
        F = 96485 # Faraday's constant

        # Ratio for volume difference, Inter Membrane Space is about 10x smaller than matrix
        volM = 1 # Matrix
        volIM = .1 # Inter Membrane Space

        protonsM = self.parent.protonsM / volM
        protonsIM = self.parent.protonsIM / volIM

        if protonsM == 0 or protonsIM == 0:
            print("No protons in IM or IMS")
            return None

        deltaPSI = (R * T / F) * math.log(protonsIM / protonsM)
        return deltaPSI


# Stores all molecules in cell
class cellState():

    def __init__(self):

        # Energy Molecules
        self.ADP = 100
        self.ATP = 0

        # Common Molecules
        self.oxygen = 100
        self.water = 100


# Stores all molecules in matrix
class matrixState():

    def __init__(self):
        self.calc = calculateETC(self)
        self.ETC = ClassETC(self)

        # Electron Carriers
        self.FADH2 = 100
        self.FAD = 100
        self.NADH = 100
        self.NAD = 100

        # Energy Molecules
        self.ADP = 100
        self.ATP = 0
        self.protonsM = 850
        self.protonsIM = 10000

        # Gen carriers
        self.Ubiquinone = 1
        self.Semiquinone = 1
        self.Ubiquinol = 1
        self.cytochromeC_Fe3 = 1
        self.cytochromeC_Fe2 = 1

        # Common Molecules
        self.oxygen = 100
        self.water = 100


# Electron Transport Chain
class ClassETC():

    def __init__(self, matrix):
        self.matrix = matrix

    # Complex I donates NADH, pumps 4H+
    def ComplexI(self, matrix):

        # Here we pass a NADH, which becomes NAD and H
        if (matrix.NADH >= 1): 
            matrix.NADH -= 1
            matrix.NAD += 1
            matrix.protonsM += 1

        # 4 Protons are pumped, moving protons = electricity
        if (matrix.protonsM >= 4) and (matrix.calc.protonDifferential() < .22): 
            matrix.protonsM -= 4
            matrix.protonsIM += 4

        # Ubiquinone takes 2e- to form semiquinone
        if(matrix.Ubiquinone >= 1): 
            matrix.Ubiquinone -= 1
            matrix.Semiquinone += 1

    # Complex II donates FADH2, pumps 0H+
    def ComplexII(self, matrix):
        
        # Pass a FADH2 and releases 2H+, pumps 0 protons
        if (matrix.FADH2 >= 1):
            matrix.FADH2 -= 1
            matrix.FAD += 1
            matrix.protonsM += 2
        
        # Semiquinol uptakes 2e- and becomes Ubiquinol
        if (matrix.Semiquinone >= 1):
            matrix.Semiquinone -= 1
            matrix.Ubiquinol += 1

    # Complex III pumps 4H+ from 2 pairs of 2e- from Ubiquinol
    def ComplexIII(self, matrix):

        # Ubiquinol passes it's electrons and 4 protons are pumped
        if (matrix.Ubiquinol >= 1):
            matrix.Ubiquinol -= 1
            matrix.Ubiquinone += 1

            # Protons are pumped
            if (matrix.protonsM >= 4) and (matrix.calc.protonDifferential() < .22):
                matrix.protonsM -= 4
                matrix.protonsIM += 4
            else:
                logger.error("Complex III Error: Out of protons!")

            # Cytochrome C picks up electrons and becomes Fe3+ to Fe2+, Note: 1 e- at a time with heme group (Fe3+ -> Fe2+) in reality
            if (matrix.cytochromeC_Fe3 >= 1):
                matrix.cytochromeC_Fe3 -= 1
                matrix.cytochromeC_Fe2 += 1
            else:
                logger.error("Complex III Error: No cytochromeC!")

        else: 
            logger.error("Complex III Error: No Ubiquinol to run!")

    # Complex IV pumps 2H+ and converts O2 into 2(H2O) with 4H+
    def ComplexIV(self, matrix):

        # Cytochrome donates its electrons
        if (matrix.cytochromeC_Fe2):
            matrix.cytochromeC_Fe2 -= 1
            matrix.cytochromeC_Fe3 += 1

            # 2H+ are pumped
            if (matrix.protonsM >= 2) & (matrix.calc.protonDifferential() < .22):
                matrix.protonsM -= 2
                matrix.protonsIM += 2
            else:
                logger.error("Complex IV Error: No H+ in matrix")
        else:
            logger.error("Complex IV Error: No cytochrome_Fe2")

        if (matrix.oxygen >= 1):
            matrix.oxygen -= 1 # diatomic oxygen
            matrix.protonsM -= 4
            matrix.water += 2

    # Uses proton differential to drive 3 H+ into matrix and use ocidative phosphylation to make ADP -> ATP (Note: moving protons = electricity!)
    def ATPSynthase(self, matrix):

        if (matrix.calc.protonDifferential() > .12) and matrix.ADP >= 1:
            matrix.protonsM += 3
            matrix.protonsIM -= 3
            matrix.ADP -= 1
            matrix.ATP += 1
        else:
            logger.error("ATP Synthase Error: Differential or ADP absent")

    # Correlates to console output
    def exportStatus(self, matrix):
        status = (
            f"NADH:{matrix.NADH} | NAD:{matrix.NAD} | FADH2:{matrix.FADH2} | FAD:{matrix.FAD} | "
            f"ADP:{matrix.ADP} | ATP:{matrix.ATP} | "
            f"Oxygen:{matrix.oxygen} | Water:{matrix.water}"
        )
        molecule_logger.info(status)

    # Cycle through the ETC
    def Cycle(self, Bigcell):
        self.ComplexI(Bigcell)
        self.ComplexII(Bigcell)
        self.ComplexIII(Bigcell)
        self.ComplexIV(Bigcell)
        self.ATPSynthase(Bigcell)
        self.exportStatus(Bigcell)
        logger.info(f"Cycle Completed: Matrix H+: {Bigcell.protonsM}, IMS H+: {Bigcell.protonsIM}, ATP: {Bigcell.ATP}, ΔΨ: {round(Bigcell.calc.protonDifferential() , 5)}")



Bigcell = matrixState()
Bigcell.ETC.Cycle(Bigcell) 

for i in range(100):
    Bigcell.ETC.Cycle(Bigcell)
    time.sleep(.01)


