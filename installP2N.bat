conda create --name P2N python=3.6 & call Patent2Net\InstallWindows.bat 2> LogInstall1.txt & call Patent2Net\InstallWindows2.bat 2> LogInstall2.txt & conda activate P2N & python setup.py install > LogInstallP2N.txt

