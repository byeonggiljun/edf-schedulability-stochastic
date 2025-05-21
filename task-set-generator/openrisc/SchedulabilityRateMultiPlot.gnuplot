# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
# set key autotitle columnhead
set terminal pdfcairo enhanced size 20cm, 18cm
set output "MultiPlot.pdf"

set multiplot layout 5, 4

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
set yrange [-10:1050]
# set key outside horizontal box
unset key

set margin 0.2, 0.2, 0.2, 0.2

#####################   Utilization 0.1   ###############################
# set title "Utilization = 0.1" font ", 16"
plot 'n5/n5_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:8 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

plot 'n10/n10_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:8 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

plot 'n25/n25_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:8 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

plot 'n50/n50_total.csv' using 0:3 lt 2 lw 3 with linespoints notitle, \
    '' using 0:4 lt 3 lw 3 with linespoints notitle, \
    '' using 0:5 lt 6 lw 3 with linespoints notitle, \
    '' using 0:6 lt 4 lw 3 with linespoints notitle, \
    '' using 0:7 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:8 lt 8 lc rgb 'red' lw 3 with linespoints notitle 

#####################   Utilization 0.2   ###############################
# set title "Utilization = 0.2" font ", 16"
plot 'n5/n5_total.csv' using 0:15 lt 2 lw 3 with linespoints notitle, \
    '' using 0:16 lt 3 lw 3 with linespoints notitle, \
    '' using 0:17 lt 6 lw 3 with linespoints notitle, \
    '' using 0:18 lt 4 lw 3 with linespoints notitle, \
    '' using 0:19 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:20 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n10/n10_total.csv' using 0:15 lt 2 lw 3 with linespoints notitle, \
    '' using 0:16 lt 3 lw 3 with linespoints notitle, \
    '' using 0:17 lt 6 lw 3 with linespoints notitle, \
    '' using 0:18 lt 4 lw 3 with linespoints notitle, \
    '' using 0:19 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:20 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n25/n25_total.csv' using 0:15 lt 2 lw 3 with linespoints notitle, \
    '' using 0:16 lt 3 lw 3 with linespoints notitle, \
    '' using 0:17 lt 6 lw 3 with linespoints notitle, \
    '' using 0:18 lt 4 lw 3 with linespoints notitle, \
    '' using 0:19 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:20 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n50/n50_total.csv' using 0:15 lt 2 lw 3 with linespoints notitle, \
    '' using 0:16 lt 3 lw 3 with linespoints notitle, \
    '' using 0:17 lt 6 lw 3 with linespoints notitle, \
    '' using 0:18 lt 4 lw 3 with linespoints notitle, \
    '' using 0:19 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:20 lt 8 lc rgb 'red' lw 3 with linespoints notitle

#####################   Utilization 0.3   ###############################
# set title "Utilization = 0.3" font ", 16"
plot 'n5/n5_total.csv' using 0:27 lt 2 lw 3 with linespoints notitle, \
    '' using 0:28 lt 3 lw 3 with linespoints notitle, \
    '' using 0:29 lt 6 lw 3 with linespoints notitle, \
    '' using 0:30 lt 4 lw 3 with linespoints notitle, \
    '' using 0:31 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:32 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n10/n10_total.csv' using 0:27 lt 2 lw 3 with linespoints notitle, \
    '' using 0:28 lt 3 lw 3 with linespoints notitle, \
    '' using 0:29 lt 6 lw 3 with linespoints notitle, \
    '' using 0:30 lt 4 lw 3 with linespoints notitle, \
    '' using 0:31 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:32 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n25/n25_total.csv' using 0:27 lt 2 lw 3 with linespoints notitle, \
    '' using 0:28 lt 3 lw 3 with linespoints notitle, \
    '' using 0:29 lt 6 lw 3 with linespoints notitle, \
    '' using 0:30 lt 4 lw 3 with linespoints notitle, \
    '' using 0:31 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:32 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n50/n50_total.csv' using 0:27 lt 2 lw 3 with linespoints notitle, \
    '' using 0:28 lt 3 lw 3 with linespoints notitle, \
    '' using 0:29 lt 6 lw 3 with linespoints notitle, \
    '' using 0:30 lt 4 lw 3 with linespoints notitle, \
    '' using 0:31 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:32 lt 8 lc rgb 'red' lw 3 with linespoints notitle

#####################   Utilization 0.4   ###############################
# set title "Utilization = 0.4" font ", 16"
plot 'n5/n5_total.csv' using 0:39 lt 2 lw 3 with linespoints notitle, \
    '' using 0:40 lt 3 lw 3 with linespoints notitle, \
    '' using 0:41 lt 6 lw 3 with linespoints notitle, \
    '' using 0:42 lt 4 lw 3 with linespoints notitle, \
    '' using 0:43 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:44 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n10/n10_total.csv' using 0:39 lt 2 lw 3 with linespoints notitle, \
    '' using 0:40 lt 3 lw 3 with linespoints notitle, \
    '' using 0:41 lt 6 lw 3 with linespoints notitle, \
    '' using 0:42 lt 4 lw 3 with linespoints notitle, \
    '' using 0:43 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:44 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n25/n25_total.csv' using 0:39 lt 2 lw 3 with linespoints notitle, \
    '' using 0:40 lt 3 lw 3 with linespoints notitle, \
    '' using 0:41 lt 6 lw 3 with linespoints notitle, \
    '' using 0:42 lt 4 lw 3 with linespoints notitle, \
    '' using 0:43 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:44 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n50/n50_total.csv' using 0:39 lt 2 lw 3 with linespoints notitle, \
    '' using 0:40 lt 3 lw 3 with linespoints notitle, \
    '' using 0:41 lt 6 lw 3 with linespoints notitle, \
    '' using 0:42 lt 4 lw 3 with linespoints notitle, \
    '' using 0:43 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:44 lt 8 lc rgb 'red' lw 3 with linespoints notitle

#####################   Utilization 0.5   ###############################
# set title "Utilization = 0.5" font ", 16"
plot 'n5/n5_total.csv' using 0:51 lt 2 lw 3 with linespoints notitle, \
    '' using 0:52 lt 3 lw 3 with linespoints notitle, \
    '' using 0:53 lt 6 lw 3 with linespoints notitle, \
    '' using 0:54 lt 4 lw 3 with linespoints notitle, \
    '' using 0:55 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:56 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n10/n10_total.csv' using 0:51 lt 2 lw 3 with linespoints notitle, \
    '' using 0:52 lt 3 lw 3 with linespoints notitle, \
    '' using 0:53 lt 6 lw 3 with linespoints notitle, \
    '' using 0:54 lt 4 lw 3 with linespoints notitle, \
    '' using 0:55 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:56 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n25/n25_total.csv' using 0:51 lt 2 lw 3 with linespoints notitle, \
    '' using 0:52 lt 3 lw 3 with linespoints notitle, \
    '' using 0:53 lt 6 lw 3 with linespoints notitle, \
    '' using 0:54 lt 4 lw 3 with linespoints notitle, \
    '' using 0:55 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:56 lt 8 lc rgb 'red' lw 3 with linespoints notitle

plot 'n50/n50_total.csv' using 0:51 lt 2 lw 3 with linespoints notitle, \
    '' using 0:52 lt 3 lw 3 with linespoints notitle, \
    '' using 0:53 lt 6 lw 3 with linespoints notitle, \
    '' using 0:54 lt 4 lw 3 with linespoints notitle, \
    '' using 0:55 lt 1 lc rgb 'purple' lw 3 with linespoints notitle, \
    '' using 0:56 lt 8 lc rgb 'red' lw 3 with linespoints notitle
