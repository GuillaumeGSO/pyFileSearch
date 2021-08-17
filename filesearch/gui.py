"""
Graphical User Interface implemented with PySimpleGUI
"""
import os
import sys
import asyncio
import PySimpleGUI as sg
from filesearch.file_parser import find_files_in_set

lst = list()
layout = [
    [sg.InputText(key="-INPUT-", enable_events=True),
     sg.Text(len(lst), size=(10, 1), key="-NB-")],
    [sg.Listbox(values=lst, size=(140, 30),
                key="-RESULT-", tooltip="double click to open", bind_return_key=True), ],
    [sg.Exit()]
]

window = sg.Window('Py Simple Search', layout, finalize=True)

async def wait_list(my_set):
    """
    builds task list for asynIO
    """
    search_state = {'searching' : False, "interrupting" : False}
    await asyncio.wait([background(my_set, search_state), handle_ui(search_state)])


def construct_interface(my_set):
    """
    prepares event_loop for interface handling
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_list(my_set))
    loop.close()


async def handle_ui(search_state):
    """
    UI build and handling
    """
    last_search = ''
    # Event Loop to process "events"
    while True:
        event, values = window.read(timeout=1)
        if event in (sg.WIN_CLOSED, 'Exit'):
            sys.exit()
        elif event == '-INPUT-':
            if last_search != values['-INPUT-']:
                window['-RESULT-'].update([])
                last_search = values['-INPUT-']
                if search_state['searching']:
                    search_state['interrupting'] = True
        elif event == '-RESULT-':
            file_clicked = values['-RESULT-'][0]
            if search_state['searching']:
                search_state['interrupting'] = True
            os.startfile(file_clicked)
        elif event == '__TIMEOUT__':
            pass
        else:
            print(event, values)
        await asyncio.sleep(0)


async def background(my_set, search_state):
    """
    background task (search) and interuption handling
    """
    search = ''
    while True:
        if window['-INPUT-'].get() != search:
            search = window['-INPUT-'].get()
            #print(search)
            lst.clear()
            window['-NB-'].update(0)
            i = 0
            for item in find_files_in_set(my_set, search):
                i += 1
                lst.append(item)
                if search_state['searching'] and search_state['interrupting']:
                    search_state['interrupting'] = False
                    break
                search_state['searching'] = True
                if i % 100 == 0:
                    window['-RESULT-'].update(lst)
                    window['-NB-'].update(len(lst))
                await asyncio.sleep(0)
            search_state['searching'] = False
            search_state['interrupting'] = False
            window['-RESULT-'].update(lst)
            window['-NB-'].update(len(lst))
        await asyncio.sleep(0.001)
