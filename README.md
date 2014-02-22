CivilCoding
===========

Programs related to Civil Engineering


Requirements
============

	Configure public_html/cgi-bin folder for executing files on browser.<br>
	Assuming you already installed apache if not then run following
	command in terminal

    	$ sudo apt-get install apache2
    
	**Steps to configure public_html**
        
    	$ mkdir ~/public_html
    
    	$ sudo a2enmod userdir
        
    	$ sudo service apache2 restart
        
	Give 755 permissions to public_html directory
        
    	$ chmod -R 755 ~/public_html
        
	Now open http://localhost/~username in browser.
	Here username is your login name.
    
	**Steps to configure cgi-bin in public_html**
    
    	$ sudo a2enmod cgi
    
    	$ sudo a2enmod cgid
    
    	$ sudo service apache2 restart
     
    	$ cd ~/public_html
    
    	$ mkdir cgi-bin
    
    	$ cd /etc/apache2
    
    	$ sudo vim sites-available/default
    
	Add following text in file:
    
    	ScriptAlias /cgi-bin/ /home/*/public_html/cgi-bin/
    	<Directory "/home/*/public_html/cgi-bin">
        	AllowOverride None
        	Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        	SetHandler cgi-script
        	Order allow,deny
        	Allow from all
    	</Directory>
    
	Save it and then restart apache

    	$ sudo service apache2 restart

	Installing the C/C++ Compiler and Make
	
	$ sudo apt-get install build-essential

	Installing GNUPLOT to plot the graph

	$ sudo apt-get install gnuplot
	
	Only required Library for this is RUDE CGI Library. You can use the following link to download it.

	http://www.rudeserver.com/cgiparser/download/rudecgi-5.0.0.tar.gz

	Untar it. cd to rudecgi-5.0.0 directory

	Now Execute the following commands

	$ ./configure

	$ make

	$ sudo make install

	Or you can install RUDECGI from Terminal

	$ sudo apt-get install librudecgi5 librudecgi-dev

How to Use
==========

	Clone this repository in your /home/yourusername/public_html/cgi-bin/
	
	$ git clone https://github.com/GreatDevelopers/CivilCoding

	After Cloning give CivilCoding folder write permissions.

	$ chmod -R 777 CivilCoding

	Now cd to CivilCoding directory

	$ cd ~/public_html/cgi-bin/CivilCoding

	$ make

	Make command will compile the program

	Then open your browser and point it to http://localhost/~username/cgi-bin/CivilCoding/main


AUTHORS:
--------

<b>Mentor and Manager</b>

Dr. Hardeep Singh Rai

Website: http://gndec.ac.in/~hsrai

[Piyush Parkash](https://github.com/piyushparkash)

Website: piyushparkash.blogspot.com
