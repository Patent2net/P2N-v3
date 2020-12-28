@ECHO OFF
docker run -t -d -p 0.0.0.0:50000-50050:50000-50050 -p 0.0.0.0:20-21:20-21 -p 0.0.0.0:5000-5010:5000-5010 --name p2na p2na:1.0 || docker start p2na
docker exec -d p2na vsftpd
docker exec -d p2na /usr/src/P2N-V3/carrot2/carrot2-4.0.4/dcs/dcs.sh --port 5005
start "" "http://127.0.0.1:5000/"