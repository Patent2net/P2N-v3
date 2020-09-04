#insert below your request in cql format as done in the example
#insert also a compliant name (no space or special characters) for 
#the "patents universe" corresponding to the request
request: ***requete***
###############################
# Name of files OR directories
DataDirectory: ***dataDir***

###############################
# Set next to *True* to collect patent list
GatherPatent: True

###############################
# Set it to *True* to collect patent bibliographic data
GatherBiblio: False

###############################
# Set it to *True* to collect patent content (description, abstract, claims)
GatherContent: False

###############################
# Set it to *True* to collect patent families
GatherFamilly: False

###############################
# Set it to *True* to produce the Inventors' network 
InventorNetwork: False

###############################
# Set it to *True* to produce the GUESS
ApplicantNetwork: False

###############################
# Set it to *True* to produce the GUESS
ApplicantInventorNet: False

###############################
# Set it to *True* to produce the GUESS
ApplicantCrossTechNetwork: False

###############################
# Set it to *True* to produce the GUESS
InventorCrossTechNetwork: False

###############################
# Set it to *True* to produce the GUESS
CrossTechNetwork: False

###############################
# Set it to *True* to produce the GUESS
CompleteNetwork: False

###############################
# Set it to *True* to produce the GUESS
CountryCrossTechNetwork: False

###############################
# Set it to *True* to produce the GUESS
ReferencesNetwork: False

###############################
# Set it to *True* to produce the GUESS
CitationsTechNetwork: False

###############################
# Set it to *True* to produce the GUESS
EquivalentsTechNetwork: False
###############################
# Set it to *True* to produce the GUESS
FamiliesNetwork: False

###############################
# Set it to *True* to produce the GUESS
FamiliesHierarchicNetwork: False

###############################
# Should put here formating resulting switching option...