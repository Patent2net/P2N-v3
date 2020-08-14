@ECHO OFF
docker run -t -d -p 0.0.0.0:50000-50520:50000-50520 -p 0.0.0.0:20-21:20-21 -p 0.0.0.0:5000:5000 --name p2na p2na:1.0 || docker start p2na
docker exec -d p2na vsftpd

start "" "http://127.0.0.1:5000/"