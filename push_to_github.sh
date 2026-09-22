#!/bin/bash

git config user.name "Jujita Fermin Stairs"
git config user.email "jujitastairs@gmail.com"

echo "================================================================================"
echo " 🚀 PREPARING INITIAL GITHUB COMMIT & PUSH"
echo "================================================================================"

# Create clean .gitignore for build artifacts and local databases
cat << 'GITIGNORE' > .gitignore
tax_audit_log.db
audit_export_*.csv
audit_export_*.json
*.bak
.gradle/
build/
__pycache__/
GITIGNORE

# Stage python scripts, xml templates, ignore rules, and shell scripts
git add *.py *.xml *.sh *.json *.html .gitignore 2>/dev/null

echo "Staged files for initial commit:"
git status --short

echo "--------------------------------------------------------------------------------"
# Create initial commit
git commit -m "feat(core): initial commit for edge tax audit engine and sha-256 verification framework"

# Ensure branch is named main and push upstream
git branch -M main
echo "Pushing updates to GitHub..."
git push -u origin main

echo "================================================================================"
echo " SUCCESS: GitHub repository initialized and updated."
echo "================================================================================"
