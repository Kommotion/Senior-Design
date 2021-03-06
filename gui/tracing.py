"""
   Copyright 2017 Nicolas Ramirez

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import tkinter
import os
from tkinter import ttk
from utils import constants
from utils import calculators


class TracingOptions:
    def __init__(self, parent):
        self.top = tkinter.Toplevel(parent)
        self._file_path = os.path.dirname(os.path.realpath(__file__))
        self._options = dict()
        self._options['changed'] = False
        self._custom_potrace = tkinter.StringVar()
        self._init_gui()

    def get(self):
        """ Returns the options """
        return self._options

    def _save_options(self):
        """ Sets all the options and saves into a dict """
        self._options['changed'] = True
        self._options['potrace'] = self._custom_potrace
        self._quit()

    def _quit(self):
        """ Destroys this Toplevel widget """
        self.top.destroy()

    def _init_gui(self):
        """ Initializes all the widgets """
        self.top.grab_set()
        geo = calculators.center(self.top.master, 375, 150)
        self.top.geometry(geo)
        self.top.title('Tracing Options')
        self.top.resizable(height=False, width=False)
        self.top.wm_iconbitmap(self._file_path + r'\ucf.ico')
        self.top.grid_columnconfigure(1, weight=1)

        label = 'Custom command line:'
        self.output_label = ttk.Label(self.top, text=label, anchor=tkinter.W)
        self.output_label.grid(padx=5, pady=5, columnspan=10, sticky=tkinter.W)

        self.save_button = ttk.Button(self.top, text='Save', command=self._save_options)
        self.save_button.grid(row=5, padx=5, pady=5, sticky=tkinter.W)

        self.cancel_button = ttk.Button(self.top, text='Cancel', command=self._quit)
        self.cancel_button.grid(row=5, column=1, padx=5, pady=5, sticky=tkinter.W)

        self.custom_entry = ttk.Entry(self.top, textvariable=self._custom_potrace, width=50)
        self.custom_entry.grid(row=1, column=0, columnspan=15, padx=5, sticky=tkinter.W)

        label = 'Warning: Only change the command line option ' \
                'if you know what you\'re doing. This adds on ' \
                'to end of the tracing command so there is no ' \
                'need to specify input and output files.'
        self.warning_label = ttk.Label(self.top, text=label, wraplength=300, justify='left')
        self.warning_label.grid(row=2, padx=5, column=0, rowspan=3)
