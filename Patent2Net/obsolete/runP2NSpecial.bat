conda activate P2N & for %%f in (Requests\*.cql) do (
move /Y %%f requete.cql & p2n acquire --config=../requete.cql
)
