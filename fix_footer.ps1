$files = Get-ChildItem -Path '.' -Filter '*.html' | Where-Object {
    $_.Name -ne 'blog-TEMPLATE.html' -and
    $_.Name -ne 'Mad Dog I.V Bar & Recovery Lounge.html'
}

$totalChanged = 0
$footerCSS = '<style>html{height:100%}body{min-height:100%;display:flex;flex-direction:column}main{flex:1 0 auto}footer.site-footer{flex-shrink:0}</style>'

foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $original = $c

    # Only add if not already present
    if ($c -notmatch 'flex-shrink:0.*site-footer|site-footer.*flex-shrink') {
        $c = $c.Replace('</head>', $footerCSS + '</head>')
    }

    if ($c -ne $original) {
        [System.IO.File]::WriteAllText($f.FullName, $c, [System.Text.Encoding]::UTF8)
        Write-Output ("UPDATED: " + $f.Name)
        $totalChanged++
    } else {
        Write-Output ("NO CHANGE: " + $f.Name)
    }
}

Write-Output ""
Write-Output ("Total pages updated: " + $totalChanged)
