#insert below your request in cql format as done in the example
#insert also a compliant name (no space or special characters) for 
#the "patents universe" corresponding to the request
request: lentille

###############################
# Name of files OR directories
DataDirectory: lentille

###############################
# Set next to *True* to collect patent list
GatherPatent: False

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
InventorNetwork: True

###############################
# Set it to *True* to produce the GUESS
ApplicantNetwork: True

###############################
# Set it to *True* to produce the GUESS
ApplicantInventorNet: True

###############################
# Set it to *True* to produce the GUESS
ApplicantCrossTechNetwork: True

###############################
# Set it to *True* to produce the GUESS
InventorCrossTechNetwork: True

###############################
# Set it to *True* to produce the GUESS
CompleteNetwork: True

###############################
# Set it to *True* to produce the GUESS
CountryCrossTechNetwork: True

###############################
# Set it to *True* to produce the GUESS
ReferencesNetwork: True

###############################
# Set it to *True* to produce the GUESS
CitationsTechNetwork: True

###############################
# Set it to *True* to produce the GUESS
EquivalentsTechNetwork: True



###############################
# Set it to *True* to produce the GUESS
FamiliesNetwork: True

###############################
# Set it to *True* to produce the GUESS
FamiliesHierarchicNetwork: True

###############################
# Should put here formating resulting switching option...