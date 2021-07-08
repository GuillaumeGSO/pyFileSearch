# pyFileIndexer
Simple tool to index filenames on a directory and search tool

My comments in french for a fresh start
- [ ] TODO : everything in english
- [ ] TODO : cleaner code about --output options
- [ ] TODO : code separation between main, interface, index file handling...
- [ ] TODO : add interactive mode if index file or path name not provided ?

Indexation et recherche par wildcard (* et ?) sur des noms de fichiers
#Exemples : 

1 - indexer mon disque dur :
>python file_dir.py -index "lecteurC" -path "c:\"

un fichier d'index lecteurC.pbz2 sera générer (compressé)

2 - recherche tous les fichiers log
>python file_dir.py -find "*.log" -i "lecteurC"

le fichier d'index lu doit se nommer lecteurC.pbz2


## Usage : 
 * -h ou --help : affiche l'aide
 * -v ou --verbose : affiche plus d'information sur la sortie standard

### Mode indexation : 2 paramètres obligatoires
 * -p ou --path <pathname>: chemin à indexer
 * -i ou --index <indexfilename> : lance l'indexation de <pathname> et écrit l'indexe dans <indexfilename>

### Mode recherche : 2 paramètres obligatoires *****
* -f ou --find <search>: recherche dans le fichier d'index <indexfilename> les noms de fichiers qui correspondent :
       ** *.xls : tous les fichiers Excel
       ** *202?.log : tous les fichiers .log comme fic2020.log, param2021.log, etc 
* -i ou --index <indexfilename> : utilise le fichier d'index <indexfilename> (obligatoire)
* -o ou --output <ouputfilename>: écrire le résultat de la recherche dans le fichier <ouputfilename>
        (ignoré si pas en mode recherche)
