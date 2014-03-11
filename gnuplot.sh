set title "BM" tc rgb "blue"
set term png
set output "BM.png"
set xlabel "x axis" tc rgb "black"
set ylabel "y axis" tc rgb "red"
set border linecolor rgbcolor "grey"
set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2 # --- red
set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2 # --- green
plot "cantbm.out" with linespoints lt rgb "green"


set title "SF" tc rgb "blue"
set term png
set output "SF.png"
set xlabel "x axis" tc rgb "black"
set ylabel "y axis" tc rgb "red"
set border linecolor rgbcolor "grey"
set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2 # --- red
set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2 # --- green
plot "cantsf.out" with linespoints lt rgb "green"
