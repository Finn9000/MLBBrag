# Creates a dated snapshot of MLBB.GG's public Mythic rank tier list.
# Run from the project root: .\scripts\scrape_mlbb_tierlist.ps1

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$dataDirectory = Join-Path $projectRoot "data"
$sourceUrl = "https://mlbb.gg/tierlist"

# One page request: the public HTML contains the rendered Mythic tier-list data.
$content = (Invoke-WebRequest -Uri $sourceUrl -UseBasicParsing).Content

$marker = '\"tierListData\":'
$markerIndex = $content.IndexOf($marker)
if ($markerIndex -lt 0) {
    throw "Could not find tier-list data in the page response."
}

# The Next.js page data is JSON escaped inside the HTML response.
$payload = $content.Substring($markerIndex + $marker.Length)
$payload = $payload -replace '\\"', '"'
$objectStart = $payload.IndexOf('{')

if ($objectStart -lt 0) {
    throw "Could not find the start of the tier-list data."
}

# Find the closing brace while respecting quoted strings in JSON.
$depth = 0
$inString = $false
$escaped = $false
$objectEnd = -1

for ($index = $objectStart; $index -lt $payload.Length; $index++) {
    $character = $payload[$index]

    if ($inString) {
        if ($escaped) {
            $escaped = $false
        }
        elseif ($character -eq '\') {
            $escaped = $true
        }
        elseif ($character -eq '"') {
            $inString = $false
        }
    }
    else {
        if ($character -eq '"') {
            $inString = $true
        }
        elseif ($character -eq '{') {
            $depth++
        }
        elseif ($character -eq '}') {
            $depth--
            if ($depth -eq 0) {
                $objectEnd = $index
                break
            }
        }
    }
}

if ($objectEnd -lt 0) {
    throw "The tier-list data was incomplete."
}

$tierList = $payload.Substring($objectStart, $objectEnd - $objectStart + 1) |
    ConvertFrom-Json

$retrievedAt = Get-Date -Format "yyyy-MM-dd"
$rows = foreach ($tierGroup in $tierList.data) {
    foreach ($entry in $tierGroup.data) {
        $mainRole = ($entry.hero.lanes |
            Where-Object { $_.is_main } |
            Select-Object -ExpandProperty name) -join "; "

        $secondaryRoles = ($entry.hero.lanes |
            Where-Object { -not $_.is_main } |
            Select-Object -ExpandProperty name) -join "; "

        $document = @"
MLBB tier-list snapshot
Hero: $($entry.hero.name)
Tier: $($tierGroup.tier)
Main role: $mainRole
Secondary roles: $secondaryRoles
Rank: Mythic
Mode: Rank
Movement: $($entry.movement)
Source: MLBB.GG
Source updated: $($tierList.updated_at)
Retrieved: $retrievedAt
"@.Trim()

        [PSCustomObject]@{
            hero_id         = $entry.hero.id
            hero_name       = $entry.hero.name
            tier            = $tierGroup.tier
            movement        = $entry.movement
            main_role       = $mainRole
            secondary_roles = $secondaryRoles
            rank            = "Mythic"
            mode            = "Rank"
            source          = "MLBB.GG"
            source_url      = $sourceUrl
            updated_at      = $tierList.updated_at
            retrieved_at    = $retrievedAt
            document        = $document
        }
    }
}

$outputPath = Join-Path $dataDirectory "mlbb_tierlist_mythic_$($tierList.updated_at).csv"
$rows | Export-Csv -LiteralPath $outputPath -NoTypeInformation -Encoding utf8

Write-Host "Saved $($rows.Count) tier-list records to: $outputPath"
Write-Host "Source update date: $($tierList.updated_at)"
Write-Host "Tier counts: $(($rows | Group-Object tier | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ', ')"
