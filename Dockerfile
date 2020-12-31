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
#RUN yum -y install which; yum clean all
#RUN yum -y install net-tools; yum clean all

RUN yum install -y curl \
		gcc \
		graphviz \
		ImageMagick \
		pkg-config

RUN yum -y update; yum clean all		
#RUN  passwd -l root 
#RUN useradd p2n -d /usr/src/P2N-V3 -G wheel,ftp -M
#RUN passwd -f -d p2n	
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
# java uncomment for carrot2
# RUN yum -y install java-11-openjdk.x86_64

#configuring vsftpd
RUN chmod 777  /etc/vsftpd/vsftpd.conf
# RUN COPY vsftpd.conf /etc/vsftpd/vsftpd.conf
RUN { \
        echo 'anonymous_enable=NO'; \
        echo 'userlist_deny=NO'; \
        echo 'local_enable=YES'; \
        echo 'connect_from_port_20=YES'; \
        echo 'write_enable=YES'; \
        echo 'ftpd_banner=Welcome to P2N VSFTPD service.'; \
        echo 'local_umask=022'; \
        echo 'dirmessage_enable=YES'; \
        echo 'xferlog_enable=YES'; \
        echo 'chown_uploads=YES'; \
        echo 'chown_username=p2n'; \
        echo 'xferlog_std_format=YES'; \
        echo 'pasv_addr_resolve=YES'; \
        echo 'pasv_address=0.0.0.0'; \
        echo 'pasv_enable=YES'; \
        echo 'pasv_max_port=51010'; \
        echo 'pasv_min_port=51000'; \
        echo 'port_enable=YES'; \
        echo 'listen=NO'; \
        echo 'listen_ipv6=YES'; \
        echo 'pam_service_name=vsftpd'; \
        echo 'userlist_enable=YES'; \	
    } > /etc/vsftpd/vsftpd.conf
RUN chmod 400  /etc/vsftpd/vsftpd.conf
# RUN COPY vsftpd.conf /etc/vsftpd/vsftpd.conf
RUN chmod 777 /etc/vsftpd/user_list
RUN { \
        echo 'p2n'; \
        echo ''; \	
    } > /etc/vsftpd/user_list
RUN chmod 400 /etc/vsftpd/user_list
#RUN COPY users.txt /etc/vsftpd/user_list

RUN yum install -y passwd

RUN cd /usr/src/
WORKDIR /usr/src/
RUN mkdir P2N-V3
#
RUN git clone https://github.com/Patent2net/P2N-V3.git

RUN useradd p2n -d /usr/src/P2N-V3 -G wheel,ftp -M
RUN passwd -f -d p2n
RUN chown -R p2n:p2n /usr/src/P2N-V3
RUN su - p2n
RUN cd /usr/src/P2N-V3

RUN mkdir DATA
#RUN mkdir P2N-V3/indexData
#RUN chmod -R 755 P2N-V3/indexData
RUN chmod -R 755 DATA

EXPOSE 20-21
EXPOSE 5000
EXPOSE 8005
EXPOSE 51000-51010

WORKDIR /usr/src/P2N-V3
RUN cd /usr/src/P2N-V3
RUN chmod -R 755 update.sh

# uncomment the 3 next lines for carrot2 (if java installed)
#RUN chmod 755 carrot2.sh
#RUN carrot2.sh 
#RUN P2N-V3/carrot2/carrot2-4.0.4/dcs/dcs.sh --port 8005 &
CMD ["/usr/sbin/vsftpd &"]
ENTRYPOINT bash && /usr/sbin/vsftpd && python app.py

