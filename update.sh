git stash
git pull $@
python setup.py build
python setup.py install
python Patent2Net/extensions/Dlcarrot2.py /usr/src/P2N-V3
chmod +x update.sh
