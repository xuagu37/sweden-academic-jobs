#!/bin/bash

set -e  # Exit on error

echo "Cleaning previous Sphinx build..."
bash scripts/build_clean.sh

echo "Committing updated source files to Git..."
git add .
git commit -m "Update content" || echo "No changes to commit."

echo "Pushing to main branch (triggers GitHub Pages build via Actions)..."
git push origin main

echo "Deployment triggered. Check progress at:"
echo "   https://github.com/xuagu37/sweden-academic-jobs/actions"
echo "And visit the site at:"
echo "   https://xuagu37.github.io/sweden-academic-jobs/"
