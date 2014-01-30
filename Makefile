# Here comes the variables
OUTPUT = 		main
CIVIL = 		Civil.c
CIVIL_HEADER = 	Civil.h


all: Civil.o
	g++ -o $(OUTPUT) main.c Civil.o

Civil.o: $(CIVIL) $(CIVIL_HEADER)
	g++ -c $(CIVIL)

output: gnuplot.sh
	cat gnuplot.sh | gnuplot

clean:
	rm *.o
