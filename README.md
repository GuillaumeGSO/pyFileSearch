# pyFileSearch
Simple GUI tool to search from filename using a file index generated by pyFileIndexer

My comments in french for a fresh start
- [x] TODO : everything in english
- [ ] TODO : code separation between main, interface, index file handling...

## Search mode
* -i ou --index <indexfilename> : set the index file name to use <indexfilename>, default "index.pbz2"
       Note : the index file has to be generated by pyFileIndexer (no extension required is the argument)

## Build an executable
install pyinstaller with the command :
 * pip install pyinstaller

build the executable:
 * pyinstaller ./pyFileSearch.py --onefile -w
 Options : 
       - onefile : generates only one .exe executable file with all included
       - w : hide the console window at run time 
 * or use the pyFileSearch.spec
## Use the executable
Do not forget to copy the index file (index.pbz2) next to the executable file

[ ] TODO : the executable cannot accept arguments to define the index file name yet.