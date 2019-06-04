CALL conda.bat activate P2N && for /F "delims=~" %%f in (requirements.txt) do CALL conda install --yes "%%f" && CALL conda install --yes pygraphviz -c alubbock
