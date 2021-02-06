#!/usr/bin/python3

from urllib.parse import urlparse
import base64
import bs4
import getopt
import magic
import os
import sys

def is_url(url):
    return urlparse(url).scheme in ('http', 'https')

def main(argv):
    # debug verbose output
    enable_verbose = False
    def verbose(text):
        if enable_verbose:
            print(text)

    # fetch command line arguments
    try:
        opts, args = getopt.getopt(argv, "vhi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("encoder.py -i <input html file> -o <output html file> [-v]")
        sys.exit(2)

    inputfile = ""
    outputfile = ""

    # decode arguments
    for opt, arg in opts:
        if opt == "-h":
            print("encoder.py -i <input html file> -o <output html file> [-v]")
            sys.exit()
        elif opt == "-v":
            enable_verbose = True
            verbose("Running the script in verbose.")
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # ensure input/output path given
    if not inputfile or not outputfile:
        print("encoder.py -i <input html file> -o <output html file> [-v]")
        sys.exit(2)

    verbose("Input file: " + inputfile)
    verbose("Output file: " + outputfile)

    # open and interpret the html file (read only)
    with open(inputfile, "r") as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, 'lxml')

    mime = magic.Magic(mime=True)

    # modify all the media tags
    for mediaTag in soup.findAll(['img', 'video', 'source']):
        if not mediaTag.has_attr('src'):
            verbose("The media tag doesn't have a source. Doing nothing...")
            continue

        verbose("Looking at media tag with src: " + mediaTag['src'])

        if is_url(mediaTag['src']):
            verbose("\tThe source is external. Doing nothing...")
            continue

        try:
            # get the correct path to the image file
            infPath = os.path.join(os.path.dirname(inputfile), mediaTag['src'])

            # we need the MIME type when creating the data URL
            mimeString = mime.from_file(infPath)
            verbose("\tMimetype: " + mimeString)
            # we also need a base64 encoding of the binary file
            with open(infPath, "rb") as inf:
                b64dataString = base64.b64encode(inf.read()).decode('ascii')

            data_url = f"data:{mimeString};base64,{b64dataString}"
        except OSError:
            print("\tCould not open/read the file: " + infPath)
            print("\tSetting the 'src' to NULL.")
            data_url = ""
            if not mediaTag['alt']:
                mediaTag['alt'] = "[Unavailable media]"

        # modify the source to not be dependent on internal files
        mediaTag['src'] = data_url

    # save the modified file to specified output
    with open(outputfile, "w") as outf:
        outf.write(str(soup))

if __name__ == "__main__":
    main(sys.argv[1:])


