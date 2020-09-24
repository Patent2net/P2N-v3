$Reps = "Req-P7","requests","requests2", "requests3"
foreach ($scriptPath in $Reps) {
	$scriptPath = (-join('..\', $scriptPath, '\'))
	echo $scriptPath
	$filename = Get-ChildItem ($scriptPath)
	foreach ($f in $filename) {python verifCorpora.py (-join($scriptPath,$f)) > (-join('verif', $f, 'txt'))}
	}