#!/bin/bash

function join_by { local d=$1; shift; echo -n "$1"; shift; printf "%s" "${@/#/$d}"; }

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
	python variables.py $config_path


	#load values from csv files
	for filename in ${config_dir}*.csv; do
		filename=${filename%.csv}

		#assign these values to variables
		while read line; do
			stringarray=(${line})
			eval ${stringarray[0]}=${stringarray[1]}
		done < ${config_dir}${filename}.vars
		#start plotting the histogram
		gnuplot <<- EOF
			reset
			set encoding utf8

			set terminal cairolatex color standalone pdf size 16.5cm, 10cm dashed transparent \
			header '\newcommand{\hl}[1]{\setlength{\fboxsep}{0.5pt}\colorbox{white}{#1}}'
			set output '${config_dir}${filename}.tex'

			round(x) = x - floor(x) < 0.5 ? floor(x) : ceil(x)
			round2(x, n) = round(x*10**n)*10.0**(-n)

			n = ${bars} # anzahl bins
			max = ${max} # maximaler wert
			min = ${min} # minimaler wert
			tics = (max - min)/5
			rounded_tics = round2(tics, ($round_to_n-1))
			rows = ${rows} # anzahl messwerte
			sigma = ${sigma} # standardabweichung
			mu = ${mu} # mittelwert
			ceil = ${upper} # Intervall
			floor = ${lower} #


			set key bmargin center height "2cm"
			set key spacing 2

			# gaussverteilung:
			gauss(x) = 1. / (sigma * sqrt(2 * pi)) * exp((-1/2.)*(((x - mu)/(sigma))**2))

			# breite der bins
			width = (max - min) / n

			# histogrammfunktion für gnuplot
			hist(x, width) = width * floor(x / width) + width / 2.0

			# ein paar gnuplot-einstellungen
			set tics out
			set xrange [floor:ceil]
			set yrange [0:]
			set grid
			set xtics min, rounded_tics, max
			set boxwidth width * 0.5
			set style fill solid 0.5
			set tics out nomirror
			set xlabel "${label_histogram_x}"
			set ylabel "${label_histogram_y}"
			#set format x "%g"
			#set format y "%g %%"

			plot "<(sed -e 's/,.*$//g' ${filename}.csv)" using (hist(\$1, width)):(100.0 / rows) smooth freq w boxes lc rgb"${label_color_2}" notitle, \
			gauss(x) * width * 100.0 title '\hl{\large $\frac{1}{\sqrt{2\pi\sigma^2}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$\\ $,\sigma \approx ${sigmaround}$}\\ $,\mu \approx {$muround}$' lc rgb"${label_color_1}" lw 2
		EOF
		echo ${config_dir}${filename}.tex
		xelatex ${config_dir}${filename}.tex
	done
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
