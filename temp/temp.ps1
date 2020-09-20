$scriptPath = "REQ-P7"
$filename = Get-ChildItem (-join('..\', $scriptPath, '\'))
foreach ($f in $filename) {(-join('..\', $scriptPath, '\',$f))}