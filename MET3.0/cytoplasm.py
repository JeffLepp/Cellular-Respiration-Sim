# TODO: transfer M.ATP to C.ATP
# TODO: self regulate rate of metabolism
# TODO: GTP exporting/ -> atp
#       based on available ATP GTP?

from matrix import matrixState, GLY_logger
import time


'''
These classes represent the cytoplasm of a cell
'''
# Stores all molecules in cytoplasm
class cellState():

    def __init__(self):
        self.mitochondria = mitochondriaClass(self)
        self.glycolysis = ClassGylcolysis(self)
        self.gEnzymes = ClassGlycolysisEnzymes(self)

        # Energy Molecules
        self.ADP = 100
        self.GTP = 100
        self.ATP = 100
        self.NAD = 100
        self.NADH = 100

        # Common Molecules
        self.O2 = 100
        self.H2O = 100
        self.Pi = 100

        # Glycolysis Molecules
        self.glucose = 100
        self.glucose_6_phosphate = 100
        self.fructose_6_phosphate = 100
        self.fructose_1_6_biphosphate = 100
        self.glyceraldehyde_3_phosphate = 100
        self.dihydroxyl_acetone_phosphate = 100 
        self.biphospho_1_3_glycerate = 100 # techncially prefixed with 1,3-
        self.phospho_3_glycerate = 100 # prefixed with 3-
        self.phospho_2_glycerate = 100
        self.phospho_enol_pyruvate = 100
        self.pyruvate = 100

# Represents a mitochondrion in the cytoplasm
class mitochondriaClass():
    def __init__(self, cell):
        self.cell = cell
        self.matrix = matrixState()

    def exportATP(self):
        if (self.matrix.ATP >= 25):
            self.matrix.ATP -= 1
            self.cell.ATP += 1



'''
These classes correspond to Glyolysis in the cytoplasm
'''
# Stores enzymes for glycolytic enzymes
class ClassGlycolysisEnzymes():
    def __init__(self, cell):
        self.cell = cell

    def hexokinase(self, cell):
        if (self.cell.glucose >= 1 and self.cell.ATP >= 1):
            self.cell.glucose -= 1
            self.cell.glucose_6_phosphate += 1
            self.cell.ATP -= 1
            self.cell.ADP += 1

    def phospho_glucose_isomerase(self, cell):
        if (self.cell.glucose_6_phosphate >= 1):
            self.cell.glucose_6_phosphate -= 1
            self.cell.fructose_6_phosphate += 1

    def phospho_fructo_kinase(self, cell):
        if (self.cell.fructose_6_phosphate >= 1 and self.cell.ATP >= 1):
            self.cell.fructose_6_phosphate -= 1
            self.cell.fructose_1_6_biphosphate += 1
            self.cell.ATP -= 1
            self.cell.ADP += 1

    def aldolase(self, cell):
        if (self.cell.fructose_1_6_biphosphate >= 1):
            self.cell.fructose_1_6_biphosphate -= 1
            self.cell.dihydroxyl_acetone_phosphate += 1
            self.cell.glyceraldehyde_3_phosphate += 1

    def triose_phosphate_isomerase(self, cell):
        if (self.cell.dihydroxyl_acetone_phosphate >= 1):
            self.cell.dihydroxyl_acetone_phosphate -= 1
            self.cell.glyceraldehyde_3_phosphate += 1

    def glyceraldehyde_phosphate_dehydrogenase(self, cell):
        if (self.cell.NAD >= 1 and self.cell.glyceraldehyde_3_phosphate >= 1 and self.cell.Pi >= 1):
            self.cell.glyceraldehyde_3_phosphate -= 1
            self.cell.NAD -= 1
            self.cell.Pi -= 1
            self.cell.NADH += 1
            self.cell.biphospho_1_3_glycerate += 1

    def phospho_glycerate_kinase(self, cell):
        if (self.cell.biphospho_1_3_glycerate >= 1 and self.cell.ADP >= 1):
            self.cell.biphospho_1_3_glycerate -= 1
            self.cell.ADP -= 1
            self.cell.phospho_3_glycerate += 1
            self.cell.ATP += 1

    def phospho_glycerate_mutase(self, cell):
        if (self.cell.phospho_3_glycerate >= 1):
            self.cell.phospho_3_glycerate -= 1
            self.cell.phospho_2_glycerate += 1

    def enolase(self, cell):
        if (self.cell.phospho_2_glycerate >= 1):
            self.cell.phospho_2_glycerate -= 1
            self.cell.H2O += 1
            self.cell.phospho_enol_pyruvate += 1

    def pyruvate_kinase(self, cell):
        if (self.cell.phospho_enol_pyruvate >= 1 & self.cell.ADP >= 1):
            self.cell.phospho_enol_pyruvate -= 1
            self.cell.ADP -= 1
            self.cell.pyruvate += 1
            self.cell.ATP += 1

# Glycolysis
class ClassGylcolysis():
    def __init__(self, cell):
        self.cell = cell

    # TODO: add comments
    def Cycle(self):
        self.cell.gEnzymes.hexokinase(self.cell)
        self.cell.gEnzymes.phospho_glucose_isomerase(self.cell)
        self.cell.gEnzymes.phospho_fructo_kinase(self.cell)
        self.cell.gEnzymes.aldolase(self.cell)
        self.cell.gEnzymes.triose_phosphate_isomerase(self.cell)
        self.cell.gEnzymes.glyceraldehyde_phosphate_dehydrogenase(self.cell)
        self.cell.gEnzymes.phospho_glycerate_kinase(self.cell)
        self.cell.gEnzymes.phospho_glycerate_mutase(self.cell)
        self.cell.gEnzymes.enolase(self.cell)
        self.cell.gEnzymes.pyruvate_kinase(self.cell)

    def exportGlycolysisStatus(self):
        status = (
            f"Glc:{self.cell.glucose}|G6P:{self.cell.glucose_6_phosphate}|F6P:{self.cell.fructose_6_phosphate}|"
            f"FBP:{self.cell.fructose_1_6_biphosphate}|GAP:{self.cell.glyceraldehyde_3_phosphate}|"
            f"DHAP:{self.cell.dihydroxyl_acetone_phosphate}|BPG:{self.cell.biphospho_1_3_glycerate}|"
            f"3PG:{self.cell.phospho_3_glycerate}|"
            f"PEP:{self.cell.phospho_enol_pyruvate}|Pyr:{self.cell.pyruvate}"
        )
        GLY_logger.info(status)



cellMain = cellState()

for i in range(500):
    cellMain.mitochondria.matrix.ETC.Cycle()
    cellMain.mitochondria.matrix.CAC.Cycle()
    cellMain.glycolysis.Cycle()
    cellMain.mitochondria.exportATP()
    cellMain.glycolysis.exportGlycolysisStatus()
    time.sleep(.1)