$files = Get-ChildItem -Path '.' -Filter '*.html' | Where-Object {
    $_.Name -ne 'blog-TEMPLATE.html' -and
    $_.Name -ne 'Mad Dog I.V Bar & Recovery Lounge.html'
}

$totalChanged = 0

# The bad CSS we injected previously
$badCSS = '<style>html{height:100%}body{min-height:100%;display:flex;flex-direction:column}main{flex:1 0 auto}footer.site-footer{flex-shrink:0}</style>'

foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $original = $c

    # Remove the bad flex footer CSS we injected
    $c = $c.Replace($badCSS, '')

    # Also remove the margin-top:auto rule that conflicts
    # and replace the existing footer CSS to use proper bottom positioning
    # The footer should just sit naturally at the bottom of content
    # Remove any margin-top:auto on footer that we may have left
    $c = [regex]::Replace($c, 'footer\.site-footer\{margin-top:auto !important\}', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

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
