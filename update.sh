source /vpy3/bin/activate
find . -type d -name __pycache__ -exec rm -rf {} \;
pip install -r requirements.txt
pip install -r requirements-release.txt
cp dex.js dex.sav
cp dex.json dex.sav2
git stash
git pull $@
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
cp Patent2Net/Carrot2/main.4974e0c5.chunk.js /home/p2n/carrot2/carrot2-4.2.1/dcs/web/frontend/static/js


