# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
set key autotitle columnhead
set terminal pdfcairo enhanced
set output "key.pdf"

set style fill solid 0.5 border -1
set datafile separator ","

# Define the lambda names on x-axis
# set xtics ("1e-7/h" 0, "1e-6/h" 1, "1e-5/h" 2, "1e-4/h" 3, "1e-3/h" 4, "1e-2/h" 5, "1e-1/h" 6, "1e-1/h" 7)

# set xtics font ", 14"
# set format x ""
# set xtics scale 1
# set ytics (0, 500, 1000)
# set ytics font ", 18"

# set xrange [-0.3:6.3]
set xrange [-0.3:6.3]
set yrange [-0.03:1050]
# unset key

set key horizontal outside 
# set xrange[0:10]
# set yrange[0:1]
# plot NaN lt 7 title "RTailor", \
#     NaN lt 3 title "RTailor considering SDC", \
#     NaN lt 5 title "PREFACE" 

# folder ="plots/"
# #####################   Utilization 0.1   ###############################
# # set title "Utilization = 0.1" font ", 16"
set tmargin 10
set key spacing 1.5
plot 'n5/n5_total.csv' using 0:3 lt 2 lw 3 with linespoints title "Reghenzani", \
    '' using 0:4 lt 3 lw 3 with linespoints title "Reghenzani considering SDC", \
    '' using 0:5 lt 6 lw 3 with linespoints title "RTailor", \
    '' using 0:6 lt 4 lw 3 with linespoints title "RTailor considering SDC", \
    '' using 0:7 lt 8 lw 3 with linespoints title "PREFACE" 
