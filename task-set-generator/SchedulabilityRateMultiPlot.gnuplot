# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
set key autotitle columnhead
set terminal pdfcairo enhanced
set output 'Result.pdf'

set multiplot layout 6, 4

set style data histograms
set style histogram rowstacked

set xtics rotate by -45 nomirror
set lt 1 lc rgb 'red'
set lt 2 lc rgb 'orange-red'
set lt 3 lc rgb 'orange'
set lt 4 lc rgb 'yellow'
set lt 5 lc rgb 'green'
set lt 6 lc rgb 'blue'
set lt 7 lc rgb 'dark-blue'
set lt 8 lc rgb 'violet'

set margins 0, 0, 0, 0

set size 1, 0.1
set origin 0, 0.9
set border 0
unset tics
unset xlabel
unset ylabel
set key center center horizontal box
set xrange[0:1]
set yrange[0:1]
plot NaN lt 7 title "RTailorSuccess", \
    NaN lt 3 title "NewRTailorSuccess", \
    NaN lt 5title "PREFACESuccess" 
unset key    # Remove legend for all data plots
plot NaN notitle, \
    NaN notitle, \
    NaN notitle
plot NaN notitle, \
    NaN notitle, \
    NaN notitle
plot NaN notitle, \
    NaN notitle, \
    NaN notitle
unset xrange
unset yrange

# Reset settings for data plots
set size noratio  # Size for each subplot
set border
set tics
unset key    # Remove legend for all data plots

# set xlabel "Fault Rate ({/Symbol l})" font ", 16"
# set ylabel "Count" font ", 16"

# set label "Fault Rate ({/Symbol l})" at screen 0.5, 0.01 center
# set label "Count" rotate by 90 at screen 0.05, 0.5 center

# set label "Utilization = 0.2" at screen 0.8, 0.9
# set label "Utilization = 0.4" at screen 0.8, 0.7
# set label "Utilization = 0.6" at screen 0.8, 0.5
# set label "Utilization = 0.8" at screen 0.8, 0.3
# set label "Utilization = 1.0" at screen 0.8, 0.1

# set label 1 "Utilization = 0.2" at screen 0.9, 0.85
# set label 2 "Utilization = 0.4" at screen 0.9, 0.65
# set label 3 "Utilization = 0.6" at screen 0.9, 0.45
# set label 4 "Utilization = 0.8" at screen 0.9, 0.25
# set label 5 "Utilization = 1.0" at screen 0.9, 0.05

set label "N = 5" at screen 0.1, 0.88
set label "N = 10" at screen 0.35, 0.88
set label "N = 25" at screen 0.6, 0.88
set label "N = 50" at screen 0.85, 0.88

set style fill solid 0.5 border -1
set boxwidth 0.75
set datafile separator ","

set xtics font ", 14"
set ytics font ", 14"


# Define the lambda names on x-axis
set xtics ("1e-7/h" 0, "1e-6/h" 1, "1e-5/h" 2, "1e-4/h" 3, "1e-3/h" 4, "1e-2/h" 5, "1e-1/h" 6, "1e-1/h" 7)

# set xrange [-0.3:7.3]

unset xtics
unset ytics
set margins 0.2, 0.8, 0.4, 0

#####################   Utilization 0.1   ###############################
# set title "Utilization = 0.1" font ", 16"
plot 'n5/n5_total.csv' using 4 lt 7 title "RTailorSuccess", \
    '' using 5 lt 3 title "NewRTailorSuccess", \
    '' using 6 lt 5 title "PREFACESuccess"

plot 'n10/n10_total.csv' using 4 lt 7 title "RTailorSuccess", \
    '' using 5 lt 3 title "NewRTailorSuccess", \
    '' using 6 lt 5 title "PREFACESuccess"

plot 'n25/n25_total.csv' using 4 lt 7 title "RTailorSuccess", \
    '' using 5 lt 3 title "NewRTailorSuccess", \
    '' using 6 lt 5 title "PREFACESuccess"

plot 'n50/n50_total.csv' using 4 lt 7 title "RTailorSuccess", \
    '' using 5 lt 3 title "NewRTailorSuccess", \
    '' using 6 lt 5 title "PREFACESuccess"

#####################   Utilization 0.2   ###############################
# set title "Utilization = 0.2" font ", 16"
plot 'n5/n5_total.csv' using 12 lt 7 title "RTailorSuccess", \
    '' using 13 lt 3 title "NewRTailorSuccess", \
    '' using 14 lt 5 title "PREFACESuccess"

plot 'n10/n10_total.csv' using 12 lt 7 title "RTailorSuccess", \
    '' using 13 lt 3 title "NewRTailorSuccess", \
    '' using 14 lt 5 title "PREFACESuccess"

plot 'n25/n25_total.csv' using 12 lt 7 title "RTailorSuccess", \
    '' using 13 lt 3 title "NewRTailorSuccess", \
    '' using 14 lt 5 title "PREFACESuccess"

plot 'n50/n50_total.csv' using 12 lt 7 title "RTailorSuccess", \
    '' using 13 lt 3 title "NewRTailorSuccess", \
    '' using 14 lt 5 title "PREFACESuccess"

#####################   Utilization 0.3   ###############################
# set title "Utilization = 0.3" font ", 16"
plot 'n5/n5_total.csv' using 20 lt 7 title "RTailorSuccess", \
    '' using 21 lt 3 title "NewRTailorSuccess", \
    '' using 22 lt 5 title "PREFACESuccess"

plot 'n10/n10_total.csv' using 20 lt 7 title "RTailorSuccess", \
    '' using 21 lt 3 title "NewRTailorSuccess", \
    '' using 22 lt 5 title "PREFACESuccess"

plot 'n25/n25_total.csv' using 20 lt 7 title "RTailorSuccess", \
    '' using 21 lt 3 title "NewRTailorSuccess", \
    '' using 22 lt 5 title "PREFACESuccess"

plot 'n50/n50_total.csv' using 20 lt 7 title "RTailorSuccess", \
    '' using 21 lt 3 title "NewRTailorSuccess", \
    '' using 22 lt 5 title "PREFACESuccess"

#####################   Utilization 0.4   ###############################
# set title "Utilization = 0.4" font ", 16"
plot 'n5/n5_total.csv' using 28 lt 7 title "RTailorSuccess", \
    '' using 29 lt 3 title "NewRTailorSuccess", \
    '' using 30 lt 5 title "PREFACESuccess"

plot 'n10/n10_total.csv' using 28 lt 7 title "RTailorSuccess", \
    '' using 29 lt 3 title "NewRTailorSuccess", \
    '' using 30 lt 5 title "PREFACESuccess"

plot 'n25/n25_total.csv' using 28 lt 7 title "RTailorSuccess", \
    '' using 29 lt 3 title "NewRTailorSuccess", \
    '' using 30 lt 5 title "PREFACESuccess"

plot 'n50/n50_total.csv' using 28 lt 7 title "RTailorSuccess", \
    '' using 29 lt 3 title "NewRTailorSuccess", \
    '' using 30 lt 5 title "PREFACESuccess"

#####################   Utilization 0.5   ###############################
# set title "Utilization = 0.5" font ", 16"
plot 'n5/n5_total.csv' using 36 lt 7 title "RTailorSuccess", \
    '' using 37 lt 3 title "NewRTailorSuccess", \
    '' using 38 lt 5 title "PREFACESuccess"

plot 'n10/n10_total.csv' using 36 lt 7 title "RTailorSuccess", \
    '' using 37 lt 3 title "NewRTailorSuccess", \
    '' using 38 lt 5 title "PREFACESuccess"

plot 'n25/n25_total.csv' using 36 lt 7 title "RTailorSuccess", \
    '' using 37 lt 3 title "NewRTailorSuccess", \
    '' using 38 lt 5 title "PREFACESuccess"

plot 'n50/n50_total.csv' using 36 lt 7 title "RTailorSuccess", \
    '' using 37 lt 3 title "NewRTailorSuccess", \
    '' using 38 lt 5 title "PREFACESuccess"
