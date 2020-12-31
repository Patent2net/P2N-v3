FROM elasticsearch:7.9.2

RUN yum -y update; yum clean all
RUN yum -y install git; yum clean all

WORKDIR /usr/share/elasticsearch
RUN set -ex && for path in data logs config config/scripts; do \
        mkdir -p "$path"; \
        chown -R elasticsearch:elasticsearch "$path"; \
    done

RUN cd /usr/share/elasticsearch
RUN git clone https://github.com/carrot2/elasticsearch-carrot2.git
RUN cd elasticsearch-carrot2
RUN bin/elasticsearch-plugin install org.carrot2:elasticsearch-carrot2:7.9.2
COPY --chown=elasticsearch custom_elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
USER elasticsearch

EXPOSE 9200 9300

ENV PATH=$PATH:/usr/share/elasticsearch/bin

CMD ["elasticsearch"]

