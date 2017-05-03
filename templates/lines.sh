#!/bin/bash
filename=${1%.csv}
gnuplot <<- EOF
  #!/usr/bin/gnuplot
  reset
  set encoding utf8

  set terminal cairolatex color standalone pdf size 16.5cm, 10cm dashed transparent \
  header '\newcommand{\hl}[1]{\setlength{\fboxsep}{0.5pt}\colorbox{white}{#1}} \
  \usepackage{siunitx} \sisetup{separate-uncertainty, multi-part-units = brackets} \
\sisetup{exponent-product = \cdot, output-product = \cdot} \
\sisetup{range-phrase=-}'
  set output '${filename}.tex'

  round(x) = x - floor(x) < 0.5 ? floor(x) : ceil(x)
	round2(x, n) = round(x*10**(n))*10.0**(-n)
	round3(x, n) = round(x*10**(n))

  unset key
  set grid
  set ytics
  set xtics

  set xtics font "Helvetica,02"
  set ytics font "Helvetica,02"

  set ylabel "\$U_A\\\, \\\mathrm{in \\\, \\\si{\\\volt}}\$" # rotate by 0
  set xlabel "\$U_B\\\, \\\mathrm{in \\\, \\\si{\\\volt}}\$"

  set key left Left reverse width -35 height 3.8
  set key font ",15"
  set datafile separator ","

  plot "${filename}.csv" using (\$1)*10:(\$2):(\$1-(\$3)/sqrt(6))*10:(\$1+(\$3)/sqrt(6))*10:(\$2-(\$4)/sqrt(6)):(\$2+(\$4)/sqrt(6)) with xyerrorbars title 'Messdaten' linecolor rgb '#dc322f'
EOF
