# Define paths
$destDir = "build"
$itemsToCopy = @("cleneshade", "interp.py")

# 1. Create the build directory if it doesn't exist
if (!(Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir | Out-Null
}

# 2. Copy the folder and python script
foreach ($item in $itemsToCopy) {
    if (Test-Path $item) {
        Copy-Item -Path $item -Destination $destDir -Recurse -Force
    }
}

# 3. Create clenec.bat (Windows)
$batContent = @"
@echo off
python "%~dp0interp.py" %*
"@
$batContent | Out-File -FilePath "$destDir\clenec.bat" -Encoding ascii

# 4. Create clenec.sh (Linux/macOS) 
# Note: We use `$($)` to escape the dollar signs so PowerShell doesn't try to run 'dirname'
$shContent = @"
#!/bin/bash
python3 "`$(dirname "`$0")/interp.py" "`$@"
"@
$shContent | Out-File -FilePath "$destDir\clenec.sh" -Encoding ascii

Write-Host "Build complete: Files copied and launchers created correctly." -ForegroundColor Green