#For the manual installation on which that dockerfile is based go to :https://docs.ip-tools.org/patent2net/index.html
# Run the ubuntu image of docker
FROM centos:8
#Set Environment langage Profile
#ENV LANG=LC.UTF-8 LC_ALL=LC.UTF-8
ENV container docker

## Systemd cleanup base image
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;


#RUN localectl set-locale LANG=fr_FR.utf8

#Install packages for system
RUN yum -y update 

RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all

RUN yum install -y curl \
		gcc \
		graphviz \
		ImageMagick \
		libjpeg-dev \
		libxml2-dev \
		libfreetype6-dev \
		libpng-dev \
		libgraphviz-dev \
		libncurses5-dev \
		libncursesw5-dev \
		pkg-config \
		
RUN yum -y update; yum -y install which vsftpd net-tools vsftpd-sysvinit; yum clean all
COPY vusers.txt /etc/vsftpd/
RUN db_load -T -t hash -f /etc/vsftpd/vusers.txt /etc/vsftpd/vsftpd-virtual-user.db; rm -v /etc/vsftpd/vusers.txt; \ 
	chmod 600 /etc/vsftpd/vsftpd-virtual-user.db
COPY vsftpd.conf /etc/vsftpd/
COPY vsftpd.virtual /etc/pam.d/
COPY vsftpd.service /usr/lib/systemd/system/vsftpd.service


#RUN  passwd -l root 


	
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
		Flask \
		flask_cors \
		elasticsearch 

#Clone and install p2n from github

RUN yum -y update; yum clean all
RUN yum -y install git; yum clean all
RUN cd /usr/src/
RUN git clone -b master https://github.com/Patent2net/P2N-V3
#VOLUME P2N-V3
#RUN chown -R root:ftp /usr/src/P2N-V3


# java 
RUN yum -y install java-11-openjdk.x86_64

# carrot2
# RUN git clone -b master https://github.com/carrot2/carrot2.git
# using the binary release

# open vsftpd services for anonymous_enable


RUN mkdir P2N-V3/DATA
#RUN mkdir P2N-V3/indexData
#RUN chmod -R 755 P2N-V3/indexData
RUN chmod -R 755 P2N-V3/DATA

EXPOSE 20-21
EXPOSE 5000
EXPOSE 8005
EXPOSE 51000-51050

RUN yum -y install unzip

WORKDIR P2N-V3

RUN chmod -R 755 update.sh
RUN chmod 755 carrot2.sh
#RUN carrot2.sh
 
#RUN P2N-V3/carrot2/carrot2-4.0.4/dcs/dcs.sh --port 8005 &
CMD ["/usr/sbin/vsftpd","-obackground=NO"]
ENTRYPOINT /usr/sbin/init & python app.py && bash && /usr/sbin/vsftpd && dcs

