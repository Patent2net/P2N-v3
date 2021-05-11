# Patent2Net V3 configuration file
##############################
# request
# insert below your request in cql format as done in the example
request: (TA="neural net" OR TA="machine learning" OR CPC=G06N) AND PN=WO AND PD=202105

##############################
# Directory to use
# insert a compliant name (no space or special characters) for the "Patent Universe" (PU)
DataDirectory: autom2_segments_202105

###############################
#Patent2Net options : Set to *True* or False
###############################
# Collecting
# patents list corresponding to the request. e.g the "Patent Universe" (PU)
GatherPatent: True

# patents bibliographic data corresponding to patent list
GatherBiblio: False

# patent content (description, abstract, claims) completing patents bibliographic data
GatherContent: False
OPSGatherContentsv2-Iramuteq: False

#patents families extending the PU to families
GatherFamilly: False

#NEW 2018: images
GatherImages: False

###############################
# Networks. Produce both online and for download and local use of Gephi
# Inventors' network 
InventorNetwork: False

# Applicants' network
ApplicantNetwork: False

# IPCs' network
CrossTechNetwork: False

# Applicants and Inventors network
ApplicantInventorNetwork: False

# Applicants and IPCs' network
ApplicantCrossTechNetwork: False

# Inventors and IPCs' network 
InventorCrossTechNetwork: False

# Countries and IPCs' network
CountryCrossTechNetwork: False

# Network of references for the PU (each reference cited by each patent within the PU, includes external bibliographic refs) 
ReferencesNetwork: False

# Network of citation for the PU (each patent cited within the PU cited in the rest of the patents world) 
CitationsTechNetwork: False

# Network of equivalent patents for each patent within the PU
EquivalentsTechNetwork: False

# The total network
CompleteNetwork: False

# Complete families network
FamiliesNetwork: False
FamiliesHierarchicNetwork: False

###############################
#  Mindmaps of IPCs both online and for download and local use of freeplane
P2N-FreePlane: False

###############################
# export patents as a bibligraphic file in bibTex format
FormateExportBiblio: False

###############################
# Produce the world maps of inventors, applicants, deposit country
FormateExportAttractivityCartography: False
FormateExportCountryCartography: False

###############################
# Patents as a table
FormateExportDataTable: False
FormateExportDataTableFamilies: False

###############################
# Prepare interactive pivottable
FormateExportPivotTable: False

###############################
# prepare Abstracts, descriptions, claims for text analysis
# for download and local use of Carrot2 and Iramuteq
FusionCarrot2: False
FusionIramuteq2: False

###############################
# NEW Feature (BETA)
# Double clustering system based on non so trivial words
P2N-Cluster: False

