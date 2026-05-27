$files = Get-ChildItem -Path '.' -Filter '*.html' | Where-Object {
    $_.Name -ne 'blog-TEMPLATE.html' -and
    $_.Name -ne 'Mad Dog I.V Bar & Recovery Lounge.html'
}

$totalChanged = 0

foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $original = $c

    # Remove the edit-banner div (single line version)
    $c = [regex]::Replace($c, '<div class="edit-banner"[^>]*>[\s\S]*?</div>', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove save-banner div too
    $c = [regex]::Replace($c, '<div class="save-banner"[^>]*>[\s\S]*?</div>', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove standalone save button
    $c = [regex]::Replace($c, '<button[^>]*onclick="savePage\(\)"[^>]*>.*?</button>', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove save-page-btn button element
    $c = [regex]::Replace($c, '<button[^>]*id="save-page-btn"[^>]*>.*?</button>', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

    # Remove the style block that forces edit-banner to display:flex
    # Target the specific style block with edit-banner/save-banner flex rules
    $c = [regex]::Replace($c, '\.edit-banner,\.save-banner\{[^}]+\}', '.edit-banner,.save-banner{display:none!important}', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $c = [regex]::Replace($c, '\.edit-banner button,\.save-banner button\{[^}]+\}', '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

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
