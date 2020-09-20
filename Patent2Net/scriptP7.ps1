$Reps = "temp"
foreach ($scriptPath in $Reps) {
	$scriptPath = (-join('..\', $scriptPath, '\'))
	echo $scriptPath
	$filename = Get-ChildItem ($scriptPath)
	foreach ($f in $filename) {python AnalyseReseaux2.py (-join($scriptPath,$f))}
	
	foreach ($f in $filename) {foreach ($app in (Get-Content .\scriptlist.txt)) {python $app --config=(-join($scriptPath,$f))}}
	}