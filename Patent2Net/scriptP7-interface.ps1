$Reps = "requests3", "requests2", "requests", "REQ-P7"
foreach ($scriptPath in $Reps) {
	$scriptPath = (-join('..\', $scriptPath, '\'))
	echo $scriptPath
	$filename = Get-ChildItem ($scriptPath)
	foreach ($f in $filename) {python Interface2.py (-join($scriptPath,$f))}
	}
