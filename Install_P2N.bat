@ECHO OFF
docker volume create p2nData
docker build --tag p2ne:1.0 .