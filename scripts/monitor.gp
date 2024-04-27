set terminal pdfcairo enhanced color dashed font "Alegreya, 14" \
rounded size 16 cm, 9.6 cm

# Default encoding, line styles, pallette, border and grid are set in
# /usr/local/share/gnuplot/x.y/gnuplotrc.

set grid
#set key left top
set key right bottom
set output 'job.pdf'

set multiplot title "cvg and sta of “job”" layout 2,1 downwards

set xlabel ''
#set format x ''
set lmargin 10
set logscale y
unset mytics
set format y '%H'
x = 0.
plot 'job.sta' skip 2 using (x=x+$4):($7 == 0 ? 1e-7 : $7) w l ls 2 title "dt", \
'job.cvg' skip 4 using 0:($6 == 0 ? 1e-7 : $6) w l ls 3 title "force", \
'' skip 4 using 0:7 w l ls 1 title "disp"

unset logscale
set xlabel "iteration"
set y2label "step time"
set ylabel "# of cont. elements"

x = 0.
plot 'job.cvg' skip 4 using 0:5 w l ls 1 title "# cont. el.", \
'job.sta' skip 2 using (x=x+$4):5 w l ls 2 axes x1y2 title "step time"

unset multiplot
