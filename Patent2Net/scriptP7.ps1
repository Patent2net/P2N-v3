# directory containing requests files

$Reps = "requests2", "requests3", "requests1", "REQ-P7"

# processing networks and reseting the whole interface

foreach ($scriptPath in $Reps) {
	$scriptPath = (-join('..\', $scriptPath, '\'))
	echo $scriptPath
	$filename = Get-ChildItem ($scriptPath)
    #foreach ($f in $filename) {foreach ($app in (Get-Content .\scriptlist.txt)) {python $app --config=(-join($scriptPath,$f))}}
	foreach ($f in $filename) {foreach ($app in ("AcadNNets.py", "Interface2.py")) {python $app --config=(-join($scriptPath,$f))}}
	}