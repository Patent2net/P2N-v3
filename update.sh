git stash
git pull $@
python setup.py build
python setup.py install
chmod +x update.sh
