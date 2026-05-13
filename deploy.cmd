@echo off
REM One-command deploy: commits, pushes, deploys to Cloudflare Pages,
REM then archives the now-live index.html to OneDrive.
REM
REM Usage:
REM   deploy "commit message"   - commit, push, deploy, archive
REM   deploy                    - deploy current state without committing, archive

setlocal enabledelayedexpansion

if not "%~1"=="" (
  echo [1/4] Committing changes...
  git add .
  git commit -m "%~1"
  echo.
  echo [2/4] Pushing to GitHub...
  git push
  echo.
  echo [3/4] Deploying to Cloudflare Pages...
) else (
  echo [1/2] Deploying current state to Cloudflare Pages ^(no commit^)...
)

call wrangler pages deploy . --project-name=ryoticoalu --commit-dirty=true
if errorlevel 1 (
  echo.
  echo Deploy failed - skipping OneDrive archive.
  exit /b 1
)

REM === Archive the now-live index.html to OneDrive ===
REM Per Ryo's rule: save live versions only, never drafts.
REM Path:   %USERPROFILE%\OneDrive\Documents\Personal\CV\Portfolio Website
REM Format: Website - Portfolio (DD-MM-YY HH-MM).html

echo.
if not "%~1"=="" (
  echo [4/4] Archiving live version to OneDrive...
) else (
  echo [2/2] Archiving live version to OneDrive...
)

for /f "delims=" %%I in ('powershell -NoProfile -Command "Get-Date -Format 'dd-MM-yy HH-mm'"') do set "ts=%%I"
set "od=%USERPROFILE%\OneDrive\Documents\Personal\CV\Portfolio Website"
if not exist "%od%" mkdir "%od%"
copy /Y index.html "%od%\Website - Portfolio (!ts!).html" >nul
if errorlevel 1 (
  echo WARN: OneDrive archive failed. Live deploy succeeded - check OneDrive sync.
) else (
  echo Archived: %od%\Website - Portfolio ^(!ts!^).html
)

endlocal
