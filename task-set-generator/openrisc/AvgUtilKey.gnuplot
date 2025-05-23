# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
set key autotitle columnhead
set terminal pdfcairo enhanced # size 20 cm, 15 cm 
set output "AvgUtilkey.pdf"

set datafile separator ","
# set multiplot layout 2, 2

xx = 0.43 # the margine between graphs
ww = 0.8 # width of graphs

# # set multiplot
set style fill solid 0.5 border -1
set boxwidth 0.85

set xtics ('' 0, '' 1, '' 2, '' 3, '' 4, '' 5, '' 6)
set ytics ("" 0, "" 0.3, "" 0.6, "" 0.9, "" 1.0)

set xrange [-0.5:7.5]
set yrange [0:1.01]

set margin 0.2, 0.2, 0.2, 1

set key outside horizontal
set tmargin 10
set key spacing 1.5

set key font ", 24"
#####################################################
plot 'n25/n25_total.csv' every ::0::0 using (7):40 lt 10 w boxes title "TMR", \
    '' every ::0::6 using ($0):42 lt 8 lc rgb 'red' w boxes title "PREFACE"