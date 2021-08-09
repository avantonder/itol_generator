# itol_generator

Script for generating metadata strip files for iTOL from csv file of metadata.

# Usage:

python iTOL_generator.py -i metadata.csv -m "#a0a0a0"

optional arguments:

-h, --help            show this help message and exit
  
--input INPUT, -i INPUT Input file in csv format (sample names in first column)

--missing_colour MISSING_COLOUR, -m MISSING_COLOUR  Colour to use for missing data (Hexadecimal code).  (default = white ("#ffffff")) [OPTIONAL]
