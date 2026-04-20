# Biber Infrastructure Fix (Apple Silicon)

*Created: 2026-04-20 12:36:54 IST*
*Status: ✅ Resolved*

## Issue
Empty `.bbl` file generated during LaTeX compilation on Apple Silicon (M1/M2/M3 Macs).

## Root Cause
MiKTeX's x86_64 biber symlink at `/usr/local/bin/biber` was crashing silently under Rosetta translation on Apple Silicon, producing an empty `.bbl` file.

## Solution
Removed the MiKTeX x86_64 biber symlink, allowing the homebrew arm64 biber at `/opt/homebrew/bin/biber` to take precedence in the PATH.

## Technical Details
- **Platform**: macOS Apple Silicon (M-series chips)
- **Conflict**: MiKTeX (x86_64) vs Homebrew (arm64 native) biber installations
- **Mechanism**: Rosetta 2 translation was causing silent crashes for x86_64 biber
- **Resolution**: Prefer native arm64 biber from Homebrew over emulated x86_64 version

## Future Reference
When setting up LaTeX environments on Apple Silicon:
1. Prefer native arm64 packages (Homebrew) over x86_64 packages (MiKTeX)
2. Check PATH ordering to ensure native binaries take precedence
3. Verify biber version with `biber --version` after installation
