import os
import pickle
import bz2
import fnmatch

def findFilesInSet(my_set, my_search):
    for item in my_set:
        # File Name match : permet d'utiliser des * ou ? (plus simple que des regexp)
        # For now it is case sensitive
        if fnmatch.fnmatch(item.split(os.path.sep)[-1], my_search):
            yield item


def read_index_file(my_index_file):
    trace(f'Uncompressing & Reading index file : {my_index_file}')
    data = bz2.BZ2File(my_index_file + '.pbz2', 'rb')
    myset = pickle.load(data)
    trace(f'Return un set de longueur : {len(myset)}')
    return myset

def trace(trc):
    print(trc)