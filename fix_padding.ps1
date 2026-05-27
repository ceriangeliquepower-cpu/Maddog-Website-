$files = Get-ChildItem -Path '.' -Filter '*.html' | Where-Object {
    $_.Name -ne 'blog-TEMPLATE.html' -and
    $_.Name -ne 'Mad Dog I.V Bar & Recovery Lounge.html'
}

$totalChanged = 0

foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $original = $c

    # Remove padding-bottom from body rule that was for save bar
    $c = [regex]::Replace($c, 'body\s*\{[^}]*min-height:100vh[^}]*padding-bottom:44px[^}]*\}', 'body{min-height:100vh}', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove the env(safe-area-inset-bottom) padding from body in media queries
    $c = [regex]::Replace($c, 'padding-bottom:\s*env\(safe-area-inset-bottom[^)]*\)\s*!important\s*;', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove standalone padding-bottom:44px on body
    $c = [regex]::Replace($c, '(body\s*\{[^}]*)padding-bottom:\s*44px\s*;?([^}]*\})', '$1$2', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove display:flex;flex-direction:column from body (leftover from old save bar JS)
    $c = [regex]::Replace($c, '(body\s*\{[^}]*)display:flex;\s*flex-direction:column;\s*([^}]*\})', '$1$2', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

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
