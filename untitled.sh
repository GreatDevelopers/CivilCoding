#!/bin/bash
if [ ! -f main ]; then
		ln -s src/main main
	fi
	mkdir ../../photos
	if [ ! -d ../../photos ]; then
		echo "Cannot make photos directory in public_html. Make it manually and give it write permissions";
	fi

	#Check if we can write in the photos direcly
	sudo -u www-data touch ../../photos/somefile
	if [ ! -f ../../photos/somefile ]; then
		sudo chmod -R 777 ../../photos/
	else
		rm ../../photos/somefile
	fi

	#Now we have write and read permissions. Place the files form the asset folder in the assets folder
	cp assets/* ../../photos/
	sudo chmod -R 777 ../`basename $(pwd)`
