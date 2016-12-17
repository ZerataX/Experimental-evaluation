#!/bin/bash

if [ ${#@} != 1 ]; then
	echo please give one configuration file\nEg: bash regression.sh example.conf
else
	#define relative path
	config_path=$@
	config_dir=$(dirname "${config_path}")
	config_name=$(basename "${config_path}")
	config_name=$(echo $config_name | cut -f 1 -d '.')
	if [ "${config_dir}" != "" ]; then
		config_dir+="/"
	fi

	#load config
	while read line; do
		stringarray=(${line})
		echo ${stringarray[@]:1}
		eval ${stringarray[0]}="${stringarray[@]:1}"
	done < $config_path

	#use python to calculate values
	python regression.py $config_path

	#assign values to variables
	while read line; do
		stringarray=(${line})
		eval ${stringarray[0]}=${stringarray[1]}
	done < ${config_dir}${config_name}.vars

	#start plotting the regression
	gnuplot <<- EOF
		#!/usr/bin/gnuplot
		reset

		set terminal cairolatex color standalone pdf size 16.5cm, 10cm dashed transparent \
		header '\newcommand{\hl}[1]{\setlength{\fboxsep}{0.5pt}\colorbox{white}{#1}}'
		set output '${config_dir}${config_name}.tex'

		round(x) = x - floor(x) < 0.5 ? floor(x) : ceil(x)
		round2(x, n) = round(x*10**n)*10.0**(-n)

		ydistance = ${ydistance}
		slope = ${slope}
		slope_rounded = round2(slope, 2)

		unset key
		set grid
		set ytics
		set xtics

		set xtics font "Helvetica,02"
		set ytics font "Helvetica,02"


		set xlabel "${label_regression_x}"
		set ylabel "${label_regression_y}"
		set xrange [${lower}:${upper}]
		set yrange [${y_start_regression}:]


		set style data points

		set key left box height "2cm" width "4cm"
		if (${slope_bool} == 1) {
			set label sprintf("\$m=%g${label_slope}$", slope_rounded) right at graph ${slope_x}, graph ${slope_y}
		}

		P(x) = x*slope+ydistance

		if (${fit_bool} == 1 ) {
			plot P(x) title "gefittet" linecolor rgb '${label_color_1}',  \
				"${config_dir}${config_name}.dat" using 1:2 with points title "gemessen" linecolor rgb '${label_color_2}'
		}else{
			plot "${config_dir}${config_name}.dat" using 1:2:3 with yerrorbars title "gemessen" linecolor rgb '${label_color_2}'
		}
		# vim: set tw=200:
	EOF
	xelatex ${config_dir}${config_name}.tex
	rm ${config_dir}*.aux
	rm ${config_dir}*.log
	rm ${config_dir}*.dvi
	rm ${config_dir}*inc.pdf
	rm ${config_dir}*.tex
	rm ${config_dir}*.vars
	rm *.aux
	rm *.log
	rm *.dvi
	rm *inc.pdf
	rm *.tex
	rm *.vars
fi
