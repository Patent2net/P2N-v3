REM this will install ES & kibana
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.9.2
docker pull docker.elastic.co/kibana/kibana:7.9.2
docker volume create volumeInd
docker network create elastic
docker build --no-cache --tag elasticp2n .
docker run -d --mount source=volumeInd,target=/usr/share/elasticsearch/data --network=elastic --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticp2n

docker run -d --network=elastic --name kibana -p 5601:5601 docker.elastic.co/kibana/kibana:7.9.2