for /F "delims=~" %%f in (requirementsPip.txt) do pip install --upgrade "%%f" && python -m textblob.download_corpora

