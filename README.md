CivilCoding
===========

Programs related to Civil Engineering


Requirements
============

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
