# Here comes the variables
OUTPUT = main



all:
	g++ -o $(OUTPUT) main.c


output:
	cat gnuplot.sh | gnuplot	
