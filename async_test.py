import PySimpleGUI as sg
import asyncio
import random
import sys
import os
from File_dir.file_parser import findFilesInSet
import bz2
import pickle

__SEARCHING__ = False
__INTERRUPT__ = False


def read_index_file(my_index_file):
    data = bz2.BZ2File(my_index_file + '.pbz2', 'rb')
    myset = pickle.load(data)
    return myset


lst = []
layout = [
    [sg.InputText(key="-INPUT-", enable_events=True),
     sg.Text(len(lst), size=(10, 1), key="-NB-")],
    [sg.Listbox(values=lst, size=(140, 30),
                key="-RESULT-", tooltip="double click to open", bind_return_key=True), ],
    [sg.Text(size=(10, 1), key='-TEMP-')],
    [sg.Exit()]
]
window = sg.Window('Py Simple Indexer', layout, finalize=True)
print("Début Lecture index file done")
my_set = read_index_file("index")
print("Fin Lecture index file done")


async def background():
    search = ''
    while True:
        tirage = random.randint(2, 20000000000)
        # print(tirage)
        window['-TEMP-'].update(tirage)
        if window['-INPUT-'].get() != search:
            search = window['-INPUT-'].get()
            print(search)
            lst.clear()
            window['-NB-'].update(0)
            i = 0
            for r in findFilesInSet(my_set, search):
                i += 1
                lst.append(r)
                global __SEARCHING__
                global __INTERRUPT__
                if __SEARCHING__ and __INTERRUPT__:
                    __INTERRUPT__ = False
                    break
                __SEARCHING__ = True
                if i % 100 == 0:
                    window['-RESULT-'].update(lst)
                    window['-NB-'].update(len(lst))
                await asyncio.sleep(0)
            __SEARCHING__ = False
            __INTERRUPT__= False
            window['-RESULT-'].update(lst)
            window['-NB-'].update(len(lst))
        await asyncio.sleep(0.001)


async def ui():
    last_search = ''
    global __INTERRUPT__
    global __SEARCHING__
    # Event Loop to process "events"
    while True:
        event, values = window.read(timeout=1)
        if event in (sg.WIN_CLOSED, 'Exit'):
            sys.exit()
        elif event == '-INPUT-':
            if last_search != values['-INPUT-']:
                window['-RESULT-'].update([])
                last_search = values['-INPUT-']
                if __SEARCHING__:
                    __INTERRUPT__ = True
        elif event == '-RESULT-':
            file_clicked = values['-RESULT-'][0]
            if __SEARCHING__:
                    __INTERRUPT__ = True
            os.startfile(file_clicked)
        elif event == '__TIMEOUT__':
            pass
        else:
            print(event, values)
        await asyncio.sleep(0)


async def wait_list():
    await asyncio.wait([background(), ui()])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_list())
    loop.close()
