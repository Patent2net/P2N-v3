python Patent2Net/extensions/Dlcarrot2.py /usr/src/
cd ..
chown -R root:ftp carrot2.zip
chgrp -R ftp carrot2.zip
unzip -o carrot2.zip -d carrot2
chgrp -R ftp carrot2*
chmod -R 755 carrot2/carrot2-4.0.4/dcs/dcs.sh
exec /usr/src/carrot2/carrot2-4.0.4/dcs/dcs.sh --port 8000 &
cd P2N-V3
