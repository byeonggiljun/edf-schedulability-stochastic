# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
set key autotitle columnhead
set terminal pdfcairo enhanced # size 20 cm, 15 cm 
set output "AvgUtilkey.pdf"

set datafile separator ","
# set multiplot layout 2, 2

xx = 1.29 # the margine between graphs
xxx = 0.43
ww = 0.6 # width of graphs

# # set multiplot
set style fill solid 0.5 border -1
set boxwidth 0.85

set xtics ('' 0, '' 4, '' 8, '' 12)
set ytics ("" 0, "" 0.3, "" 0.6, "" 0.9, "" 1.0)

# set xrange [0:7]
set yrange [0:0.51]

set margin 0.2, 0.2, 0.2, 1

set key outside horizontal
set tmargin 10
set key spacing 1.5

set key font ", 24"
#####################################################
plot 'n25/n25_total.csv' every ::1::4 using (4*$0-xx):9 lt 3 w boxes title "Reghenzani {/Times-Italic et al.} considering SDC",\
    '' every ::1::4 using (4*$0-xxx):10 lt 4 w boxes title "RTailor considering SDC", \
    '' every ::1::4 using (4*$0+xxx):11 lt 10 w boxes title "TMR", \
    '' every ::1::4 using (4*$0+xx):12 lt 8 lc rgb 'red' w boxes title "PREFACE"