#For the manual installation on which that dockerfile is based go to :https://docs.ip-tools.org/patent2net/index.html
# Run the ubuntu image of docker
FROM centos:8
#Set Environment langage Profile
#ENV LANG=LC.UTF-8 LC_ALL=LC.UTF-8
ENV container docker



#RUN localectl set-locale LANG=fr_FR.utf8

#Install packages for system
RUN yum -y update 

RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all


		
RUN yum -y update 
RUN yum -y install vsftpd; yum clean all
RUN yum -y install which; yum clean all
RUN yum -y install net-tools; yum clean all

RUN yum install -y curl \
		gcc \
		graphviz \
		ImageMagick \
		pkg-config

RUN yum -y update; yum clean all		
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
RUN yum -y install unzip
# java 
RUN yum -y install java-11-openjdk.x86_64

#configuring vsftpd
# COPY vusers.txt /etc/vsftpd/
# RUN db_load -T -t hash -f /etc/vsftpd/vusers.txt /etc/vsftpd/vsftpd-virtual-user.db; rm -v /etc/vsftpd/vusers.txt; \ 
#	chmod 600 /etc/vsftpd/vsftpd-virtual-user.db
#COPY vsftpd.conf /etc/vsftpd/
#COPY vsftpd.virtual /etc/pam.d/
#COPY vsftpd.service /usr/lib/systemd/system/vsftpd.service

RUN useradd p2n -d /usr/src/P2N-V3 -G wheel,ftp -p p2n -M

RUN cd /usr/src/
RUN mkdir P2N-V3
RUN cd P2N-V3
RUN wget https://github.com/Patent2net/P2N-V3.git
#RUN git https://github.com/Patent2net/P2N-V3.git
RUN chown -R p2n:p2n /usr/src/P2N-V3
RUN su - p2n
RUN mkdir P2N-V3/DATA
#RUN mkdir P2N-V3/indexData
#RUN chmod -R 755 P2N-V3/indexData
RUN chmod -R 755 P2N-V3/DATA

EXPOSE 20-21
EXPOSE 5000
EXPOSE 8005
EXPOSE 51000-51010

WORKDIR /usr/src/P2N-V3

RUN chmod -R 755 update.sh
RUN chmod 755 carrot2.sh
RUN carrot2.sh
 
RUN P2N-V3/carrot2/carrot2-4.0.4/dcs/dcs.sh --port 8005 &
CMD ["/usr/sbin/vsftpd","-obackground=NO"]
ENTRYPOINT python app.py && bash && /usr/sbin/vsftpd && dcs

