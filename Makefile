# Here comes the variables
OUTPUT = 		main
CIVIL = 		Civil.c
CIVIL_HEADER = 	Civil.h


all: Civil.o
	g++ -o $(OUTPUT) main.cpp Civil.o -lrudecgi

Civil.o: $(CIVIL) $(CIVIL_HEADER)
	g++ -c $(CIVIL)

output: gnuplot.sh
	cat gnuplot.sh | gnuplot

clean:
	rm *.o
	rm *.out
	rm *.png
	
