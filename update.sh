#!/bin/bash
REPO_SITE='learn.pufna.com' 
APP_PATH='~/learn.pufna.com/'

cd $APP_PATH
echo "Run git pull"
git checkout .
git pull

echo "Run Pip Install"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
