# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
set key autotitle columnhead
set terminal pdfcairo enhanced

set xlabel "Fault Rate ({/Symbol l})" font ", 16"
set ylabel "Success Ratio" font ", 16"
# set grid
set key right title "Utilization" font ",14"
set key box

set xtics rotate by -45
# set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 pi -1 ps 0.5
set style line 1 lc "blue" lt 1 lw 2 pt 1 pi -1 ps 0.8
set style line 2 lc "magenta" lt 1 lw 2 pt 3 pi -1 ps 0.8
set style line 3 lc "orange" lt 1 lw 2 pt 5 pi -1 ps 0.8
set style line 4 lc "black" lt 1 lw 2 pt 7 pi -1 ps 0.8
set style line 5 lc "green" lt 1 lw 2 pt 9 pi -1 ps 0.8
set pointintervalbox -1

# Define the lambda names on x-axis
# set xtics ("1e-5/h" 1, "1e-4/h" 2, "1e-3/h" 3, "1e-2/h" 4, "1e-1/h" 5, "1e-2/min" 6, "1e-1/min" 7, "1e-1/sec" 8)
set xtics ("1e-5/h" 0, "1e-4/h" 1, "1e-3/h" 2, "1e-2/h" 3, "1e-1/h" 4, "1e-2/min" 5, "1e-1/min" 6, "1e-1/sec" 7)

set style fill solid 0.5 border -1
set datafile separator ","

set xtics font ", 14"
set ytics font ", 14"

set xrange [-0.3:7.3]
set yrange [-0.03:1.03]


set output 'n5_success_rate.pdf'
set title "N = 5" font ", 16"
plot 'n5/n5_total.csv' using 0:(1 - $4) with linespoints ls 1 title "0.2", \
    '' using 0:(1 - $8) with linespoints ls 2 title "0.4", \
    '' using 0:(1 - $12) with linespoints ls 3 title "0.6", \
    '' using 0:(1 - $16) with linespoints ls 4 title "0.8", \
    '' using 0:(1 - $20) with linespoints ls 5 title "1.0"

set output 'n10_success_rate.pdf'
set title "N = 10" font ", 16"
plot 'n10/n10_total.csv' using 0:(1 - $4) with linespoints ls 1 title "0.2", \
    '' using 0:(1 - $8) with linespoints ls 2 title "0.4", \
    '' using 0:(1 - $12) with linespoints ls 3 title "0.6", \
    '' using 0:(1 - $16) with linespoints ls 4 title "0.8", \
    '' using 0:(1 - $20) with linespoints ls 5 title "1.0"

set output 'n25_success_rate.pdf'
set title "N = 25" font ", 16"
plot 'n25/n25_total.csv' using 0:(1 - $4) with linespoints ls 1 title "0.2", \
    '' using 0:(1 - $8) with linespoints ls 2 title "0.4", \
    '' using 0:(1 - $12) with linespoints ls 3 title "0.6", \
    '' using 0:(1 - $16) with linespoints ls 4 title "0.8", \
    '' using 0:(1 - $20) with linespoints ls 5 title "1.0"

set output 'n50_success_rate.pdf'
set title "N = 50" font ", 16"
plot 'n50/n50_total.csv' using 0:(1 - $4) with linespoints ls 1 title "0.2", \
    '' using 0:(1 - $8) with linespoints ls 2 title "0.4", \
    '' using 0:(1 - $12) with linespoints ls 3 title "0.6", \
    '' using 0:(1 - $16) with linespoints ls 4 title "0.8", \
    '' using 0:(1 - $20) with linespoints ls 5 title "1.0"

# plot 'n5/n5_total.csv' using 4 with linespoints ls 1 title "Utilization 0.2", \
#     # '' u 0:4:(sprintf("%.3f", $4)) w labels offset -0.5, 1.1 font ",12" notitle, \
#     '' using 8 with linespoints ls 2 title "Utilization 0.4", \
#     # '' u 0:8:(sprintf("%.3f", $8)) w labels offset -0.5, 1.1 font ",12" notitle, \
#     '' using 12 with linespoints ls 3 title "Utilization 0.6", \
#     # '' u 0:12:(sprintf("%.3f", $12)) w labels offset -0.5, 1.1 font ",12" notitle., \
#     '' using 16 with linespoints ls 4 title "Utilization 0.8", \
#     # '' u 0:16:(sprintf("%.3f", $16)) w labels offset -0.5, 1.1 font ",12" notitle, \
#     '' using 20 with linespoints ls 5 title "Utilization 1.0"
#     # '' u 0:20:(sprintf("%.3f", $20)) w labels offset -0.5, 1.1 font ",12" notitle
