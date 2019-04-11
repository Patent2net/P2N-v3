for /F "delims=~" %%f in (Patent2Net\requirements.txt) do conda install --yes "%%f" 

