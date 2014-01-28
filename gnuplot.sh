set title "Look 1" tc rgb "blue"
set term png
set output "1.png"
set xlabel "x axis" tc rgb "yellow"
set ylabel "y axis" tc rgb "red"
set border linecolor rgbcolor "grey"
plot "cantbm.out" using 1:1 with lines lt rgb "green"
