(CALL conda update --yes -n base -c defaults conda
CALL conda create --yes --name P2N2 python=3.6
CALL InstallWindows.bat 2> LogInstall1.txt
CALL InstallWindows2.bat 2> LogInstall2.txt
CALL conda activate P2N && python setup.py install > LogInstallP2N.txt
)

