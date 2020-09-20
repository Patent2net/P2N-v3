$scriptPath = "REQ-P7"
$filename = Get-ChildItem (-join('..\', $scriptPath, '\'))
foreach ($f in $filename) {python PatentListFiltering.py (-join('..\', $scriptPath, '\',$f))}
foreach ($f in $filename) {python preProcessNormalisationNames.py (-join('..\', $scriptPath, '\',$f))}
foreach ($f in $filename) {python SplitCorpus2.py (-join('..\', $scriptPath, '\',$f))}