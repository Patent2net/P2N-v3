conda activate P2N
for %%i in (REQUESTS/*.cql) do p2n run --config=../REQUESTS/%%i --with-family

