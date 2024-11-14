# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
set key autotitle columnhead
set terminal pdfcairo enhanced

set xlabel "Fault Rate ({/Symbol l})" font ", 16"
set ylabel "Count" font ", 16"
# set grid
set key top center horizontal outside
set key box

set xtics rotate by -45 nomirror
set lt 1 lc rgb 'red'
set lt 2 lc rgb 'orange-red'
set lt 3 lc rgb 'orange'
set lt 4 lc rgb 'yellow'
set lt 5 lc rgb 'green'
set lt 6 lc rgb 'blue'
set lt 7 lc rgb 'dark-blue'
set lt 8 lc rgb 'violet'

set style data histograms
set style histogram rowstacked

set style fill solid 0.5 border -1
set boxwidth 0.75
set datafile separator ","

set xtics font ", 14"
set ytics font ", 14"


# Define the lambda names on x-axis
set xtics ("1e-5/h" 0, "1e-4/h" 1, "1e-3/h" 2, "1e-2/h" 3, "1e-1/h" 4, "1e-2/min" 5, "1e-1/min" 6, "1e-1/sec" 7)

set xrange [-0.3:7.3]
# set yrange [-0.03:1.03]

#####################   N5   ###############################
set output 'n5_success_rate_ut_2.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n5/n5_total.csv' using 3 lt 1 title "Infeasible", \
    '' using 4 lt 3 title "RTailorSuccess", \
    '' using 5 lt 5 title "FeasiblePREFACE", \
    '' using 6 lt 7 title "InfeasiblePREFACE"

set output 'n5_success_rate_ut_4.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n5/n5_total.csv' using 10 lt 1 title "Infeasible", \
    '' using 11 lt 3 title "RTailorSuccess", \
    '' using 12 lt 5 title "FeasiblePREFACE", \
    '' using 13 lt 7 title "InfeasiblePREFACE"

set output 'n5_success_rate_ut_6.pdf'
set title "Utilization = 0.4" font ", 16"
plot 'n5/n5_total.csv' using 17 lt 1 title "Infeasible", \
    '' using 18 lt 3 title "RTailorSuccess", \
    '' using 19 lt 5 title "FeasiblePREFACE", \
    '' using 20 lt 7 title "InfeasiblePREFACE"

set output 'n5_success_rate_ut_8.pdf'
set title "Utilization = 0.8" font ", 16"
plot 'n5/n5_total.csv' using 24 lt 1 title "Infeasible", \
    '' using 25 lt 3 title "RTailorSuccess", \
    '' using 26 lt 5 title "FeasiblePREFACE", \
    '' using 27 lt 7 title "InfeasiblePREFACE"

set output 'n5_success_rate_ut_10.pdf'
set title "Utilization = 1.0" font ", 16"
plot 'n5/n5_total.csv' using 31 lt 1 title "Infeasible", \
    '' using 32 lt 3 title "RTailorSuccess", \
    '' using 33 lt 5 title "FeasiblePREFACE", \
    '' using 34 lt 7 title "InfeasiblePREFACE"

#####################   N10   ###############################
set output 'n10_success_rate_ut_2.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n10/n10_total.csv' using 3 lt 1 title "Infeasible", \
    '' using 4 lt 3 title "RTailorSuccess", \
    '' using 5 lt 5 title "FeasiblePREFACE", \
    '' using 6 lt 7 title "InfeasiblePREFACE"

set output 'n10_success_rate_ut_4.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n10/n10_total.csv' using 10 lt 1 title "Infeasible", \
    '' using 11 lt 3 title "RTailorSuccess", \
    '' using 12 lt 5 title "FeasiblePREFACE", \
    '' using 13 lt 7 title "InfeasiblePREFACE"

set output 'n10_success_rate_ut_6.pdf'
set title "Utilization = 0.4" font ", 16"
plot 'n10/n10_total.csv' using 17 lt 1 title "Infeasible", \
    '' using 18 lt 3 title "RTailorSuccess", \
    '' using 19 lt 5 title "FeasiblePREFACE", \
    '' using 20 lt 7 title "InfeasiblePREFACE"

set output 'n10_success_rate_ut_8.pdf'
set title "Utilization = 0.8" font ", 16"
plot 'n10/n10_total.csv' using 24 lt 1 title "Infeasible", \
    '' using 25 lt 3 title "RTailorSuccess", \
    '' using 26 lt 5 title "FeasiblePREFACE", \
    '' using 27 lt 7 title "InfeasiblePREFACE"

set output 'n10_success_rate_ut_10.pdf'
set title "Utilization = 1.0" font ", 16"
plot 'n10/n10_total.csv' using 31 lt 1 title "Infeasible", \
    '' using 32 lt 3 title "RTailorSuccess", \
    '' using 33 lt 5 title "FeasiblePREFACE", \
    '' using 34 lt 7 title "InfeasiblePREFACE"

#####################   N25   ###############################
set output 'n25_success_rate_ut_2.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n25/n25_total.csv' using 3 lt 1 title "Infeasible", \
    '' using 4 lt 3 title "RTailorSuccess", \
    '' using 5 lt 5 title "FeasiblePREFACE", \
    '' using 6 lt 7 title "InfeasiblePREFACE"

set output 'n25_success_rate_ut_4.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n25/n25_total.csv' using 10 lt 1 title "Infeasible", \
    '' using 11 lt 3 title "RTailorSuccess", \
    '' using 12 lt 5 title "FeasiblePREFACE", \
    '' using 13 lt 7 title "InfeasiblePREFACE"

set output 'n25_success_rate_ut_6.pdf'
set title "Utilization = 0.4" font ", 16"
plot 'n25/n25_total.csv' using 17 lt 1 title "Infeasible", \
    '' using 18 lt 3 title "RTailorSuccess", \
    '' using 19 lt 5 title "FeasiblePREFACE", \
    '' using 20 lt 7 title "InfeasiblePREFACE"

set output 'n25_success_rate_ut_8.pdf'
set title "Utilization = 0.8" font ", 16"
plot 'n25/n25_total.csv' using 24 lt 1 title "Infeasible", \
    '' using 25 lt 3 title "RTailorSuccess", \
    '' using 26 lt 5 title "FeasiblePREFACE", \
    '' using 27 lt 7 title "InfeasiblePREFACE"

set output 'n25_success_rate_ut_10.pdf'
set title "Utilization = 1.0" font ", 16"
plot 'n25/n25_total.csv' using 31 lt 1 title "Infeasible", \
    '' using 32 lt 3 title "RTailorSuccess", \
    '' using 33 lt 5 title "FeasiblePREFACE", \
    '' using 34 lt 7 title "InfeasiblePREFACE"

#####################   N50   ###############################
set output 'n50_success_rate_ut_2.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n50/n50_total.csv' using 3 lt 1 title "Infeasible", \
    '' using 4 lt 3 title "RTailorSuccess", \
    '' using 5 lt 5 title "FeasiblePREFACE", \
    '' using 6 lt 7 title "InfeasiblePREFACE"

set output 'n50_success_rate_ut_4.pdf'
set title "Utilization = 0.2" font ", 16"
plot 'n50/n50_total.csv' using 10 lt 1 title "Infeasible", \
    '' using 11 lt 3 title "RTailorSuccess", \
    '' using 12 lt 5 title "FeasiblePREFACE", \
    '' using 13 lt 7 title "InfeasiblePREFACE"

set output 'n50_success_rate_ut_6.pdf'
set title "Utilization = 0.4" font ", 16"
plot 'n50/n50_total.csv' using 17 lt 1 title "Infeasible", \
    '' using 18 lt 3 title "RTailorSuccess", \
    '' using 19 lt 5 title "FeasiblePREFACE", \
    '' using 20 lt 7 title "InfeasiblePREFACE"

set output 'n50_success_rate_ut_8.pdf'
set title "Utilization = 0.8" font ", 16"
plot 'n50/n50_total.csv' using 24 lt 1 title "Infeasible", \
    '' using 25 lt 3 title "RTailorSuccess", \
    '' using 26 lt 5 title "FeasiblePREFACE", \
    '' using 27 lt 7 title "InfeasiblePREFACE"

set output 'n50_success_rate_ut_10.pdf'
set title "Utilization = 1.0" font ", 16"
plot 'n50/n50_total.csv' using 31 lt 1 title "Infeasible", \
    '' using 32 lt 3 title "RTailorSuccess", \
    '' using 33 lt 5 title "FeasiblePREFACE", \
    '' using 34 lt 7 title "InfeasiblePREFACE"
