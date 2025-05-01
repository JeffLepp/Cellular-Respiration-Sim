import math
from logger_config import logger, molecule_logger, CAC_logger, GLY_logger

'''
These classes represent the matrix, including structures and relevent molecules
'''
# Stores all molecules in matrix
class matrixState():

    def __init__(self):
        self.calc = calculateETC(self)
        self.ETC = ClassETC(self)
        self.CAC = ClassCAC(self)
        self.mEnzymes = ClassMatrixEnzymes(self)

        # Working Molecules
        self.pyruvate = 100         # 3 Carbon
        self.acetylCoA = 100        # 2 Carbon
        self.oxaloacetate = 100     # 4 Carbon
        self.citrate = 100          # 6 Carbon
        self.isocitrate = 100       # 6 Carbon
        self.αKetoglutarate = 100   # 5 Carbon
        self.succinylCoA = 100      # 4 Carbon
        self.succinate = 100        # 4 Carbon
        self.fumarate = 100         # 4 Carbon
        self.malate = 100           # 4 Carbon

        # Electron Carriers
        self.FADH2 = 100
        self.FAD = 100
        self.NADH = 100
        self.NAD = 100

        # Energy Molecules
        self.ADP = 100
        self.GDP = 100
        self.GTP = 10
        self.ATP = 10
        self.protonsM = 850
        self.protonsIM = 10000

        # Gen carriers
        self.Ubiquinone = 1
        self.Semiquinone = 1
        self.Ubiquinol = 1
        self.cytochromeC_Fe3 = 1
        self.cytochromeC_Fe2 = 1

        # Common Molecules
        self.O2 = 100
        self.H2O = 100
        self.CO2 = 100



'''
These classes correspond to the citric acid cycles, provides NADH and FADH2 in exchange for pyruvate.
'''
# Basic enzymes for mitochondiral matrix
class ClassMatrixEnzymes():
    def __init__(self, matrix):
        self.matrix = matrix

    def pyruvate_dehydrogenase(self):
        if (self.matrix.O2 >= 1 and self.matrix.pyruvate >= 1 and self.matrix.NAD >= 1):
            self.matrix.pyruvate -= 1
            self.matrix.NAD -= 1
            self.matrix.acetylCoA += 1
            self.matrix.CO2 += 1
            self.matrix.NAD += 1

    def citrate_synthase(self):
        if (self.matrix.acetylCoA >= 1 & self.matrix.oxaloacetate >= 1):
            self.matrix.acetylCoA -= 1
            self.matrix.oxaloacetate -= 1
            self.matrix.citrate += 1

    def aconitase(self):
        if (self.matrix.citrate >= 1):
            self.matrix.citrate -= 1
            self.matrix.isocitrate += 1

    def isocitrate_dehydrogenase(self):
        if (self.matrix.isocitrate >=1):
            self.matrix.isocitrate -= 1
            self.matrix.αKetoglutarate += 1
    
    def αKetoglutarate_dehydrogenase(self):
        if (self.matrix.αKetoglutarate >= 1 and self.matrix.NAD >= 1):
            self.matrix.αKetoglutarate -= 1
            self.matrix.succinylCoA += 1
            self.matrix.CO2 += 1
            self.matrix.NAD -= 1
            self.matrix.NADH += 1

    def succinylCoA_synthetase(self):
        if (self.matrix.succinylCoA >= 1 and self.matrix.GDP >= 1):
            self.matrix.succinylCoA -= 1
            self.matrix.succinate += 1
            self.matrix.GDP -= 1
            self.matrix.GTP += 1

    def succinate_dehydrogenase(self):
        if (self.matrix.succinate >= 1 and self.matrix.FADH2 >= 1):
            self.matrix.succinate -= 1
            self.matrix.fumarate += 1
            self.matrix.FAD -= 1
            self.matrix.FADH2 += 1

    def fumarase(self):
        if (self.matrix.fumarate >= 1):
            self.matrix.fumarate -= 1
            self.matrix.malate += 1

    def malate_dehydrogenase(self):
        if (self.matrix.malate >= 1):
            self.matrix.malate -= 1
            self.matrix.oxaloacetate += 1
            self.matrix.NADH += 1

# Citric acid cycle
class ClassCAC():

    def __init__(self, matrix):
        self.matrix = matrix

    def Cycle(self):
        # (3C) Pyruvate + NAD → CO2 + (2C) Acetyl-CoA + NADH
        self.matrix.mEnzymes.pyruvate_dehydrogenase()

        # (2C) Acetyl-CoA + (4C) Oxaloacetate → (6C) Citrate
        self.matrix.mEnzymes.citrate_synthase()

        # (6C) Citrate → (6C) Isocitrate
        self.matrix.mEnzymes.aconitase()

        # (6C) Isocitrate → (5C) α-Ketoglutarate + CO₂ + NADH
        self.matrix.mEnzymes.isocitrate_dehydrogenase()

        # (5C) α-Ketoglutarate → (4C) Succinyl-CoA + CO₂ + NADH
        self.matrix.mEnzymes.αKetoglutarate_dehydrogenase()

        # (4C) Succinyl-CoA → (4C) Succinate + GTP
        self.matrix.mEnzymes.succinylCoA_synthetase()

        # (4C) Succinate → (4C) Fumarate + FADH2
        self.matrix.mEnzymes.succinate_dehydrogenase()

        # (4C) Fumarate → (4C) Malate
        self.matrix.mEnzymes.fumarase()

        # (4C) Malate → (4C) Oxaloacetate + NADH
        self.matrix.mEnzymes.malate_dehydrogenase()

        self.exportStatus(self.matrix)

    def exportStatus(self, matrix):
        status = (
            f"AcCoA:{matrix.acetylCoA}|Cit:{matrix.citrate}|IsCit:{matrix.isocitrate}|"
            f"aKG:{matrix.αKetoglutarate}|ScCoA:{matrix.succinylCoA}|"
            f"Suc:{matrix.succinate}|Fum:{matrix.fumarate}|Mal:{matrix.malate}|"
            f"OA:{matrix.oxaloacetate}"
        )
        CAC_logger.info(status)



'''
These classes correspond to the eletron trasport chain
'''
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
        if (matrix.cytochromeC_Fe2 and matrix.O2 >= 1):
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

        if (matrix.O2 >= 1):
            matrix.O2 -= 1 # diatomic O2
            matrix.protonsM -= 4
            matrix.H2O += 2
        else:
            logger.error("Complex IV Error: No free O2")

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
    
    # Tracks number of specific molecules in matrix for CAC
    def exportStatus(self, matrix):
        status = (
            f"NADH:{matrix.NADH} | NAD:{matrix.NAD} | FADH2:{matrix.FADH2} | FAD:{matrix.FAD} | "
            f"ADP:{matrix.ADP} | ATP:{matrix.ATP} | "
            f"O2:{matrix.O2} | H2O:{matrix.H2O}"
        )
        molecule_logger.info(status)

    # Cycle through the ETC
    def Cycle(self):
        self.ComplexI(self.matrix)
        self.ComplexII(self.matrix)
        self.ComplexIII(self.matrix)
        self.ComplexIV(self.matrix)
        self.ATPSynthase(self.matrix)
        self.exportStatus(self.matrix)
        logger.info(f"Cycle Completed: Matrix H+: {self.matrix.protonsM}, IMS H+: {self.matrix.protonsIM}, ATP: {self.matrix.ATP}, ΔΨ: {round(self.matrix.calc.protonDifferential() , 5)}")





