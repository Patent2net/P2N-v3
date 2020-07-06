-------------------- Install Docker P2N on another Computer ---------------------

Instead downloading Docker P2N on each computer you can create a tar file who will be used to install the P2N image on new computer.

* On The already installed Docker P2N machine :
	1- Go in "Copy Docker P2N" folder
	2- Click on "Copy_Docker_P2N.bat". The procedure will take some time. When ended, the window will close and you will see a "p2na.tar" file.
	3- Copy "Copy Docker P2N" folder on External device.


* On The new Computer :
	1- Copy "Copy Docker P2N" Folder from the external device on your computer.
	2- Download and install docker : https://docs.docker.com/get-docker/
	3- Click on "Load_Docker_P2N.bat" it will create the P2N image from the "p2na.tar" file present in the folder. 
		The window will automatically close at the end of the process.
	4- Go in "P2N Docker Folder"
	5- Click on "Run_P2N.bat", Docker P2N is now fully installed and will automatically start.
	6- Update the file cles-epo.txt with your credentials (if you don't have it follow the instructions who can be found here :
		http://patent2netv2.vlab4u.info/dokuwiki/doku.php?id=user_manual:download_install#register_the_use_of_p2n )
	7- Click on "Replace_Epo_P2N.bat" it will add the the updated cles-epo.txt in docker P2N.
	8 - You can now use P2N. To access it,on your web browser go at 127.0.0.1:5000

- After the installation "p2na.tar" is no longer needed. You can delete it if needed.
- The Copy initially don't have the "Cles-epo.txt" or the results of the research you did on the computer who created the tar file.
	it only propose a faster install for other computers after the install of the first one.

-"If your computer have latency after the install of Docker P2N go to Docker Options,
	 and uncheck "Use the WSL 2 based engine (requires Win 10 build 19018+)"