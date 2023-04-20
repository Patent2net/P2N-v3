#!/bin/bash
source /vpy3/bin/activate
find . -type d -name __pycache__ -exec rm -rf {} \;
cp dex.js dex.sav
cp dex.json dex.sav2
git stash
git pull $@
pip install -r requirements.txt
pip install -r requirements-release.txt
cd doc
sphinx-build -M html . _build
cd ..
python setup.py build
python setup.py install
chmod +x update.sh
chmod +x run-all.sh
cp -f dex.sav dex.js
cp -f dex.sav2 dex.json
rm dex.sav
rm dex.sav2

