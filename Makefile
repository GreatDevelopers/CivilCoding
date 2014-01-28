# Here comes the variables
OUTPUT = main



all: Civil.o
	g++ -o $(OUTPUT) main.c Civil.o

Civil.o: Civil.h Civil.c
	g++ -c Civil.c

output: gnuplot.sh
	cat gnuplot.sh | gnuplot	
