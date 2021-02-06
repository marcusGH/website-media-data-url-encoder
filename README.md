# Website Media Data Url Encoder

A script that embeds media files, stored locally with the html file, into the html file itself such that it's more portable.

## Usage

Use the script as follows:

    ./encoder.py -i <input html file> -o <output html file> [-v]

Specify a path to the html file to be simplified after the `-i` flag and specify the location of the output file after the `-o` flag. The `-v` flag enables verbose debug information.

Example:

    ./encoder.py -i test_html/index.html -o output_html.html

## Dependencies

The following python modules are needed:

* urllib
* base64
* bs4
* getopt
* magic
* os
* sys
