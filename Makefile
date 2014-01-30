# Here comes the variables
OUTPUT = main



all: Civil_new.o
	g++ -o $(OUTPUT) main.c Civil_new.o

Civil_new.o: Civil_new.h Civil_new.c
	g++ -c Civil_new.c

output: gnuplot.sh
	cat gnuplot.sh | gnuplot

clean:
	rm *.o
