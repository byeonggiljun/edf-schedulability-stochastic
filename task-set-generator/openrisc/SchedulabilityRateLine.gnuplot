# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
# set key autotitle columnhead
set terminal pdfcairo enhanced

set style fill solid 0.5 border -1
set datafile separator ","

# Define the lambda names on x-axis
# set xtics ("1e-7/h" 0, "1e-6/h" 1, "1e-5/h" 2, "1e-4/h" 3, "1e-3/h" 4, "1e-2/h" 5, "1e-1/h" 6, "1e-1/h" 7)

# set xtics font ", 14"
set format x ""
set xtics scale 1
set ytics (0, 500, 1000)
# set ytics font ", 18"
set format y ""

# set xrange [-0.3:6.3]
set xrange [0.7:7.3]
set yrange [-0.03:1050]
# set key outside horizontal box
unset key

folder ="plots/"
#####################   Utilization 0.1   ###############################
# set title "Utilization = 0.1" font ", 16"
set output folder.'n5_u1.pdf'
plot 'n5/n5_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

set output folder.'n10_u1.pdf'
plot 'n10/n10_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

set output folder.'n25_u1.pdf'
plot 'n25/n25_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

set output folder.'n50_u1.pdf'
plot 'n50/n50_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

#####################   Utilization 0.2   ###############################
# set title "Utilization = 0.2" font ", 16"
set output folder.'n5_u2.pdf'
plot 'n5/n5_total.csv' using 0:13 lt 2 lw 3 with linespoints notitle, \
    '' using 0:14 lt 3 lw 3 with linespoints notitle, \
    '' using 0:15 lt 6 lw 3 with linespoints notitle, \
    '' using 0:16 lt 4 lw 3 with linespoints notitle, \
    '' using 0:17 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n10_u2.pdf'
plot 'n10/n10_total.csv' using 0:13 lt 2 lw 3 with linespoints notitle, \
    '' using 0:14 lt 3 lw 3 with linespoints notitle, \
    '' using 0:15 lt 6 lw 3 with linespoints notitle, \
    '' using 0:16 lt 4 lw 3 with linespoints notitle, \
    '' using 0:17 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n25_u2.pdf'
plot 'n25/n25_total.csv' using 0:13 lt 2 lw 3 with linespoints notitle, \
    '' using 0:14 lt 3 lw 3 with linespoints notitle, \
    '' using 0:15 lt 6 lw 3 with linespoints notitle, \
    '' using 0:16 lt 4 lw 3 with linespoints notitle, \
    '' using 0:17 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n50_u2.pdf'
plot 'n50/n50_total.csv' using 0:13 lt 2 lw 3 with linespoints notitle, \
    '' using 0:14 lt 3 lw 3 with linespoints notitle, \
    '' using 0:15 lt 6 lw 3 with linespoints notitle, \
    '' using 0:16 lt 4 lw 3 with linespoints notitle, \
    '' using 0:17 lt 8 lc rgb 'red' lw 3 with linespoints notitle

#####################   Utilization 0.3   ###############################
# set title "Utilization = 0.3" font ", 16"
set output folder.'n5_u3.pdf'
plot 'n5/n5_total.csv' using 0:23 lt 2 lw 3 with linespoints notitle, \
    '' using 0:24 lt 3 lw 3 with linespoints notitle, \
    '' using 0:25 lt 6 lw 3 with linespoints notitle, \
    '' using 0:26 lt 4 lw 3 with linespoints notitle, \
    '' using 0:27 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n10_u3.pdf'
plot 'n10/n10_total.csv' using 0:23 lt 2 lw 3 with linespoints notitle, \
    '' using 0:24 lt 3 lw 3 with linespoints notitle, \
    '' using 0:25 lt 6 lw 3 with linespoints notitle, \
    '' using 0:26 lt 4 lw 3 with linespoints notitle, \
    '' using 0:27 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n25_u3.pdf'
plot 'n25/n25_total.csv' using 0:23 lt 2 lw 3 with linespoints notitle, \
    '' using 0:24 lt 3 lw 3 with linespoints notitle, \
    '' using 0:25 lt 6 lw 3 with linespoints notitle, \
    '' using 0:26 lt 4 lw 3 with linespoints notitle, \
    '' using 0:27 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n50_u3.pdf'
plot 'n50/n50_total.csv' using 0:23 lt 2 lw 3 with linespoints notitle, \
    '' using 0:24 lt 3 lw 3 with linespoints notitle, \
    '' using 0:25 lt 6 lw 3 with linespoints notitle, \
    '' using 0:26 lt 4 lw 3 with linespoints notitle, \
    '' using 0:27 lt 8 lc rgb 'red' lw 3 with linespoints notitle

#####################   Utilization 0.4   ###############################
# set title "Utilization = 0.4" font ", 16"
set output folder.'n5_u4.pdf'
plot 'n5/n5_total.csv' using 0:33 lt 2 lw 3 with linespoints notitle, \
    '' using 0:34 lt 3 lw 3 with linespoints notitle, \
    '' using 0:35 lt 6 lw 3 with linespoints notitle, \
    '' using 0:36 lt 4 lw 3 with linespoints notitle, \
    '' using 0:37 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n10_u4.pdf'
plot 'n10/n10_total.csv' using 0:33 lt 2 lw 3 with linespoints notitle, \
    '' using 0:34 lt 3 lw 3 with linespoints notitle, \
    '' using 0:35 lt 6 lw 3 with linespoints notitle, \
    '' using 0:36 lt 4 lw 3 with linespoints notitle, \
    '' using 0:37 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n25_u4.pdf'
plot 'n25/n25_total.csv' using 0:33 lt 2 lw 3 with linespoints notitle, \
    '' using 0:34 lt 3 lw 3 with linespoints notitle, \
    '' using 0:35 lt 6 lw 3 with linespoints notitle, \
    '' using 0:36 lt 4 lw 3 with linespoints notitle, \
    '' using 0:37 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n50_u4.pdf'
plot 'n50/n50_total.csv' using 0:33 lt 2 lw 3 with linespoints notitle, \
    '' using 0:34 lt 3 lw 3 with linespoints notitle, \
    '' using 0:35 lt 6 lw 3 with linespoints notitle, \
    '' using 0:36 lt 4 lw 3 with linespoints notitle, \
    '' using 0:37 lt 8 lc rgb 'red' lw 3 with linespoints notitle

#####################   Utilization 0.5   ###############################
# set title "Utilization = 0.5" font ", 16"
set output folder.'n5_u5.pdf'
plot 'n5/n5_total.csv' using 0:43 lt 2 lw 3 with linespoints notitle, \
    '' using 0:44 lt 3 lw 3 with linespoints notitle, \
    '' using 0:45 lt 6 lw 3 with linespoints notitle, \
    '' using 0:46 lt 4 lw 3 with linespoints notitle, \
    '' using 0:47 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n10_u5.pdf'
plot 'n10/n10_total.csv' using 0:43 lt 2 lw 3 with linespoints notitle, \
    '' using 0:44 lt 3 lw 3 with linespoints notitle, \
    '' using 0:45 lt 6 lw 3 with linespoints notitle, \
    '' using 0:46 lt 4 lw 3 with linespoints notitle, \
    '' using 0:47 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n25_u5.pdf'
plot 'n25/n25_total.csv' using 0:43 lt 2 lw 3 with linespoints notitle, \
    '' using 0:44 lt 3 lw 3 with linespoints notitle, \
    '' using 0:45 lt 6 lw 3 with linespoints notitle, \
    '' using 0:46 lt 4 lw 3 with linespoints notitle, \
    '' using 0:47 lt 8 lc rgb 'red' lw 3 with linespoints notitle

set output folder.'n50_u5.pdf'
plot 'n50/n50_total.csv' using 0:43 lt 2 lw 3 with linespoints notitle, \
    '' using 0:44 lt 3 lw 3 with linespoints notitle, \
    '' using 0:45 lt 6 lw 3 with linespoints notitle, \
    '' using 0:46 lt 4 lw 3 with linespoints notitle, \
    '' using 0:47 lt 8 lc rgb 'red' lw 3 with linespoints notitle
