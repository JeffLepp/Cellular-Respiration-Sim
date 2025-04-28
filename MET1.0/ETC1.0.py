import math

# Includes Electron Carrying molecules, isolated complexes, proton count between IMS and Matrix, 
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
        print("Membrane Potential (ΔΨ) equals: ", round(deltaPSI, 10))
        return deltaPSI
    
class cellState():
    def __init__(self):
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
        self.ubiquinone = 10
        self.semiquinone = 10
        self.ubiquinol = 10
        self.cytochromeC = 1

        # Common Molecules
        self.oxygen = 10
        self.water = 10

class complex():

    def __init__(self):

        # Utility classes
        self.calculateETC = calculateETC(self)
        self.cell = cellState()

        # Electron Carriers
        self.FADH2 = 100
        self.FAD = 100
        self.NADH = 100
        self.NAD = 100

        # Energy Molecules
        self.ADP = 100
        self.ATP = 0
        self.protonsM = 700
        self.protonsIM = 10000

        # Gen carriers
        self.ubiquinone = 10
        self.semiquinone = 10
        self.ubiquinol = 10
        self.cytochromeC = 1

        # Common Molecules
        self.oxygen = 10
        self.water = 10

    def ComplexI(self):

        # Donating a electron pair
        if self.cell.NADH > 0:

            print(f"Complex I: NADH [{self.cell.NADH}] donating 2 electrons")
            self.cell.NAD += 1
            self.cell.NADH -= 1
            self.cell.protonsM += 1

            # Pumping 4 protons
            # moving protons = electricity, which is where the energy to drive proton pumping comes from. On a lower lvl, its a redox reaction from NADH and COMPLEX I.
            print(f"Complex 1: Pumped 4 protons into IMS [{self.cell.protonsIM}]")
            self.cell.protonsM -= 4
            self.cell.protonsIM += 4

            # Ubiquinone uptaking electron pair
            self.cell.ubiquinone -= 1

            print(f"Complex I: Semiquinone [{self.cell.semiquinone}] radical formed")
            #.ubiquinol may not be made until complex 2, this is an intermediate of some sort in reality
            self.cell.semiquinone += 1

        else:
            print()

    def ComplexII(self):

        if self.cell.FADH2 > 0:

            # FADH2 donates, releasing 2 protons
            print(f"Complex II: FADH2 [{self.cell.FADH2}] donates 2H+ and 2 electrons")
            self.cell.FADH2 -= 1
            self.cell.FAD += 1
            self.cell.protonsM += 2

            print(f"Complex II:.ubiquinol [{self.cell.ubiquinol}] formed")
            self.cell.ubiquinol += 1
            self.cell.protonsM -= 2
        
        else:
            print()


    def ComplexIII(self):

        if self.cell.ubiquinol > 0:

            #.ubiquinol donates the 2 electron pairs to Complex III
            print(f"Complex III:ubiquinol [{self.cell.ubiquinol}] donates 2 electron pairs")
            self.cell.ubiquinol -= 1
            self.cell.ubiquinone += 1
            self.cell.protonsM += 2

            print(f"Complex III: Pumped 4 protons into IMS [{self.cell.protonsIM}]")
            self.cell.protonsM -= 4
            self.cell.protonsIM += 4

            print(f"Complex III: CytochromeC picks up electrons")
            self.cell.cytochromeC += 1

        else:
            print()

    def ComplexIV(self):
        
        if self.cell.cytochromeC > 0:

            # Cytochrome C donates electrons for a final pump, before devliering to oxygen
            print(f"Complex IV: ")
            self.cell.cytochromeC-= 1

            print(f"Complex IV: ")
            self.cell.protonsM -= 2
            self.cell.protonsIM += 2

            # Finished with electrons
            print(f"Complex IV: Water is produced with ")
            self.cell.oxygen -= 2
            self.cell.protonsM -= 4
            self.cell.water += 2
        
        else:
            print()

    def ATPSynthase(self):
        if self.cell.calculateETC.protonDifferential() > .12:
            self.cell.protonsM += 3
            self.cell.protonsIM -= 3
            self.cell.ADP -= 1
            self.cell.ATP += 1

    def runCycle(self):
        self.ComplexI()
        self.ComplexII()
        self.ComplexIII()
        self.ComplexIV()
        self.ATPSynthase()
        self.calculateETC.protonDifferential()
        self.printDetails()

    def printDetails(self):
        print(f"ATP: {self.cell.ATP}")
        print(f"Protons in Matrix: {self.cell.protonsM}")
        print(f"Protons in IMS: {self.cell.protonsIM}")
        #print(f"NADH: {self.NADH}, NAD+: {self.NAD}")
        #print(f"FADH2: {self.FADH2}, FAD: {self.FAD}")
        #print(f"Ubiquinone: {self.ubiquinone},.ubiquinol: {self.ubiquinol}")
        #print(f"Oxygen: {self.oxygen}, Water: {self.water}")
        #print(f"Cytochrome C: {self.cytochromeC}")
        print("-------------------------------")

class glycolysis():
    def __init__(self):
        self.NADH = 1
    
ETC = complex()
cell = cellState()

i = 0
while (i < 70):
    i += 1
    ETC.runCycle()


