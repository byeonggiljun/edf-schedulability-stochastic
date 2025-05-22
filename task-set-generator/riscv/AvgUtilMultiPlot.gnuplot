# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
# set key autotitle columnhead
set terminal pdfcairo enhanced size 20cm, 18cm
set output "AvgUtilRISCV.pdf"

set datafile separator ","
set multiplot layout 2, 2

xx = 0.43 # the margine between graphs
ww = 0.6 # width of graphs

# # set multiplot
set style fill solid 0.5 border -1
set boxwidth 0.85

# set xtics ('1e-7' 1, '1e-6' 2, '1e-5' 3, '1e-4' 4)
# set xtics ('1e-7' 0, '1e-6' 3, '1e-5' 6, '1e-4' 9)
# set format x ""
# set ytics ("0" 0, "0.5" 0.5, "1" 1)
# set format y ""

set xtics ('' 0, '' 1, '' 2, '' 3, '' 4, '' 5)
set ytics ("" 0, "" 0.3, "" 0.6, "" 0.9, "" 1.0)

set xrange [-0.5:6.5]
set yrange [0:1.01]

set margin 0.2, 2, 0.2, 1

##############################################
plot 'n25/n25_total.csv' every ::1::7 using ($0):42 lt 8 lc rgb 'red' w boxes notitle

plot 'n50/n50_total.csv' every ::1::7 using ($0):42 lt 8 lc rgb 'red' w boxes notitle

plot 'n25/n25_total.csv' every ::1::7 using ($0):56 lt 8 lc rgb 'red' w boxes notitle

plot 'n50/n50_total.csv' every ::1::7 using ($0):56 lt 8 lc rgb 'red' w boxes notitle

# plot 'n25/n25_total.csv' every ::1::1 using (7):40 lt 10 w boxes notitle,\
#     '' every ::1::7 using ($0):42 lt 8 lc rgb 'red' w boxes notitle

# plot 'n50/n50_total.csv' every ::1::1 using (7):40 lt 10 w boxes notitle,\
#     '' every ::1::7 using ($0):42 lt 8 lc rgb 'red' w boxes notitle

# plot 'n25/n25_total.csv' every ::1::1 using (7):54 lt 10 w boxes notitle,\
#     '' every ::1::7 using ($0):56 lt 8 lc rgb 'red' w boxes notitle

# plot 'n50/n50_total.csv' every ::1::1 using (7):54 lt 10 w boxes notitle,\
#     '' every ::1::7 using ($0):56 lt 8 lc rgb 'red' w boxes notitle