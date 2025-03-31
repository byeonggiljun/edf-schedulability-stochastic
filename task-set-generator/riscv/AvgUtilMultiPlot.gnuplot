# set terminal pdfcairo enhanced crop color size 40.0,30.0 solid linewidth 4 font "Helvetica, 270"
# set key autotitle columnhead
set terminal pdfcairo enhanced size 20cm, 18cm
set output "AvgUtilRISCV.pdf"

set datafile separator ","
set multiplot layout 2, 2

xx = 0.8 # the margine between graphs
ww = 0.7 # width of graphs

# # set multiplot
set style fill solid 0.5 border -1
set boxwidth 0.85

# set xtics ('1e-7' 1, '1e-6' 2, '1e-5' 3, '1e-4' 4)
# set xtics ('1e-7' 0, '1e-6' 3, '1e-5' 6, '1e-4' 9)
# set format x ""
# set ytics ("0" 0, "0.5" 0.5, "1" 1)
# set format y ""

set xtics ('' 0, '' 3, '' 6, '' 9)
set ytics ("" 0, "" 0.1, "" 0.2, "" 0.3, "" 0.4, "" 0.5)

# set xrange [0:7]
set yrange [0:0.51]

set margin 0.2, 2, 0.2, 1

##############################################
plot 'n25/n25_total.csv' every ::1::4 using (3*$0-xx):8 lt 3 w boxes notitle,\
    '' every ::1::4 using (3*$0):9 lt 4 w boxes notitle, \
    '' every ::1::4 using (3*$0+xx):10 lt 8 lc rgb 'red' w boxes notitle
    # '' u 0:38:(sprintf("%.5f", $38)) w labels offset 0,1.4 font ",12" notitle,\

plot 'n50/n50_total.csv' every ::1::4 using (3*$0-xx):8 lt 3 w boxes notitle,\
    '' every ::1::4 using (3*$0):9 lt 4 w boxes notitle, \
    '' every ::1::4 using (3*$0+xx):10 lt 8 lc rgb 'red' w boxes notitle

plot 'n25/n25_total.csv' every ::1::4 using (3*$0-xx):28 lt 3 w boxes notitle,\
    '' every ::1::4 using (3*$0):29 lt 4 w boxes notitle, \
    '' every ::1::4 using (3*$0+xx):30 lt 8 lc rgb 'red' w boxes notitle

plot 'n50/n50_total.csv' every ::1::4 using (3*$0-xx):28 lt 3 w boxes notitle,\
    '' every ::1::4 using (3*$0):29 lt 4 w boxes notitle, \
    '' every ::1::4 using (3*$0+xx):30 lt 8 lc rgb 'red' w boxes notitle
