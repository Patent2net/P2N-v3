conda activate P2N & for /F "delims=~" %%f in (Patent2Net\requirements.txt) do conda install --yes "%%f" 
& conda install pygraphviz -c alubbock