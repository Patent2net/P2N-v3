source /vpy3/bin/activate
for f in ./RequestsSets/*.cql ; do p2n run --config=.$f; done
