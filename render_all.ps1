=====================================================================Tarangam Manim Batch RendererRun this from your D:\tarangam-app\ folder in PowerShell=====================================================================$projectRoot = "D:\tarangam-app"$scriptDir = "$projectRoot\manim_scripts"$outDir = "$projectRoot\assets\videos"1. Create the assets/videos directory if it doesn't exist yetif (-not (Test-Path $outDir)) {Write-Host "Creating output directory: $outDir" -ForegroundColor CyanNew-Item -ItemType Directory -Force -Path $outDir | Out-Null}2. Set working directory to project root so Manim outputs the 'media' folder hereSet-Location $projectRoot3. Define the exact list of files you want to render$scripts = @("m1_05_formulation.py","m1_06_optimization.py","m1_07_linear_regression.py","m1_08_multiple_regression.py","m1_map.py","m1_ml_vs_traditional.py","m1_mle.py","m1_mle_hill_climb.py","m1_paradigms.py")Write-Host "Starting batch render for $($scripts.Length) videos..." -ForegroundColor GreenWrite-Host "Target quality: 1080p 60fps (-qh)" -ForegroundColor GreenWrite-Host "====================================================`n"4. Loop through each file and renderforeach ($script in $scripts) {$scriptPath = Join-Path $scriptDir $script$baseName = [System.IO.Path]::GetFileNameWithoutExtension($script)$finalVideoPath = Join-Path $outDir "$baseName.mp4"if (-not (Test-Path $scriptPath)) {
    Write-Host "[SKIPPED] Cannot find $scriptPath" -ForegroundColor Red
    continue
}

Write-Host ">>> RENDERING: $script" -ForegroundColor Cyan

# Run Manim high-quality command. 
# (Since there is only one class/scene per file, Manim automatically selects it)
manim -qh $scriptPath

# Manim defaults to saving files deep inside: media/videos/<filename>/1080p60/
$mediaFolder = "$projectRoot\media\videos\$baseName\1080p60"

if (Test-Path $mediaFolder) {
    # Find the generated mp4 inside the 1080p60 folder
    $mp4File = Get-ChildItem -Path $mediaFolder -Filter "*.mp4" | Select-Object -First 1
    
    if ($mp4File) {
        # Move and rename it directly to our assets/videos folder
        Move-Item -Path $mp4File.FullName -Destination $finalVideoPath -Force
        Write-Host "[SUCCESS] Saved to: assets\videos\$baseName.mp4`n" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Rendered successfully, but couldn't find the .mp4 in $mediaFolder`n" -ForegroundColor Red
    }
} else {
    Write-Host "[ERROR] Manim failed to render $script (Folder not found: $mediaFolder)`n" -ForegroundColor Red
}
}Write-Host "===================================================="Write-Host "Batch rendering complete! All videos are in assets/videos/" -ForegroundColor Green