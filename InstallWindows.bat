for /F "delims=~" %%f in (requirements.txt) do conda install --yes "%%f" || pip install --upgrade "%%f"
