git stash
git pull $@
python setup.py build
python setup.py install
python Patent2Net/extensions/Dlcarrot2.py /usr/src/P2N-V3
chown -R root:ftp carrot2.zip
chgrp -R ftp ./usr/src/P2N-V3/carrot2.zip
unzip carrot2.zip
chgrp -R ftp carrot2*
chmod +x update.sh
