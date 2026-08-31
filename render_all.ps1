# Configuring directories...
$projectRoot = "D:\tarangam-app"
$scriptDir = "$projectRoot\manim_scripts"
$outDir = "$projectRoot\assets\videos"

if (-not (Test-Path $outDir)) {
    Write-Host "Creating output directory: $outDir" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

Set-Location $projectRoot

# Defining the script list...
$scripts = @(
    "m1_08_multiple_regression.py",
    "m1_05_formulation.py",
    "m1_06_optimization.py",
    "m1_07_linear_regression.py",
    "m1_map.py",
    "m1_ml_vs_traditional.py",
    "m1_mle.py",
    "m1_mle_hill_climb.py",
    "m1_paradigms.py"
)

Write-Host "Starting batch render..." -ForegroundColor Green

# Looping through scripts and rendering...
foreach ($script in $scripts) {
    # Fixed missing newlines and spaces here
    $scriptPath = Join-Path $scriptDir $script
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($script)
    $finalVideoPath = Join-Path $outDir "$baseName.mp4"

    if (-not (Test-Path $scriptPath)) {
        Write-Host "[SKIPPED] Cannot find $scriptPath" -ForegroundColor Red
        continue
    }

    Write-Host ">>> RENDERING: $script" -ForegroundColor Cyan

    manim -qh $scriptPath

    $mediaFolder = "$projectRoot\media\videos\$baseName\1080p60"

    if (Test-Path $mediaFolder) {
        # Fixed missing space after -Path
        $mp4File = Get-ChildItem -Path $mediaFolder -Filter "*.mp4" | Select-Object -First 1
        
        if ($mp4File) {
            # Fixed missing space after -Destination
            Move-Item -Path $mp4File.FullName -Destination $finalVideoPath -Force
            Write-Host "[SUCCESS] Saved to: assets\videos\$baseName.mp4" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Rendered successfully, but .mp4 missing in $mediaFolder" -ForegroundColor Red
        }
    } else {
        Write-Host "[ERROR] Manim failed to render $script" -ForegroundColor Red
    }
}

Write-Host "Batch rendering complete!" -ForegroundColor Green