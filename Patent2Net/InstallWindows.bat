for /F "delims=~" %%f in (requirements.txt) do conda install --yes "%%f" 

