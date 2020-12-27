git stash
git pull $@
chmod +x update.sh
python setup.py build
python setup.py install
