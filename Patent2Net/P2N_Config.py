import os
import sys


class P2NConfig:
    def __init__(self):

        # Global path for results
        self.GlobalPath = '..//DATA'

        # Initiate all empty attributes
        self.requete = ""
        self.ndf = ""
        self.GatherContent = False
        self.GatherBiblio = False
        self.GatherPatent = False
        self.GatherFamilly = False
        self.GatherIramuteq = False
        self.GatherImages = False
        # Networks config loading
        self.InventorNetwork = False
        self.ApplicantNetwork = False
        self.ApplicantInventorNetwork = False
        self.InventorCrossTechNetwork = False
        self.ApplicantCrossTechNetwork = False
        self.CountryCrossTechNetwork = False
        self.CrossTechNetwork = False
        self.CompleteNetwork = False
        self.References = False
        self.Citations = False
        self.Equivalents = False
        self.FormateExportCountryCartography = False
        self.FormateExportBiblio = False
        self.FormateExportDataTable = False
        self.FormateExportPivotTable = False

        self.FreePlane = False
        self.FusionCarrot2 = False

        # opening request file, reading parameters
        content = self.readInputFile()

        for line in content:
            # General config loading
            if line.count('request:') > 0:
                self.requete = self.getStr(line)
            elif line.count('DataDirectory:') > 0:
                self.ndf = self.getStr(line)
            elif line.count('OPSGatherContentsv2-Iramuteq') > 0:
                self.GatherIramuteq = self.getBoolean(line)
            elif line.count('GatherContent') > 0:
                self.GatherContent = self.getBoolean(line)
            elif line.count('GatherBiblio') > 0:
                self.GatherBiblio = self.getBoolean(line)
            elif line.count('GatherPatent') > 0:
                self.GatherPatent = self.getBoolean(line)
            elif line.count('GatherFamilly') > 0:
                self.GatherFamilly = self.getBoolean(line)
            elif line.count('GatherImages') > 0:
                self.GatherImages = self.getBoolean(line)

            # Networks config loading
            elif line.count('InventorNetwork') > 0:
                self.InventorNetwork = self.getBoolean(line)
            elif line.count('ApplicantNetwork') > 0:
                self.ApplicantNetwork = self.getBoolean(line)
            elif line.count('ApplicantInventorNetwork') > 0:
                self.ApplicantInventorNetwork = self.getBoolean(line)
            elif line.count('InventorCrossTechNetwork') > 0:
                self.InventorCrossTechNetwork = self.getBoolean(line)
            elif line.count('ApplicantCrossTechNetwork') > 0:
                self.ApplicantCrossTechNetwork = self.getBoolean(line)
            elif line.count('CountryCrossTechNetwork') > 0:
                self.CountryCrossTechNetwork = self.getBoolean(line)
            elif line.count('CrossTechNetwork') > 0:
                self.CrossTechNetwork = self.getBoolean(line)
            elif line.count('CompleteNetwork') > 0:
                self.CompleteNetwork = self.getBoolean(line)
            elif line.count('References') > 0:
                self.References = self.getBoolean(line)
            elif line.count('Citations') > 0:
                self.Citations = self.getBoolean(line)
            elif line.count('Equivalents') > 0:
                self.Equivalents = self.getBoolean(line)
            elif line.count('FormateExportCountryCartography') > 0:
                self.FormateExportCountryCartography = self.getBoolean(line)
            elif line.count('FormateExportPivotTable') > 0:
                self.FormateExportPivotTable = self.getBoolean(line)
            elif line.count('FormateExportBiblio') > 0:
                self.FormateExportBiblio = self.getBoolean(line)
            elif line.count('FormateExportDataTable') > 0:
                self.FormateExportDataTable = self.getBoolean(line)
            elif line.count('P2N-FreePlane') > 0:
                self.FreePlane = self.getBoolean(line)
            elif line.count('FusionCarrot2') > 0:
                self.FusionCarrot2 = self.getBoolean(line)

        self.generatePaths()

    def readInputFile(self):
        if len(sys.argv) > 1:
            for arg in sys.argv:
                if ".cql" in arg.lower():
                    return open(arg, "r").readlines()
        return open("..//requete.cql", "r").readlines()

    def generatePaths(self):
        self.ResultPath = os.path.normpath(os.path.join(self.GlobalPath, self.ndf))
        self.ResultListPath = os.path.normpath(self.ResultPath + '//PatentLists')
        self.ResultBiblioPath = os.path.normpath(self.ResultPath + '//PatentBiblios')
        self.ResultContentsPath = os.path.normpath(self.ResultPath + '//PatentContents')
        self.temporPath = os.path.normpath(self.ResultPath + '//tempo')
        self.ResultAbstractPath = os.path.normpath(self.ResultContentsPath + '//Abstract')
        self.ResultFamiliesAbstractPath = os.path.normpath(self.ResultContentsPath + '//FamiliesAbstract')
        self.ResultGephiPath = os.path.normpath(self.ResultPath + '//GephiFiles')
        self.ResultPathImages = os.path.normpath(self.ResultPath + '//PatentImages')
        for path in [
            self.ResultListPath,
            self.ResultBiblioPath,
            self.ResultContentsPath,
            self.temporPath,
            self.ResultAbstractPath,
            self.ResultFamiliesAbstractPath,
            self.ResultGephiPath,
            self.ResultPathImages,
        ]:
            
            if not os.path.isdir(path):
                os.makedirs(path)

    def getStr(self, line):
        return line.split(':')[1].strip()

    def getBoolean(self, line):
        s = self.getStr(line)
        if s.count('True') > 0 or s.count('true') > 0:
            return True  # to gather contents
        else:
            return False


def LoadConfig():
    return P2NConfig()
