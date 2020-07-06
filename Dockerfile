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
				setuptools



RUN pip install dogpile.cache \
		mpld3 \
		python-epo-ops-client \
		sklearn \
		where \
		Flask

#Clone and install p2n from github

RUN apt-get -y install git
RUN git -C ./usr/src clone -b docker https://github.com/Patent2net/P2N-V3
WORKDIR /usr/src/P2N-V3
RUN python setup.py install


ENTRYPOINT python app.py && bash