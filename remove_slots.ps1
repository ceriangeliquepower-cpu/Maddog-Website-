$files = Get-ChildItem -Path '.' -Filter '*.html' | Where-Object {
    $_.Name -ne 'blog-TEMPLATE.html' -and
    $_.Name -ne 'Mad Dog I.V Bar & Recovery Lounge.html'
}

$totalChanged = 0

foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $original = $c

    # Remove slot-overlay divs (with any content inside)
    $c = [regex]::Replace($c, '<div class="slot-overlay"[^>]*>[\s\S]*?</div>', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove slot-hint divs
    $c = [regex]::Replace($c, '<div class="slot-hint"[^>]*>[\s\S]*?</div>', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove gc corner marker divs (self-closing style: <div class="gc tl"></div>)
    $c = [regex]::Replace($c, '<div class="gc[^"]*"></div>', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove onclick="swapPhoto(...)" from photo slots
    $c = [regex]::Replace($c, '\s*onclick="swapPhoto\([^)]*\)"', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove cursor:pointer from photo-slot CSS (make slots non-interactive)
    $c = $c.Replace('.photo-slot{position:relative;overflow:hidden;cursor:pointer;', '.photo-slot{position:relative;overflow:hidden;cursor:default;')

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
