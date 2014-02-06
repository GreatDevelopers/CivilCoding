set title "BM" tc rgb "blue"
set term png
set output "BM.png"
set xlabel "x axis" tc rgb "black"
set ylabel "y axis" tc rgb "red"
set border linecolor rgbcolor "grey"
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5   # --- blue
plot "cantbm.out" with linespoints lt rgb "green"


set title "SF" tc rgb "blue"
set term png
set output "SF.png"
set xlabel "x axis" tc rgb "black"
set ylabel "y axis" tc rgb "red"
set border linecolor rgbcolor "grey"
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5   # --- blue
plot "cantsf.out" with linespoints lt rgb "green"
