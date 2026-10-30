param(
    [string]$InputMarkdown = "docs/ERD_33_BANG_POSTGRESQL.md",
    [string]$OutputSvg = "docs/ERD_33_BANG_POSTGRESQL.svg",
    [string]$OutputPng = "docs/ERD_33_BANG_POSTGRESQL.png"
)

$ErrorActionPreference = "Stop"

function Escape-Xml([string]$Value) {
    return [System.Security.SecurityElement]::Escape($Value)
}

$content = Get-Content -LiteralPath $InputMarkdown -Raw -Encoding UTF8
$match = [regex]::Match($content, '(?s)```mermaid\s*(erDiagram.*?)```')
if (-not $match.Success) {
    throw "Mermaid erDiagram block not found in $InputMarkdown"
}

$tables = [ordered]@{}
$relationships = [System.Collections.Generic.List[object]]::new()
$currentTable = $null

foreach ($rawLine in ($match.Groups[1].Value -split "`r?`n")) {
    $line = $rawLine.Trim()
    if (-not $line -or $line -eq "erDiagram") {
        continue
    }
    if ($line -match '^([A-Za-z0-9_]+)\s*\{$') {
        $currentTable = $Matches[1]
        $tables[$currentTable] = [System.Collections.Generic.List[object]]::new()
        continue
    }
    if ($line -eq '}') {
        $currentTable = $null
        continue
    }
    if ($null -ne $currentTable) {
        if ($line -match '^([A-Za-z0-9_]+)\s+([A-Za-z0-9_]+)(?:\s+(.+))?$') {
            $tables[$currentTable].Add([pscustomobject]@{
                Type = $Matches[1]
                Name = $Matches[2]
                Keys = if ($Matches.Count -ge 4) { $Matches[3] } else { "" }
            })
        }
        continue
    }
    if ($line -match '^([A-Za-z0-9_]+)\s+(\S+)\s+([A-Za-z0-9_]+)\s*:\s*(.+)$') {
        $relationships.Add([pscustomobject]@{
            Parent = $Matches[1]
            Cardinality = $Matches[2]
            Child = $Matches[3]
            Label = $Matches[4]
        })
    }
}

$modules = [ordered]@{
    Identity = @('roles', 'permissions', 'role_permissions', 'users', 'student_profiles')
    Housing = @('buildings', 'rooms', 'beds')
    Contracts = @('housing_applications', 'contracts', 'bed_assignments', 'room_transfer_requests', 'contract_events')
    Utilities = @('utilities', 'meters', 'utility_tariffs', 'tariff_tiers', 'utility_import_batches', 'meter_readings')
    Billing = @('bills', 'bill_items', 'payments')
    Violations = @('violation_types', 'violations', 'violation_evidences')
    Maintenance = @('maintenance_requests', 'maintenance_events', 'maintenance_plans')
    Notifications = @('notifications', 'notification_targets', 'notification_reads')
    Files = @('stored_files')
}

$moduleLane = @{
    Identity = 0
    Files = 0
    Housing = 1
    Contracts = 1
    Utilities = 2
    Billing = 3
    Violations = 3
    Maintenance = 4
    Notifications = 4
}

$moduleColors = @{
    Identity = '#2563eb'
    Housing = '#059669'
    Contracts = '#7c3aed'
    Utilities = '#0891b2'
    Billing = '#d97706'
    Violations = '#dc2626'
    Maintenance = '#4f46e5'
    Notifications = '#be185d'
    Files = '#475569'
}

$tableWidth = 510
$laneGap = 135
$leftMargin = 55
$topMargin = 75
$moduleTitleHeight = 30
$tableHeaderHeight = 31
$rowHeight = 19
$tablePaddingBottom = 9
$tableGap = 22
$moduleGap = 42
$positions = @{}
$laneY = @( $topMargin, $topMargin, $topMargin, $topMargin, $topMargin )
$moduleTitles = [System.Collections.Generic.List[object]]::new()

foreach ($moduleName in $modules.Keys) {
    $lane = $moduleLane[$moduleName]
    $x = $leftMargin + ($lane * ($tableWidth + $laneGap))
    $moduleTitles.Add([pscustomobject]@{ Module = $moduleName; X = $x; Y = $laneY[$lane] })
    $laneY[$lane] += $moduleTitleHeight
    foreach ($tableName in $modules[$moduleName]) {
        if (-not $tables.Contains($tableName)) {
            throw "Table $tableName does not exist in Mermaid"
        }
        $height = $tableHeaderHeight + ($tables[$tableName].Count * $rowHeight) + $tablePaddingBottom
        $positions[$tableName] = [pscustomobject]@{
            X = $x
            Y = $laneY[$lane]
            Width = $tableWidth
            Height = $height
            Module = $moduleName
        }
        $laneY[$lane] += $height + $tableGap
    }
    $laneY[$lane] += $moduleGap
}

$canvasWidth = $leftMargin * 2 + (5 * $tableWidth) + (4 * $laneGap)
$canvasHeight = ([Linq.Enumerable]::Max([int[]]$laneY)) + 45

$svg = [System.Text.StringBuilder]::new()
[void]$svg.AppendLine("<svg xmlns=`"http://www.w3.org/2000/svg`" width=`"$canvasWidth`" height=`"$canvasHeight`" viewBox=`"0 0 $canvasWidth $canvasHeight`">")
[void]$svg.AppendLine('<defs><filter id="shadow" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.14"/></filter><marker id="crow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" orient="auto"><path d="M1,1 L11,6 L1,11 M1,6 L11,6" fill="none" stroke="#64748b" stroke-width="1.2"/></marker></defs>')
[void]$svg.AppendLine('<rect width="100%" height="100%" fill="#f8fafc"/>')
[void]$svg.AppendLine('<text x="55" y="36" font-family="Segoe UI,Arial,sans-serif" font-size="23" font-weight="600" fill="#0f172a">Dormitory Management - PostgreSQL ERD (33 tables)</text>')
[void]$svg.AppendLine('<text x="55" y="58" font-family="Segoe UI,Arial,sans-serif" font-size="12" fill="#64748b">PK = Primary Key | FK = Foreign Key | UK = Unique Key | Alembic head 20260921_0009</text>')

# Draw relationships behind tables.
foreach ($rel in $relationships) {
    if (-not $positions.ContainsKey($rel.Parent) -or -not $positions.ContainsKey($rel.Child)) {
        continue
    }
    $p = $positions[$rel.Parent]
    $c = $positions[$rel.Child]
    $pCenterY = $p.Y + ($p.Height / 2)
    $cCenterY = $c.Y + ($c.Height / 2)
    if ($p.X -lt $c.X) {
        $x1 = $p.X + $p.Width
        $x2 = $c.X
        $bend = [Math]::Max(55, ($x2 - $x1) / 2)
        $d = "M $x1 $pCenterY C $($x1 + $bend) $pCenterY, $($x2 - $bend) $cCenterY, $x2 $cCenterY"
    } elseif ($p.X -gt $c.X) {
        $x1 = $p.X
        $x2 = $c.X + $c.Width
        $bend = [Math]::Max(55, ($x1 - $x2) / 2)
        $d = "M $x1 $pCenterY C $($x1 - $bend) $pCenterY, $($x2 + $bend) $cCenterY, $x2 $cCenterY"
    } else {
        $x1 = $p.X + $p.Width
        $x2 = $c.X + $c.Width
        $outsideX = $x1 + 42 + (($relationships.IndexOf($rel) % 4) * 10)
        $d = "M $x1 $pCenterY C $outsideX $pCenterY, $outsideX $cCenterY, $x2 $cCenterY"
    }
    [void]$svg.AppendLine("<path d=`"$d`" fill=`"none`" stroke=`"#94a3b8`" stroke-width=`"1.35`" opacity=`"0.72`" marker-end=`"url(#crow)`"/>")
}

foreach ($moduleTitle in $moduleTitles) {
    $color = $moduleColors[$moduleTitle.Module]
    $title = Escape-Xml $moduleTitle.Module
    [void]$svg.AppendLine("<text x=`"$($moduleTitle.X)`" y=`"$($moduleTitle.Y + 20)`" font-family=`"Segoe UI,Arial,sans-serif`" font-size=`"17`" font-weight=`"600`" fill=`"$color`">$title</text>")
}

foreach ($tableName in $tables.Keys) {
    if (-not $positions.ContainsKey($tableName)) {
        continue
    }
    $pos = $positions[$tableName]
    $color = $moduleColors[$pos.Module]
    [void]$svg.AppendLine("<g filter=`"url(#shadow)`">")
    [void]$svg.AppendLine("<rect x=`"$($pos.X)`" y=`"$($pos.Y)`" width=`"$($pos.Width)`" height=`"$($pos.Height)`" rx=`"4`" fill=`"#ffffff`" stroke=`"#cbd5e1`"/>")
    [void]$svg.AppendLine("<path d=`"M $($pos.X + 4) $($pos.Y) H $($pos.X + $pos.Width - 4) Q $($pos.X + $pos.Width) $($pos.Y) $($pos.X + $pos.Width) $($pos.Y + 4) V $($pos.Y + $tableHeaderHeight) H $($pos.X) V $($pos.Y + 4) Q $($pos.X) $($pos.Y) $($pos.X + 4) $($pos.Y)`" fill=`"$color`"/>")
    $escapedTable = Escape-Xml $tableName
    [void]$svg.AppendLine("<text x=`"$($pos.X + 12)`" y=`"$($pos.Y + 21)`" font-family=`"Consolas,Segoe UI,Arial,sans-serif`" font-size=`"14`" font-weight=`"600`" fill=`"#ffffff`">$escapedTable</text>")
    $rowIndex = 0
    foreach ($field in $tables[$tableName]) {
        $rowY = $pos.Y + $tableHeaderHeight + ($rowIndex * $rowHeight)
        if (($rowIndex % 2) -eq 1) {
            [void]$svg.AppendLine("<rect x=`"$($pos.X + 1)`" y=`"$rowY`" width=`"$($pos.Width - 2)`" height=`"$rowHeight`" fill=`"#f8fafc`"/>")
        }
        $keyText = Escape-Xml $field.Keys
        $typeText = Escape-Xml $field.Type
        $nameText = Escape-Xml $field.Name
        $keyColor = if ($field.Keys -match 'PK') { '#b45309' } elseif ($field.Keys -match 'FK') { '#7c3aed' } else { '#64748b' }
        [void]$svg.AppendLine("<text x=`"$($pos.X + 10)`" y=`"$($rowY + 14)`" font-family=`"Consolas,monospace`" font-size=`"11`" font-weight=`"600`" fill=`"$keyColor`">$keyText</text>")
        [void]$svg.AppendLine("<text x=`"$($pos.X + 76)`" y=`"$($rowY + 14)`" font-family=`"Consolas,monospace`" font-size=`"12`" fill=`"#0f172a`">$nameText</text>")
        [void]$svg.AppendLine("<text x=`"$($pos.X + $pos.Width - 10)`" y=`"$($rowY + 14)`" text-anchor=`"end`" font-family=`"Consolas,monospace`" font-size=`"11`" fill=`"#64748b`">$typeText</text>")
        $rowIndex++
    }
    [void]$svg.AppendLine('</g>')
}

[void]$svg.AppendLine('</svg>')
[System.IO.File]::WriteAllText((Join-Path (Get-Location) $OutputSvg), $svg.ToString(), [System.Text.UTF8Encoding]::new($false))

# Render a large PNG using System.Drawing for easy viewing in ordinary image viewers.
Add-Type -AssemblyName System.Drawing
$bitmap = [System.Drawing.Bitmap]::new($canvasWidth, $canvasHeight)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$graphics.Clear([System.Drawing.ColorTranslator]::FromHtml('#f8fafc'))

$titleFont = [System.Drawing.Font]::new('Segoe UI', 17, [System.Drawing.FontStyle]::Bold)
$subtitleFont = [System.Drawing.Font]::new('Segoe UI', 9)
$moduleFont = [System.Drawing.Font]::new('Segoe UI', 13, [System.Drawing.FontStyle]::Bold)
$headerFont = [System.Drawing.Font]::new('Consolas', 10, [System.Drawing.FontStyle]::Bold)
$fieldFont = [System.Drawing.Font]::new('Consolas', 8)
$keyFont = [System.Drawing.Font]::new('Consolas', 7, [System.Drawing.FontStyle]::Bold)
$darkBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#0f172a'))
$mutedBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#64748b'))
$whiteBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
$tableBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
$alternateBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#f8fafc'))
$borderPen = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#cbd5e1'), 1)
$relationPen = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#94a3b8'), 1.2)

$graphics.DrawString('Dormitory Management - PostgreSQL ERD (33 tables)', $titleFont, $darkBrush, 55, 13)
$graphics.DrawString('PK = Primary Key | FK = Foreign Key | UK = Unique Key | Alembic head 20260921_0009', $subtitleFont, $mutedBrush, 55, 43)

foreach ($rel in $relationships) {
    if (-not $positions.ContainsKey($rel.Parent) -or -not $positions.ContainsKey($rel.Child)) {
        continue
    }
    $p = $positions[$rel.Parent]
    $c = $positions[$rel.Child]
    $y1 = [single]($p.Y + ($p.Height / 2))
    $y2 = [single]($c.Y + ($c.Height / 2))
    if ($p.X -lt $c.X) {
        $x1 = [single]($p.X + $p.Width)
        $x2 = [single]$c.X
        $bend = [single][Math]::Max(55, ($x2 - $x1) / 2)
        $graphics.DrawBezier($relationPen, $x1, $y1, $x1 + $bend, $y1, $x2 - $bend, $y2, $x2, $y2)
    } elseif ($p.X -gt $c.X) {
        $x1 = [single]$p.X
        $x2 = [single]($c.X + $c.Width)
        $bend = [single][Math]::Max(55, ($x1 - $x2) / 2)
        $graphics.DrawBezier($relationPen, $x1, $y1, $x1 - $bend, $y1, $x2 + $bend, $y2, $x2, $y2)
    } else {
        $x1 = [single]($p.X + $p.Width)
        $x2 = [single]($c.X + $c.Width)
        $outsideX = [single]($x1 + 55)
        $graphics.DrawBezier($relationPen, $x1, $y1, $outsideX, $y1, $outsideX, $y2, $x2, $y2)
    }
}

foreach ($moduleTitle in $moduleTitles) {
    $moduleBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($moduleColors[$moduleTitle.Module]))
    $graphics.DrawString($moduleTitle.Module, $moduleFont, $moduleBrush, $moduleTitle.X, $moduleTitle.Y)
    $moduleBrush.Dispose()
}

foreach ($tableName in $tables.Keys) {
    if (-not $positions.ContainsKey($tableName)) {
        continue
    }
    $pos = $positions[$tableName]
    $headerBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($moduleColors[$pos.Module]))
    $graphics.FillRectangle($tableBrush, $pos.X, $pos.Y, $pos.Width, $pos.Height)
    $graphics.DrawRectangle($borderPen, $pos.X, $pos.Y, $pos.Width, $pos.Height)
    $graphics.FillRectangle($headerBrush, $pos.X, $pos.Y, $pos.Width, $tableHeaderHeight)
    $graphics.DrawString($tableName, $headerFont, $whiteBrush, $pos.X + 10, $pos.Y + 7)
    $rowIndex = 0
    foreach ($field in $tables[$tableName]) {
        $rowY = $pos.Y + $tableHeaderHeight + ($rowIndex * $rowHeight)
        if (($rowIndex % 2) -eq 1) {
            $graphics.FillRectangle($alternateBrush, $pos.X + 1, $rowY, $pos.Width - 2, $rowHeight)
        }
        $keyBrush = if ($field.Keys -match 'PK') {
            [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#b45309'))
        } elseif ($field.Keys -match 'FK') {
            [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#7c3aed'))
        } else {
            [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#64748b'))
        }
        $graphics.DrawString($field.Keys, $keyFont, $keyBrush, $pos.X + 8, $rowY + 4)
        $graphics.DrawString($field.Name, $fieldFont, $darkBrush, $pos.X + 74, $rowY + 3)
        $typeSize = $graphics.MeasureString($field.Type, $fieldFont)
        $graphics.DrawString($field.Type, $fieldFont, $mutedBrush, $pos.X + $pos.Width - $typeSize.Width - 8, $rowY + 3)
        $keyBrush.Dispose()
        $rowIndex++
    }
    $headerBrush.Dispose()
}

$bitmap.Save((Join-Path (Get-Location) $OutputPng), [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bitmap.Dispose()
$titleFont.Dispose()
$subtitleFont.Dispose()
$moduleFont.Dispose()
$headerFont.Dispose()
$fieldFont.Dispose()
$keyFont.Dispose()
$darkBrush.Dispose()
$mutedBrush.Dispose()
$whiteBrush.Dispose()
$tableBrush.Dispose()
$alternateBrush.Dispose()
$borderPen.Dispose()
$relationPen.Dispose()

Write-Output "Rendered $($tables.Count) tables and $($relationships.Count) relationships."
Write-Output "SVG: $OutputSvg"
Write-Output "PNG: $OutputPng"
