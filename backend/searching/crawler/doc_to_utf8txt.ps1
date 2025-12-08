$ErrorActionPreference = 'Stop'
$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$path = 'C:\Users\admin\Desktop\RAGBOX\searching\crawler\22_VBHN-VPQH_651354.doc'
$out = 'C:\Users\admin\Desktop\RAGBOX\searching\crawler\22_VBHN-VPQH_651354.txt'
$doc = $wd.Documents.Open($path)
$text = $doc.Content.Text
$doc.Close()
$wd.Quit()
[System.IO.File]::WriteAllLines($out, $text -split "`r?`n", [System.Text.Encoding]::UTF8)
Write-Output "Wrote UTF8 text to: $out"
