# Patent2Net V3 configuration file
##############################
# request
# insert below your request in cql format as done in the example
request: TA=RequestName

##############################
# Directory to use
# insert a compliant name (no space or special characters) for the "Patent Universe" (PU)
DataDirectory: RequestName

###############################
#Patent2Net options : Set to *True* or False
###############################
# Collecting
# patents list corresponding to the request. e.g the "Patent Universe" (PU)
GatherPatent: True

# patents bibliographic data corresponding to patent list
GatherBiblio: True

# patent content (description, abstract, claims) completing patents bibliographic data
GatherContent: True
OPSGatherContentsv2-Iramuteq: RequestIramuteq

#patents families extending the PU to families
GatherFamilly: RequestFamily

#NEW 2018: images
GatherImages: RequestImage

###############################
# Networks. Produce both online and for download and local use of Gephi
# Inventors' network 
InventorNetwork: RequestNetwork

# Applicants' network
ApplicantNetwork: RequestNetwork

# IPCs' network
CrossTechNetwork: RequestNetwork

# Applicants and Inventors network
ApplicantInventorNetwork: RequestNetwork

# Applicants and IPCs' network
ApplicantCrossTechNetwork: RequestNetwork

# Inventors and IPCs' network 
InventorCrossTechNetwork: RequestNetwork

# Countries and IPCs' network
CountryCrossTechNetwork: RequestNetwork

# Network of references for the PU (each reference cited by each patent within the PU, includes external bibliographic refs) 
ReferencesNetwork: RequestNetwork

# Network of citation for the PU (each patent cited within the PU cited in the rest of the patents world) 
CitationsTechNetwork: RequestNetwork

# Network of equivalent patents for each patent within the PU
EquivalentsTechNetwork: RequestNetwork

# The total network
CompleteNetwork: RequestNetwork

# Complete families network
FamiliesNetwork: RequestNetwork
FamiliesHierarchicNetwork: RequestNetwork

###############################
#  Mindmaps of IPCs both online and for download and local use of freeplane
P2N-FreePlane: RequestFreeplane

###############################
# export patents as a bibligraphic file in bibTex format
FormateExportBiblio: RequestBibfile

###############################
# Produce the world maps of inventors, applicants, deposit country
FormateExportAttractivityCartography: RequestMap
FormateExportCountryCartography: RequestMap

###############################
# Patents as a table
FormateExportDataTable: RequestTable
FormateExportDataTableFamilies: RequestTable

###############################
# Prepare interactive pivottable
FormateExportPivotTable: RequestTable

###############################
# prepare Abstracts, descriptions, claims for text analysis
# for download and local use of Carrot2 and Iramuteq
FusionCarrot2: RequestCarrot
FusionIramuteq2: RequestIramuteq

###############################
# NEW Feature (BETA)
# Double clustering system based on non so trivial words
P2N-Cluster: False

