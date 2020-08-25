#For the manual installation on which that dockerfile is based go to :https://docs.ip-tools.org/patent2net/index.html
# Run the ubuntu image of docker
FROM ubuntu:latest

#Set Environment langage Profile
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

#Block the interactions of Debian Type applications, unblocking install tzdata
ARG DEBIAN_FRONTEND=noninteractive

#Install packages for system
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils


RUN apt-get install -y build-essential \
		curl \
		gcc \
		graphviz \
		imagemagick \
		libjpeg-dev \
		libxml2-dev \
		libfreetype6-dev \
		libpng-dev \
		libgraphviz-dev \
		libncurses5-dev \
		libncursesw5-dev \
		pkg-config \
		python-dev 
		

		
RUN apt-get update \
    && apt-get install -y vsftpd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

		
RUN  passwd -l root 

RUN { \
        echo 'allow_writeable_chroot=YES'; \
        echo 'anonymous_enable=YES'; \
        echo 'chroot_local_user=YES'; \
        echo 'connect_from_port_20=YES'; \
        echo 'dirmessage_enable=YES'; \
        echo 'ftpd_banner=Welcome to P2N VSFTPD service.'; \
        echo 'listen=YES'; \
        echo 'local_enable=YES'; \
        echo 'no_anon_password=YES'; \
        echo 'pasv_addr_resolve=YES'; \
        echo 'pasv_address=0.0.0.0'; \
        echo 'pasv_enable=YES'; \
        echo 'pasv_max_port=50520'; \
        echo 'pasv_min_port=50000'; \
        echo 'port_enable=YES'; \
        echo 'seccomp_sandbox=NO'; \
        echo 'write_enable=YES'; \
        echo 'xferlog_enable=YES'; \
		echo 'ftp_username=ftp'; \
		echo 'anon_upload_enable=YES'; \	
		echo 'anon_mkdir_write_enable=YES'; \	
		echo 'anon_root=/usr/src/P2N-V3'; \	
    } > /etc/vsftpd.conf


	
		
#Install Miniconda environment
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh &&\
	bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b &&\
	rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
RUN conda install -c anaconda -y python=3.6 &&\
	conda install -c anaconda -y \ 
				attrs \
				beautifulsoup4 \
				docopt \
				jinja2 \
				jsonpointer \
				lxml \
				matplotlib \
				networkx \
				nltk \
				numpy \
				pandas \
				Pillow \
				pip \
				pydot \
				pygraphviz \
				pyparsing \
				python-louvain \
				requests \
				setuptools \
				unidecode \
				python-Levenshtein \
				xlrd \
				openpyxl

RUN pip install dogpile.cache \
		mpld3 \
		python-epo-ops-client \
		sklearn \
		where \
		fuzzywuzzy \
		Flask

#Clone and install p2n from github

RUN apt-get update
RUN apt-get -y install git
RUN git -C ./usr/src clone -b master https://github.com/Patent2net/P2N-V3

# open vsftpd services for anonymous_enable

RUN chown -R root:ftp /usr/src/P2N-V3
RUN usermod -d /usr/src/P2N-V3 ftp
chmod -R 777 /usr/src/P2N-V3/DATA

RUN mkdir /var/run/vsftpd
RUN mkdir /var/run/vsftpd/empty


VOLUME /usr/src/P2N-V3

EXPOSE 20-21
EXPOSE 50000-50520
EXPOSE 5000

WORKDIR /usr/src/P2N-V3

RUN python setup.py build
RUN python setup.py install

ENTRYPOINT python app.py && bash && vsftpd

