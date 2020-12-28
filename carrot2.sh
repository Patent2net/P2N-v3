python Patent2Net/extensions/Dlcarrot2.py /usr/src/
cd ..
chown -R root:ftp carrot2.zip
chgrp -R ftp carrot2.zip
unzip carrot2.zip
chgrp -R ftp carrot2*
chmod -R 755 carrot2-4.0.4/dcs/dcs.sh
exec /usr/src/carrot2-4.0.4/dcs/dcs.sh &
