"""
Search uility getting results from index files made with pyFileIndexer
"""
import sys
import getopt
from filesearch.gui import construct_interface
from filesearch.file_parser import read_index_file

VERBOSE = False

def main():
    """
    GUI for searching and opening indexed file from pyFileIndexer

    Exemples :
    Open the GUI for searching, the index file must be name "index.pbz2"
        >>python file_dir.py
    Let the user choose the index file name (lecteurC.pbz2)
        >>python file_dir.py -i "lecteurC"

    Usage :

    ***** Search mode : 1 optional parameter
    -i ou --index <indexfilename> : utilise le fichier d'index <indexfilename>
    "index" will be used if not specified
    """
    index_filename = 'index'

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "i:"
    long_options = ["index="]

    try:
        arguments, _ = getopt.getopt(
            argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    # Evaluate given options
    for current_argument, current_value in arguments:
        if current_argument in ("-i", "--index"):
            index_filename = current_value
    #Read the index file
    try:
        my_set = read_index_file(index_filename)
    except:
        print("Unable to read index file")
        sys.exit(2)


    # Launch GUI
    construct_interface(my_set)
    sys.exit(1)
