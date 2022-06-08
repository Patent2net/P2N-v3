import os
import sys


class P2NConfig:
    def __init__(self, file):

        # Global path for results
        self.GlobalPath = '../DATA'
        self.file = file

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
        # Format process
        self.FormateExportCountryCartography = False
        self.FormateExportBiblio = False
        self.FormateExportDataTable = False
        self.FormateExportPivotTable = False
        self.FusionIramuteq2 = False
        self.FreePlane = False
        self.FusionCarrot2 = False
        self.Cluster = False
        # opening request file, reading parameters
        content = self.readInputFile()

        for line in content:
            # General config loading
            if line.count('request:') > 0:
                self.requete = self.getStr(line)
            elif line.count('DataDirectory:') > 0:
                self.ndf = self.getStr(line)#.title()
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
            elif line.count('FusionIramuteq2') > 0:
                self.FusionIramuteq2 = self.getBoolean(line)    
            elif line.count('P2N-Cluster') > 0:
                self.Cluster = self.getBoolean(line)
        self.generatePaths()

    def readInputFile(self):
        if len(sys.argv) > 1:
            for arg in sys.argv:
                self.file = arg
                if ".cql" in arg.lower():
                    return open(arg, "r").readlines()

        if self.file != None:
            if ".cql" in self.file.lower():
                file_path = '../RequestsSets/' + self.file
                return open(file_path, "r").readlines()

        return open("../requete.cql", "r").readlines()

    def generatePaths(self):
        self.ResultPath = os.path.normpath(os.path.join(self.GlobalPath, self.ndf)).replace('\\','/')
        self.ResultListPath = os.path.normpath(self.ResultPath + '/PatentLists').replace('\\','/')
        self.ResultBiblioPath = os.path.normpath(self.ResultPath + '/PatentBiblios').replace('\\','/')
        self.ResultContentsPath = os.path.normpath(self.ResultPath + '/PatentContents').replace('\\','/')
        self.temporPath = os.path.normpath(self.ResultPath + '/tempo').replace('\\','/')
        self.ResultAbstractPath = os.path.normpath(self.ResultContentsPath + '/Abstract').replace('\\','/')
        self.ResultFamiliesAbstractPath = os.path.normpath(self.ResultContentsPath + '/FamiliesAbstract').replace('\\','/')
        self.ResultGephiPath = os.path.normpath(self.ResultPath + '/GephiFiles').replace('\\','/')
        self.ResultPathImages = os.path.normpath(self.ResultPath + '/PatentImages').replace('\\','/')
        self.ResultClusterPath =  os.path.normpath(self.ResultContentsPath+'/Metrics').replace('\\','/')
        for path in [
            self.ResultListPath,
            self.ResultBiblioPath,
            self.ResultContentsPath,
            self.temporPath,
            self.ResultAbstractPath,
            self.ResultFamiliesAbstractPath,
            self.ResultGephiPath,
            self.ResultPathImages,
            self.ResultClusterPath,
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

    def show(self):
        for cle in self.__dict__.keys():
            print (cle, " -->" , self .__dict__[cle])

def LoadConfig(file = None):
    return P2NConfig(file)
