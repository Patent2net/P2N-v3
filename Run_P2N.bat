@ECHO OFF
docker run -t -d -p 0.0.0.0:51000-51010:51000-51010 -p 0.0.0.0:20-21:20-21 -p 0.0.0.0:5000-5010:5000-5010  -p 0.0.0.0:8005:8005 -v /usr/src/P2N-V3:/home/vsftpd -e FTP_USER=root -e FTP_PASS=123456 -e PASV_ADDRESS=localhost -e PASV_MIN_PORT=21100 -e PASV_MAX_PORT=21110 --name vsftpd --privileged=true --restart=always --name p2ne p2ne:1.0 || docker start p2ne
REM Open 20 firewall port
REM firewall-cmd --zone=public --add-port=20/tcp --permanent
REM Open port 21 of firewall
REM firewall-cmd --zone=public --add-port=21/tcp --permanent
REM Open 51000-51010 firewall port
REM firewall-cmd --zone=public --add-port=51000-51010/tcp --permanent
REM Restart the firewall
REM firewall-cmd --reload
REM View the ports where the firewall has been started
REM firewall-cmd --zone=public --list-ports
REM docker exec -d p2ne /usr/src/P2N-V3/carrot2/carrot2-4.0.4/dcs/dcs.sh --port 5005
start "" "http://127.0.0.1:5000/"

