# script to filter and normalize name. P2N do these steps alone now. Corpora spliter is then called

$Reps = "REQ-P7"
$scriptPath = (-join('..\', $Reps))
$filename = Get-ChildItem ($scriptPath)
# foreach ($f in $filename) {python PatentListFiltering.py (-join('..\', $scriptPath, '\',$f))}
# foreach ($f in $filename) {python preProcessNormalisationNames.py (-join('..\', $scriptPath, '\',$f))}
# next is needed to generate publication auctoriality and affiliation
# wil be launched again after corpora splitting for sub corporas
foreach ($f in $filename) {python AcadStatsSuiteDer.py (-join($scriptPath, '\',$f))}
foreach ($f in $filename) {python SplitCorpus2.py (-join($scriptPath, '\',$f))}
