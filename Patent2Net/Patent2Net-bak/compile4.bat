rmdir /S /Q ..\distribution\Patent2Net

pyinstaller -p .  --workpath=..\tempocomp --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-FormateExportAttractivityCartography.txt FormateExportAttractivityCartography.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-OPSGatherPatentsv2.txt OPSGatherPatentsv2.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherContentsV2-Iramuteq.txt OPSGatherContentsV2-Iramuteq.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherContentsV2-Images.txt OPSGatherContentsV2-Images.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherAugment-Families.txt OPSGatherAugment-Families.py
REM pyinstaller -p . -y --noupx --version-file=version-Compatibilizer.txt Compatibilizer.py

pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-Networks.txt P2N-Networks.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-PreNetworks.txt P2N-PreNetworks.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-NetworksJS.txt P2N-NetworksJS.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionImages.txt FusionImages.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionIramuteq2.txt FusionIramuteq2.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Fusion.txt Fusion.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-FreePlane.txt P2N-FreePlane.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTable.txt FormateExportDataTable.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportPivotTable.txt FormateExportPivotTable.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTableFamilies.txt FormateExportDataTableFamilies.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportBiblio.txt FormateExportBiblio.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportCountryCartography.txt FormateExportCountryCartography.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionCarrot2.txt FusionCarrot2.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Interface2.txt Interface2.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Parallel3.txt Parallel3.py

pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --clean --version-file=version-IPC-Abstracts-Augment.txt IPC-Abstracts-Augment.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --clean --hidden-import sklearn.neighbors.typedefs --version-file=version-P2N-ClusterPreProcess.txt ClusterPreProcess.py
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --hidden-import sklearn.neighbors.typedefs --clean --version-file=version-P2N-Cluster.txt P2N-Cluster.py


rmdir /S /Q  ..\tempocomp\FormateExportAttractivityCartography\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\OPSGatherPatentsv2\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\OPSGatherContentsv2-Iramuteq\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\OPSGatherAugment-Families\setuptools-19.2-py2.7.egg
REM rmdir /S /Q   ..\tempocomp\Compatibilizer\setuptools-19.2-py2.7.egg


rmdir /S /Q  ..\tempocomp\P2N-Networks\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\P2N-Networks\pydot_ng-1.0.1.dev0-py2.7.egg
rmdir /S /Q   ..\tempocomp\P2N-PreNetworks\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\P2N-PreNetworks\pydot_ng-1.0.1.dev0-py2.7.egg
rmdir /S /Q  ..\tempocomp\P2N-NetworksJS\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\P2N-NetworksJS\pydot_ng-1.0.1.dev0-py2.7.egg

rmdir /S /Q  ..\tempocomp\FusionIramuteq2\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\Fusion\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\P2N-FreePlane\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportDataTable\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\FormateExportPivotTable\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportDataTableFamilies\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportBiblio\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportCountryCartography\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\FusionCarrot2\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\Interface2\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\Parallel3\setuptools-19.2-py2.7.egg


REM xcopy /S /Y ..\distribution\P2N-FamiliesHierarc ..\distribution\Patent2Net\

pyinstaller -p .  --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-FormateExportAttractivityCartography.txt ..\specs\FormateExportAttractivityCartography.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-OPSGatherPatentsv2.txt ..\specs\OPSGatherPatentsv2.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherContentsV2-Images.txt ..\specs\OPSGatherContentsV2-Images.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherContentsV2-Iramuteq.txt ..\specs\OPSGatherContentsV2-Iramuteq.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherAugment-Families.txt ..\specs\OPSGatherAugment-Families.spec
REM pyinstaller -p . -y --noupx --version-file=version-Compatibilizer.txt ..\specs\Compatibilizer.spec

pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-Networks.txt ..\specs\P2N-Networks.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-PreNetworks.txt ..\specs\P2N-PreNetworks.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-NetworksJS.txt ..\specs\P2N-NetworksJS.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionImages.txt ..\specs\FusionImages.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionIramuteq2.txt ..\specs\FusionIramuteq2.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Fusion.txt ..\specs\Fusion.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-FreePlane.txt ..\specs\P2N-FreePlane.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTable.txt ..\specs\FormateExportDataTable.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportPivotTable.txt ..\specs\FormateExportPivotTable.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTableFamilies.txt ..\specs\FormateExportDataTableFamilies.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportBiblio.txt ..\specs\FormateExportBiblio.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportCountryCartography.txt ..\specs\FormateExportCountryCartography.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionCarrot2.txt ..\specs\FusionCarrot2.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Interface2.txt ..\specs\Interface2.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Parallel3.txt ..\specs\Parallel3.spec

pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-IPC-Abstracts-Augment.txt ..\specs\IPC-Abstracts-Augment.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --hidden-import sklearn.neighbors.typedefs --version-file=version-P2N-ClusterPreProcess.txt specs\ClusterPreProcess.spec
pyinstaller -p . --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --hidden-import sklearn.neighbors.typedefs --version-file=version-P2N-Cluster.txt specs\P2N-Cluster.spec

mkdir  ..\distribution\Patent2Net\

xcopy /S /Y ..\distribution\FormateExportAttractivityCartography ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\OPSGatherPatentsv2 ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\OPSGatherContentsV2-Iramuteq ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\OPSGatherAugment-Families ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\OPSGatherContentsV2-Images ..\distribution\Patent2Net\
REM xcopy /S /Y ..\distribution\Compatibilizer ..\distribution\Patent2Net\

xcopy /S /Y ..\distribution\IPC-Abstracts-Augment ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\ClusterPreProcess ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\P2N-Cluster ..\distribution\Patent2Net\

xcopy /S /Y ..\distribution\P2N-Networks ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\P2N-PreNetworks ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\P2N-NetworksJS ..\distribution\Patent2Net\

xcopy /S /Y ..\distribution\FusionIramuteq2 ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FusionImages ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\Fusion ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\P2N-FreePlane ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportDataTable ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportPivotTable ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportDataTableFamilies ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportBiblio ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportCountryCartography ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FusionCarrot2 ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\Interface2 ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\Parallel3 ..\distribution\Patent2Net\


REM xcopy /S /Y ..\distribution\P2N-FamiliesHierarc ..\distribution\Patent2Net\

xcopy /Y root\* ..\distribution\
copy /Y ipcr_2015.xml ..\distribution\Patent2Net\
copy /Y requete.cql ..\distribution\
copy /y cacert.pem ..\distribution\Patent2Net\
copy /y countries.json ..\distribution\Patent2Net
copy /y P2N.css ..\distribution\Patent2Net
copy /y NameCountryMap.csv ..\distribution\Patent2Net\
copy /y scriptSearch.js ..\distribution\Patent2Net\
copy /y Searchscript.js ..\distribution\Patent2Net\
copy /y CollecteETRaite.bat ..\distribution\Patent2Net\
copy /y Process.bat ..\distribution\Patent2Net\
copy /y FormatingProcess.bat ..\distribution\Patent2Net\
copy /y GatherProcess.bat ..\distribution\Patent2Net\
copy /y NetsProcess.bat ..\distribution\Patent2Net\
copy /y ProcessPy.bat ..\distribution\Patent2Net\
REM copy /y OpenNav.bat ..\distribution\Patent2Net\OpenNav.bat
mkdir  ..\distribution\Patent2Net\templates
xcopy /S /Y templates  ..\distribution\Patent2Net\templates
copy /y cles-epo.txt  ..\distribution\
mkdir ..\distribution\Patent2Net\lib2to3
xcopy /S /Y lib2to3 ..\distribution\Patent2Net\lib2to3
mkdir ..\distribution\Patent2Net\extensions
mkdir ..\distribution\Patent2Net\media
xcopy /S /Y extensions ..\distribution\Patent2Net\extensions
xcopy /S /Y media ..\distribution\Patent2Net\media
mkdir ..\distribution\RequestsSet
mkdir ..\distribution\REQUESTS
copy /y Process.bat ..\distribution\
copy /y GatherProcess.bat  ..\distribution\
copy /y NetsProcess.bat  ..\distribution\
copy /y FormatingProcess.bat  ..\distribution\
copy /y *.info ..\distribution\
del *.info

REM cleaning
rmdir /S /Q ..\distribution\FormateExportAttractivityCartography
rmdir /S /Q ..\distribution\OPSGatherPatentsv2
rmdir /S /Q ..\distribution\OPSGatherContentsV2-Iramuteq
rmdir /S /Q ..\distribution\OPSGatherAugment-Families
rmdir /S /Q ..\distribution\OPSGatherContentsV2-Images
rmdir /S /Q ..\distribution\P2N-Networks
rmdir /S /Q ..\distribution\P2N-PreNetworks
rmdir /S /Q ..\distribution\P2N-NetworksJS
rmdir /S /Q ..\distribution\FusionIramuteq2
rmdir /S /Q ..\distribution\FusionImages
rmdir /S /Q ..\distribution\Fusion
rmdir /S /Q ..\distribution\P2N-FreePlane
rmdir /S /Q ..\distribution\FormateExportDataTable
rmdir /S /Q ..\distribution\FormateExportPivotTable
rmdir /S /Q ..\distribution\FormateExportDataTableFamilies
rmdir /S /Q ..\distribution\FormateExportBiblio
rmdir /S /Q ..\distribution\FormateExportCountryCartography
rmdir /S /Q ..\distribution\FusionCarrot2
rmdir /S /Q ..\distribution\Interface2
rmdir /S /Q ..\distribution\Parallel3

