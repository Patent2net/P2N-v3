@ECHO OFF
docker run -t -d -p 5000:5000 --name p2na p2na:1.0 || docker start p2na