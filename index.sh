#!/bin/bash


cat gnuplot.sh | gnuplot

#make sure we have the photos directory

if [ -d "../../photos" ]; then
	mkdir ../../photos/
fi
chmod -R 755 ../../photos/
mv BM.png ../../photos/
mv SF.png ../../photos/


# The Basic Header
echo Location: main?secondaryparameter=output
echo ""