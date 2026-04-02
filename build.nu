# 1. Define variables
let dest_dir = "build"
let items_to_copy = ["cleneshade", "interp.py"]

# 2. Create build directory if it doesn't exist
if not ($dest_dir | path exists) {
    mkdir $dest_dir
}

# 3. Copy items
for item in $items_to_copy {
    if ($item | path exists) {
        cp -r $item $dest_dir
    } else {
        print $"Warning: ($item) not found."
    }
}

# 4. Create clenec.bat (Windows)
# We use a raw string (single quotes) so %~dp0 isn't touched by Nu
"@echo off
python \"%~dp0interp.py\" %*
" | save -f ([$dest_dir, "clenec.bat"] | path join)

# 5. Create clenec.sh (Linux/macOS)
# Again, single quotes ensure the bash variables ($0, $@) are saved literally
'#!/bin/bash
python3 "$(dirname "$0")/interp.py" "$@"
' | save -f ([$dest_dir, "clenec.sh"] | path join)

print "Build complete: launcher scripts generated in build/ folder."