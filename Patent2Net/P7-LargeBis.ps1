$scriptPath = "P7-LargeBis.cql"
python PatentListFiltering.py (-join('..\REQ-P7\', $scriptPath))
python preProcessNormalisationNames.py (-join('..\REQ-P7\', $scriptPath))
python SplitCorpus2.py (-join('..\REQ-P7\', $scriptPath))