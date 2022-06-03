python OPSGatherPatentsv2.py  $@
python OPSGatherAugment-Families.py $@
python PatentListFiltering.py $@
python preProcessNormalisationNames.py $@

python FormateExportAttractivityCartography.py $@
python FormateExportBiblio.py $@
python FormateExportCountryCartography.py $@

python P2N-Trizifyer-syntax.py $@
python P2N-Trizifyer-semantic.py $@

python FormateExportDataTableFamilies.py $@
python FormateExportDataTable.py $@
python FormateExportPivotTable.py $@

python P2N-Nets-new.py  $@

python OPSGatherContentsV2-Iramuteq.py $@
python FusionIramuteq2.py $@

python OPSGatherContentsV2-Images.py  $@
python FusionImages.py $@

python P2N-FreePlane.py $@
python P2N-Indexer.py $@
python FusionCarrot2.py  $@

python IPC-Abstracts-Augment.py $@
python clusterPreProcess.py $@
python P2N-Cluster.py $@

python Interface2.py $@



