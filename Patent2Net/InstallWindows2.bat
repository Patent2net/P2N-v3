for /F "delims=~" %%f in (Patent2Net\requirementsPip.txt) do pip install --upgrade "%%f"
