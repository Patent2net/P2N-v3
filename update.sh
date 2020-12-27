git stash
git pull $@
python setup.py build
python setup.py install
python dlcarrot2.py /usr/src
chmod +x update.sh
