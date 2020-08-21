#!/usr/bin/env python

import os, argparse, sys
import pandas as pd

def parse_args(args):

	global _parser

	_parser = argparse.ArgumentParser(description = 'iTol_generator.py: a tool for generating iTOL datastrip files from a csv file')
	_parser = argparse.ArgumentParser(description = 'Example usage: python iTol_generator.py -i metadata.csv -m "#a0a0a0"')
	_parser.add_argument('--input', '-i', help='Input file in csv format (sample names in first column)')
	_parser.add_argument('--missing_colour', '-m', help='Colour to use for missing data (Hexadecimal code). (default = white ("#ffffff")) [OPTIONAL]')
	
	opts = _parser.parse_args(args)

	return opts

def main(opts):

	if not opts.missing_colour:
		missing_colour = "#ffffff"
	else:
		missing_colour = str(opts.missing_colour)

	colour_list = ['#0000cc','#ff0000','#ff6600','#aaffaa','#9900ff','#66ffff','#ff66cc','#006600','#ffff00','#9999ff','#996600','#663366','#99cc66',
                '#c4dc00','#660000','#666600','#cc9933','#99cc00','#cc99ff','#ccccff','#ffcc66','#336666','#000066','#666666','#663300','#1dc39f',
                '#ddff33','#ffd700','#ffac2a','#c4dc00','#8f007f','#444c04','#e8ff2a','#8f0038','#388f00','#dc00c4','#1dc34f','#c34c1d','#ff6666',
                '#ffcccc','#0000ff','#6666ff','#adad85','#40bf80','#009900','#00cc00','#00ff00','#33ff33','#66ff66','#9900cc','#bf00ff','#cc33ff',
                '#ff9900','#ffad33','#ffc266','#663300','#994d00','#cc6600','#4d2600','#993333']

	file_header = 'DATASET_COLORSTRIP' + '\n' + 'SEPARATOR' + ' ' + 'TAB' + '\n'
	
	strip_details = 'STRIP_WIDTH' + '\t' + '50' + '\n' + 'MARGIN' + '\t' + '10' + '\n' + 'BORDER_WIDTH' + '\t' + '5' + '\n' + 'BORDER_COLOR' + '\t' + '#000000' + '\n' + 'DATA' + '\n'

	csv_file = pd.read_csv(opts.input).fillna('Missing')

	sample_names = csv_file.iloc[:,:1]

	csv_headers = list(csv_file.iloc[:,1:].columns.values)

	new_df = list()

	for i in csv_headers:
		new_df.append(pd.concat([sample_names, csv_file[i]], axis = 1))

	header_summaries = [csv_file[i].value_counts() for i in csv_headers]

	summary_df = [i.rename_axis(i.name).reset_index(name='Freq') for i in header_summaries]

	for df in summary_df:
		df['colour'] = colour_list[0:len(df)]
		df['shape'] = 1

	for df, header in zip(summary_df, csv_headers):
		df.loc[df[header].astype(str) == "Missing", 'colour'] = missing_colour

	new_df_coloured = list()

	for df, i, j in zip(new_df, csv_headers, summary_df):
			new_df_coloured.append(pd.merge(df, j[[i, 'colour']], left_on = i, right_on = i, how = 'left'))

	output_df = list()

	for df, header in zip(new_df_coloured, csv_headers):
		output_df.append(df[[df.columns.values[0], 'colour', df.columns.values[1]]])

	datastrip_filenames = [i + "_iTOL_datastrip.txt" for i in csv_headers]

	datastrip_labels = ['DATASET_LABEL' + '\t' + i  + '\n' for i in csv_headers]

	legend_title = ['LEGEND_TITLE' + '\t' + i  + '\n' for i in csv_headers]

	legend_shapes = ['LEGEND_SHAPES' + '\t' + i['shape'].to_csv(index = False, sep = '\t').replace('\n', '\t')  + '\n' for i in summary_df]

	legend_colours = ['LEGEND_COLORS' + '\t' + i['colour'].to_csv(index = False, sep = '\t').replace('\n', '\t')  + '\n' for i in summary_df]

	legend_labels = ['LEGEND_LABELS' + '\t' + i[i.columns.values[0]].to_csv(index = False, sep = '\t').replace('\n', '\t')  + '\n' for i in summary_df]

	output_df_formatted = [i.to_csv(index = False, header = False, sep = '\t') for i in output_df]

	for file, label, title, shape, colour, legend, df in zip(datastrip_filenames, datastrip_labels, legend_title,
		legend_shapes, legend_colours, legend_labels, output_df_formatted):
		file_out = open(file, 'w')
		file_out.write(file_header)
		file_out.write(label)
		file_out.write(title)
		file_out.write(shape)
		file_out.write(colour)
		file_out.write(legend)
		file_out.write(strip_details)
		file_out.write(df)

if __name__ == "__main__":
  opts= parse_args(sys.argv[1:])
  main(opts)
