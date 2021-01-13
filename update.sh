cp dex.js dex.sav
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
rm dex.sav

