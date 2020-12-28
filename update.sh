git stash
git pull $@
python setup.py build
python setup.py install
python Patent2Net/extensions/Dlcarrot2.py /usr/src/
chown -R root:ftp carrot2.zip
chgrp -R ftp carrot2.zip
unzip carrot2.zip
chgrp -R ftp carrot2*
chmod -R 755 carrot2-4.0.4/dcs/dcs.sh
exec /usr/src/P2N-V3/carrot2-4.0.4/dcs/dcs.sh &
chmod +x update.sh
