@echo off
REM One-command deploy: commits, pushes, deploys to Cloudflare Pages.
REM Usage:
REM   deploy "commit message"   - commit, push, deploy
REM   deploy                    - deploy current state without committing

setlocal

if not "%~1"=="" (
  echo [1/3] Committing changes...
  git add .
  git commit -m "%~1"
  echo.
  echo [2/3] Pushing to GitHub...
  git push
  echo.
  echo [3/3] Deploying to Cloudflare Pages...
) else (
  echo Deploying current state to Cloudflare Pages ^(no commit^)...
)

wrangler pages deploy . --project-name=ryoticoalu --commit-dirty=true

endlocal
