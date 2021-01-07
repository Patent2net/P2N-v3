$Reps = "requests3", "request2", "request", "REQ-P7"
foreach ($scriptPath in $Reps) {
	$scriptPath = (-join('..\', $scriptPath, '\'))
	echo $scriptPath
	$filename = Get-ChildItem ($scriptPath)
    #foreach ($f in $filename) {python AcadStatsSuiteDer.py (-join($scriptPath,$f))}
	foreach ($f in $filename) {python P2N-Nets.py (-join($scriptPath,$f))}
	foreach ($f in $filename) {foreach ($app in (Get-Content .\scriptlist.txt)) {python $app --config=(-join($scriptPath,$f))}}
}